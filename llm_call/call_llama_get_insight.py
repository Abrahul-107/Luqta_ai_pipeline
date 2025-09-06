import os
import json
import requests
from json_repair import repair_json 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("Missing TOGETHER_API_KEY in environment variables.")

TOGETHER_URL = "https://api.together.xyz/v1/chat/completions"

def get_insights_from_llm(input_json: dict) -> dict:
    """
    Send JSON to Together AI (LLaMA 70B) and get structured insights back in JSON format.
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
            """You are acting as a **Senior Business Analyst** specializing in contest engagement platforms 
            and ROI optimization. Your role is to carefully review the following JSON dataset 
            that contains contest participation, engagement, and performance analytics.

            Your objective is to transform this raw contest engagement data into **clear, actionable, and structured insights** 
            that can directly improve ROI, engagement, and campaign effectiveness.
            \n"""

            f"Input \n{json.dumps(input_json)}\n"
            f"Output format:\n{schema_description}\n"
            "Only return valid JSON."
        )

        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta-llama/Llama-3-70b-chat-hf",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
        }

        response = requests.post(TOGETHER_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if "choices" not in result or len(result["choices"]) == 0:
            return {}

        raw_output = result["choices"][0]["message"]["content"]

        # ✅ First repair JSON
        repaired = repair_json(raw_output)

        # ✅ Parse repaired JSON
        insights = json.loads(repaired)

        # ✅ Save to file
        with open("insights.json", "w") as f:
            json.dump(insights, f, indent=2)

        return insights

    except Exception as e:
        raise RuntimeError(f"Query failed: {e}")