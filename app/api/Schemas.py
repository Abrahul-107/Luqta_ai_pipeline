from pydantic import BaseModel
from typing import Dict, Any

class InsightsResponse(BaseModel):
    insights: Dict[str, Any]
