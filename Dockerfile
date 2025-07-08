FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app
COPY sample_patients.csv /app/sample_patients.csv

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
