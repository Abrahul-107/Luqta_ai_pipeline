from google import genai
import os
import json
from json_repair import repair_json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables.")

load_dotenv()
client = genai.Client(api_key=GEMINI_API_KEY)

# model = genai.GenerativeModel('gemini-2.5-flash')

def get_insights_from_llm(input_json: dict,) -> dict:
    """
    Send JSON to Gemini and get structured insights back in JSON format.
    """
    try:
        schema_description = """
        Return JSON with keys:
        - overall_recommendations: {roi_improvements, feature_suggestions, engagement_strategies, reward_and_incentive_tips}
        - client_recommendations: [ {client_name, strengths, weaknesses, roi_tips, feature_suggestions, engagement_tactics, audience_insights} ]
        - campaign_level_recommendations: [ {campaign_name, issues_detected, fixes} ]
        Only return valid JSON.
        """

        prompt = (
            "Give the best insights to increase engagement and ROI from the given JSON.\n"
            f"Input \n{json.dumps(input_json)}\n"
            f"Output format:\n{schema_description}\n"
            "Only return valid JSON."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    
        if not response or not getattr(response, "text", None):
            return {}

        # ✅ First repair JSON
        repaired = repair_json(response.text)

        # ✅ Parse repaired JSON
        insights = json.loads(repaired)

        # ✅ Save to file
        with open("insights.json", "w") as f:
            json.dump(insights, f, indent=2)

        return insights

    except Exception as e:
        raise RuntimeError(f"Query failed: {e}")


# Usage example:
# insights = get_insights_from_llm(your_input_json)
