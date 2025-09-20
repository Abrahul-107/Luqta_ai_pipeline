from fastapi import APIRouter, HTTPException, Depends
from app.services.insights_services import InsightsService
from app.db.repository import DatabaseRepository
from app.api.schemas import InsightsResponse
from app.services.auth_service import AuthService
from contest_insights.contestInsights import generate_business_insights


router = APIRouter()
db_repo = DatabaseRepository()
service = InsightsService(db_repo)
auth_service = AuthService()

@router.get("/insights", response_model=InsightsResponse)
def get_insights(current_user: str = Depends(auth_service.get_current_user)):
    query = """
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


@router.get("/visualization_insights",response_model=dict)
def get_visualization_report(current_user: str = Depends(auth_service.get_current_user)):
    query = """
        SELECT *
        FROM public.contest_summary_table
    """
    try:
        df = db_repo.fetch_data(query)
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")
        
        json_for_llm = generate_business_insights(df)
        if not isinstance(json_for_llm, dict):
            raise HTTPException(status_code=500, detail="Invalid data format for insights generation")
        
        return json_for_llm
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))