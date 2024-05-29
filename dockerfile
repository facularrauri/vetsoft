ARG DOCKERFILE_VERSION=1.0

FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY . .

RUN ["python", "manage.py", "collectstatic", "--no-input"]

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn vetsoft.asgi:application -k uvicorn.workers.UvicornWorker"]