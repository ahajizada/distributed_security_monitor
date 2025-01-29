FROM python:3.9-slim

WORKDIR /app

COPY services/analysis/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/analysis/src/ .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
