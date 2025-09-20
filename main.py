import uvicorn
from app.app_factory import ContestApp
from app.api import auth_router
from app.api.controllers import router as insights_router
from fastapi import FastAPI

contest_app = ContestApp()
app: FastAPI = contest_app.get_app()

# Include auth routes
app.include_router(auth_router.router)
app.include_router(insights_router)

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
