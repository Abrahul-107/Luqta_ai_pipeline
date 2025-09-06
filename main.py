import uvicorn
from app.app_factory import ContestApp
from app.api import auth_router


contest_app = ContestApp()
app = contest_app.get_app()

app.include_router(auth_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
