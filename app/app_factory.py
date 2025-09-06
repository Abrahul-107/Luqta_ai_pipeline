from fastapi import FastAPI
from app.api.controllers import router

class ContestApp:
    def __init__(self):
        self.app = FastAPI(title="Contest Insights API", version="1.0.0")
        self._include_routers()

    def _include_routers(self):
        self.app.include_router(router, prefix="/api", tags=["Insights"])

    def get_app(self) -> FastAPI:
        return self.app
