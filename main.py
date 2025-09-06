import uvicorn
from app.app_factory import ContestApp

contest_app = ContestApp()
app = contest_app.get_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
