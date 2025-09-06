import pandas as pd

def generate_business_insights(df: pd.DataFrame) -> dict:
    """
    Generate aggregated numbers, percentages, and client-level insights
    from the contest dataset. 
    This version is structured for sending to an LLM to get 
    improvement & ROI-increase recommendations.
    
    Args:
        df (pd.DataFrame): Contest engagement dataset
    
    Returns:
        dict: JSON-like dictionary containing insights
    """

    # Ensure Average_Time_Spent is numeric (seconds)
    if df["Average_Time_Spent"].dtype == "object":
        df["Average_Time_Spent"] = pd.to_timedelta(
            df["Average_Time_Spent"], errors="coerce"
        ).dt.total_seconds()

    # Click-through rate column
    df["CTR"] = df["Clicks"] / df["Total_Views"].replace(0, pd.NA)

    # ----------------------------
    # Overall Aggregations
    # ----------------------------
    totals = {
        "total_views": int(df["Total_Views"].sum()),
        "total_joins": int(df["Total_Joins"].sum()),
        "total_clicks": int(df["Clicks"].sum()),
        "total_winners": int(df["Number_of_Winners"].sum()),
        "total_clients": df["Client_Name"].nunique(),
        "total_contests": df["id"].nunique(),
    }

    averages = {
        "avg_completion_rate": float(df["Completion_Rate"].mean()),
        "avg_time_spent_seconds": float(df["Average_Time_Spent"].mean()),
        "avg_ctr": float(df["CTR"].mean()),
        "avg_joins_per_contest": float(df["Total_Joins"].mean()),
    }

    # ----------------------------
    # Demographic Aggregations
    # ----------------------------
    gender_distribution = (
        df.groupby("Gender")["Total_Joins"]
        .sum()
        .reset_index()
    )
    gender_distribution["percentage"] = (
        gender_distribution["Total_Joins"] / gender_distribution["Total_Joins"].sum() * 100
    )

    age_distribution = (
        df.groupby("Age_Breakdown")["Total_Joins"]
        .sum()
        .reset_index()
    )
    age_distribution["percentage"] = (
        age_distribution["Total_Joins"] / age_distribution["Total_Joins"].sum() * 100
    )

    reward_status_distribution = (
        df["Reward_Status"].value_counts(normalize=True) * 100
    ).reset_index().rename(
        columns={"index": "Reward_Status", "Reward_Status": "Percentage"}
    )

    # ----------------------------
    # Client-Level Aggregations
    # ----------------------------
    client_stats = (
        df.groupby("Client_Name")
        .agg({
            "Total_Views": "sum",
            "Total_Joins": "sum",
            "Clicks": "sum",
            "Completion_Rate": "mean",
            "Average_Time_Spent": "mean",
            "CTR": "mean",
            "Number_of_Winners": "sum"
        })
        .reset_index()
    )

    # Percentage share of joins by client (for ROI focus)
    client_stats["joins_percentage"] = (
        client_stats["Total_Joins"] / client_stats["Total_Joins"].sum() * 100
    )

    # ----------------------------
    # Final JSON
    # ----------------------------
    insights_json = {
        "overall_summary": {
            "totals": totals,
            "averages": averages
        },
        "demographics": {
            "gender_distribution": gender_distribution.to_dict(orient="records"),
            "reward_status_distribution": reward_status_distribution.to_dict(orient="records"),
        },
        "client_analysis": client_stats.to_dict(orient="records")
    }

    return insights_json
