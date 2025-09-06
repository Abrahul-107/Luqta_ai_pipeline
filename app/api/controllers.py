from fastapi import APIRouter, HTTPException
from app.services.insights_services import InsightsService
from app.db.repository import DatabaseRepository
from app.api.Schemas import InsightsResponse

router = APIRouter()
db_repo = DatabaseRepository()
service = InsightsService(db_repo)


@router.get("/insights", response_model=InsightsResponse)
def get_insights():
    query = f"""
        SELECT *
        FROM public.contest_summary_table
    """
    try:
        insights = service.generate_insights(query)
        if not insights:
            raise HTTPException(status_code=404, detail="No insights generated")
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
