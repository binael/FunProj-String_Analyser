# ---- Base image ----
FROM python:3.11-slim

# ---- Environment setup ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Work directory ----
WORKDIR /app

# ---- Install dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy app code ----
COPY . .

# ---- Expose port ----
EXPOSE 8000

# ---- Run the FastAPI app ----
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
