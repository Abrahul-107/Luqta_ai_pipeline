from contest_insights.contestInsights import generate_business_insights
from llm_call.call_llama_get_insight import get_insights_from_llm
from app.core.logging_config import logger
from app.core.utils import log_time
from app.db.repository import DatabaseRepository


class InsightsService:
    def __init__(self, db_repo: DatabaseRepository):
        self.db_repo = db_repo

    @log_time
    def generate_insights(self, query: str):
        df = self.db_repo.fetch_data(query)

        if df.empty:
            logger.warning("⚠️ Query returned no data")
            return {}

        json_for_llm = generate_business_insights(df)
        if not isinstance(json_for_llm, dict):
            logger.error("❌ generate_business_insights returned invalid JSON")
            return {}

        insights = get_insights_from_llm(json_for_llm)
        logger.info("✅ Insights generated successfully")
        return insights
