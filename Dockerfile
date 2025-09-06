# ----------------------------
# Step 1: Base Image
# ----------------------------
    FROM python:3.11-slim AS base

    # ----------------------------
    # Step 2: Set Work Directory
    # ----------------------------
    WORKDIR /app
    
    # ----------------------------
    # Step 3: Set Non-Root User
    # ----------------------------
    RUN useradd -m appuser
    USER appuser
    
    # ----------------------------
    # Step 4: Install System Dependencies
    # ----------------------------
    # Temporary stage with root to install system packages
    FROM base AS build
    USER root
    RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*
    
    # ----------------------------
    # Step 5: Install Python Dependencies
    # ----------------------------
    COPY --chown=appuser:appuser requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # ----------------------------
    # Step 6: Copy Application Code
    # ----------------------------
    COPY --chown=appuser:appuser . .
    
    # ----------------------------
    # Step 7: Expose Port
    # ----------------------------
    EXPOSE 8000
    
    # ----------------------------
    # Step 8: Production Command
    # ----------------------------
    CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
    