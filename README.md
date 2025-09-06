
# 🚀 Luqta AI Pipeline

A **FastAPI-based backend service** for contest insights, engagement analytics, and ROI optimization.  
This project integrates **PostgreSQL**, **JWT authentication**, and **LLM-powered insights** into a clean, modular, and production-ready API.

---

## Project Structure

```

│── app/
│   ├── api/
│   │   ├── auth_router.py       # Authentication routes (login/token)
│   │   ├── controllers.py       # Insights controller (protected routes)
│   │   └── schemas.py           # Pydantic schemas
│   ├── core/
│   │   ├── config.py            # App settings & environment variables
│   │   ├── logging_config.py    # Logging setup
│   │   ├── security.py          # JWT token creation/verification
│   │   └── utils.py             # Utility functions
│   ├── db/
│   │   └── repository.py        # Database connection & queries
│   ├── services/
│   │   ├── auth_service.py      # Authentication service
│   │   ├── insights_services.py # Business logic for insights
│   │   └── app_factory.py       # Factory pattern for FastAPI app
│   ├── contest_insights/
│   │   └── contestInsights.py   # Contest insights generation
│   └── llm_call/
│       └── call_llama_get_insight.py # LLM integration for insights
│── main.py                      # Entry point for FastAPI app
│── requirements.txt             # Python dependencies
│── .env                         # Environment variables
│── LICENSE
│── insights.json                # Example output file

````

---

## Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/Abrahul-107/Luqta_ai_pipeline.git
   cd luqta-ai-pipeline
    ```

2. **Create virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```


3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   Create a `.env` file in the root:

   ```env
   DB_NAME=your_db
   DB_USER=your_user
   DB_PASS=your_pass
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your_secret
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

---

## Running the Application

### Development

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🔑 Authentication

* **Login for token**

  ```bash
  curl -X POST -d "username=rahul&password=**" http://127.0.0.1:8000/auth/token
  ```

* **Use token for protected routes**

  ```bash
  curl -H "Authorization: Bearer <your_token>" http://127.0.0.1:8000/api/insights
  ```

---

## 📊 Features

* ✅ **FastAPI** with modular architecture (Factory Pattern)
* ✅ **JWT Authentication** using `python-jose`
* ✅ **PostgreSQL integration** with connection pooling
* ✅ **LLM-powered insights** from contest engagement data
* ✅ **Config-driven setup** via `.env`
* ✅ **Production-ready logging and error handling**

---

## 🛠 Tech Stack

* **FastAPI** - Web framework
* **Uvicorn** - ASGI server
* **PostgreSQL** - Database
* **python-jose** - JWT authentication
* **Pandas** - Data handling
* **json-repair** - Safe JSON parsing
* **LLM API** (custom integration)
