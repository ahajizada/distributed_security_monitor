FROM python:3.9-slim

WORKDIR /app

COPY services/alert/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/alert/src/ .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
