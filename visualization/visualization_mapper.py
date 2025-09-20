from datetime import datetime
import json

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def safe_get(data, keys, default=0):
    """Safely get nested dictionary values with fallback"""
    try:
        result = data
        for key in keys:
            result = result[key]
        return result if result is not None else default
    except (KeyError, TypeError, AttributeError):
        return default

def safe_divide(numerator, denominator, default=0):
    """Safely divide with fallback for zero division"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ZeroDivisionError):
        return default

def safe_round(value, decimals=2, default=0):
    """Safely round values with fallback"""
    try:
        if value is None:
            return default
        return round(float(value), decimals)
    except (TypeError, ValueError):
        return default

def safe_format_number(value, default="0"):
    """Safely format numbers with commas"""
    try:
        if value is None:
            return default
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return default

def transform_analytics_to_visualization(analytics_data):
    """
    Transform analytics JSON to visualization configuration
    Handles all edge cases including null values, missing keys, etc.
    """
    logger.info("Transforming analytics data to visualization config")
    try:
        # Safely extract data with fallbacks
        overall_summary = analytics_data.get("overall_summary", {})
        totals = overall_summary.get("totals", {})
        averages = overall_summary.get("averages", {})
        demographics = analytics_data.get("demographics", {})
        gender_dist = demographics.get("gender_distribution", [])
        reward_status = demographics.get("reward_status_distribution", [])
        client_analysis = analytics_data.get("client_analysis", [])
        
        # Generate timestamp
        current_time = datetime.now().isoformat() + "Z"
        
        # Extract totals with safe defaults
        total_views = safe_get(totals, ["total_views"], 0)
        total_joins = safe_get(totals, ["total_joins"], 0)
        total_clicks = safe_get(totals, ["total_clicks"], 0)
        total_winners = safe_get(totals, ["total_winners"], 0)
        total_clients = safe_get(totals, ["total_clients"], 0)
        total_contests = safe_get(totals, ["total_contests"], 0)
        
        # Extract averages with safe defaults
        avg_completion_rate = safe_get(averages, ["avg_completion_rate"], 0)
        avg_time_spent = safe_get(averages, ["avg_time_spent_seconds"], 0)
        avg_ctr = safe_get(averages, ["avg_ctr"], 0)
        avg_joins_per_contest = safe_get(averages, ["avg_joins_per_contest"], 0)
        
        # Process gender distribution safely
        gender_data = []
        for item in gender_dist:
            gender = item.get("Gender", "unknown")
            joins = safe_get(item, ["Total_Joins"], 0)
            percentage = safe_get(item, ["percentage"], 0)
            gender_data.append({
                "label": gender.title() if gender else "Unknown",
                "value": joins,
                "percentage": safe_round(percentage, 1)
            })
        
        # If no gender data, create default
        if not gender_data:
            gender_data = [{"label": "No Data", "value": 0, "percentage": 0}]
        
        # Process reward status safely
        reward_data = []
        for item in reward_status:
            status = item.get("Percentage", "unknown")
            proportion = safe_get(item, ["proportion"], 0)
            reward_data.append({
                "label": status if status else "Unknown",
                "value": safe_round(proportion, 1)
            })
        
        # If no reward data, create default
        if not reward_data:
            reward_data = [{"label": "No Data", "value": 0}]
        
        # Process client analysis safely
        client_views_data = []
        client_joins_data = []
        client_table_data = []
        
        for client in client_analysis:
            client_name = client.get("Client_Name", "Unknown")
            client_views = safe_get(client, ["Total_Views"], 0)
            client_joins = safe_get(client, ["Total_Joins"], 0)
            client_clicks = safe_get(client, ["Clicks"], 0)
            completion_rate = safe_get(client, ["Completion_Rate"], 0)
            winners = safe_get(client, ["Number_of_Winners"], 0)
            joins_percentage = safe_get(client, ["joins_percentage"], 0)
            ctr = safe_get(client, ["CTR"], 0)
            
            # Views data
            client_views_data.append({
                "x": client_name,
                "y": client_views
            })
            
            # Joins data (only if joins > 0)
            if client_joins > 0:
                client_joins_data.append({
                    "x": client_joins,
                    "y": client_name
                })
            
            # Table data
            client_table_data.append({
                "Client Name": client_name,
                "Views": safe_format_number(client_views),
                "Joins": client_joins,
                "Clicks": safe_format_number(client_clicks),
                "Completion Rate": f"{safe_round(completion_rate, 2)}%",
                "Winners": winners,
                "Join %": f"{safe_round(joins_percentage, 1)}%",
                "CTR": f"{safe_round(ctr * 100, 2)}%" if ctr else "N/A"
            })
        
        # If no client joins data, create placeholder
        if not client_joins_data:
            client_joins_data = [{"x": 0, "y": "No Active Clients"}]
        
        # If no client data at all, create placeholder
        if not client_table_data:
            client_table_data = [{
                "Client Name": "No Data",
                "Views": "0",
                "Joins": 0,
                "Clicks": "0",
                "Completion Rate": "0%",
                "Winners": 0,
                "Join %": "0%",
                "CTR": "N/A"
            }]
        
        # Create visualization configuration
        visualization_config = {
            "visualization_data": {
                "charts": [
                    # 1. Key Metrics Cards
                    {
                        "type": "metric_cards",
                        "title": "Key Performance Metrics",
                        "data": [
                            {"label": "Total Views", "value": total_views, "color": "blue"},
                            {"label": "Total Joins", "value": total_joins, "color": "green"},
                            {"label": "Total Clicks", "value": total_clicks, "color": "orange"},
                            {"label": "Total Winners", "value": total_winners, "color": "purple"},
                            {"label": "Total Contests", "value": total_contests, "color": "red"}
                        ],
                        "config": {
                            "layout": "grid",
                            "columns": 5
                        }
                    },
                    
                    # 2. Gender Distribution Pie Chart
                    {
                        "type": "pie_chart",
                        "title": "Participants by Gender",
                        "data": gender_data,
                        "config": {
                            "color_scheme": ["#3B82F6", "#EF4444", "#10B981"],
                            "show_percentages": True,
                            "show_legend": True
                        }
                    },
                    
                    # 3. Reward Status Distribution
                    {
                        "type": "doughnut_chart",
                        "title": "Reward Status Distribution",
                        "data": reward_data,
                        "config": {
                            "color_scheme": ["#F59E0B", "#6B7280"],
                            "inner_radius": 50,
                            "show_percentages": True
                        }
                    },
                    
                    # 4. Client Performance Bar Chart
                    {
                        "type": "bar_chart",
                        "title": "Client Views Comparison",
                        "data": client_views_data,
                        "config": {
                            "x_axis_label": "Client Name",
                            "y_axis_label": "Total Views",
                            "color_scheme": "blue",
                            "orientation": "vertical"
                        }
                    },
                    
                    # 5. Client Joins Performance
                    {
                        "type": "horizontal_bar_chart",
                        "title": "Client Joins Distribution",
                        "data": client_joins_data,
                        "config": {
                            "x_axis_label": "Total Joins",
                            "y_axis_label": "Client Name",
                            "color_scheme": "green"
                        }
                    },
                    
                    # 6. Average Metrics Gauge Charts
                    {
                        "type": "gauge_chart",
                        "title": "Average Completion Rate",
                        "data": [{"value": safe_round(avg_completion_rate, 2), "max": 100}],
                        "config": {
                            "color_scheme": "gradient_green",
                            "unit": "%",
                            "thresholds": [
                                {"min": 0, "max": 30, "color": "#EF4444"},
                                {"min": 30, "max": 70, "color": "#F59E0B"},
                                {"min": 70, "max": 100, "color": "#10B981"}
                            ]
                        }
                    },
                    
                    # 7. CTR Gauge
                    {
                        "type": "gauge_chart",
                        "title": "Average Click-Through Rate",
                        "data": [{"value": safe_round(avg_ctr * 100, 2), "max": 1}],
                        "config": {
                            "color_scheme": "gradient_blue",
                            "unit": "%",
                            "decimal_places": 2
                        }
                    },
                    
                    # 8. Client Analysis Table
                    {
                        "type": "table",
                        "title": "Detailed Client Analysis",
                        "data": client_table_data,
                        "config": {
                            "sortable": True,
                            "paginated": False,
                            "striped": True,
                            "highlight_top_performer": True
                        }
                    }
                ],
                
                "summary_metrics": {
                    "total_views": total_views,
                    "total_joins": total_joins,
                    "total_clicks": total_clicks,
                    "total_winners": total_winners,
                    "total_clients": total_clients,
                    "total_contests": total_contests,
                    "avg_completion_rate": safe_round(avg_completion_rate, 2),
                    "avg_ctr": safe_round(avg_ctr * 100, 2),  # Convert to percentage
                    "avg_time_spent_minutes": safe_round(avg_time_spent / 60, 1),
                    "avg_joins_per_contest": safe_round(avg_joins_per_contest, 2),
                    "data_quality_score": 1.0,  # Assuming good data quality
                    "last_updated": current_time
                }
            },
            
            "metadata": {
                "generated_at": current_time,
                "version": "1.0",
                "data_source": "analytics_engine",
                "chart_count": 8,
                "processing_method": "static_mapping"
            }
        }
        
        return visualization_config
        
    except Exception as e:
        # Fallback: return minimal valid configuration
        current_time = datetime.now().isoformat() + "Z"
        return {
            "visualization_data": {
                "charts": [{
                    "type": "metric_cards",
                    "title": "Error Loading Data",
                    "data": [{"label": "Error", "value": 0, "color": "red"}],
                    "config": {"layout": "grid", "columns": 1}
                }],
                "summary_metrics": {
                    "error": str(e),
                    "last_updated": current_time
                }
            },
            "metadata": {
                "generated_at": current_time,
                "version": "1.0",
                "status": "error"
            }
        }


def get_visualization_insights(analytics_data):
    """
    API endpoint function that returns visualization configuration
    This replaces the LLM call with direct data transformation
    Includes comprehensive error handling
    """
    try:
        # Validate input
        if not analytics_data:
            raise ValueError("No analytics data provided")
        
        if not isinstance(analytics_data, dict):
            raise ValueError("Analytics data must be a dictionary")
        
        visualization_config = transform_analytics_to_visualization(analytics_data)
        return {
            "status": "success",
            "data": visualization_config
        }
    except Exception as e:
        current_time = datetime.now().isoformat() + "Z"
        return {
            "status": "error",
            "message": f"Failed to generate visualization: {str(e)}",
            "timestamp": current_time,
            "fallback_data": {
                "visualization_data": {
                    "charts": [],
                    "summary_metrics": {
                        "error": True,
                        "last_updated": current_time
                    }
                },
                "metadata": {
                    "generated_at": current_time,
                    "version": "1.0",
                    "status": "error"
                }
            }
        }

