FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000", "--reload", "--timeout 120"]
