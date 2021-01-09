FROM tiangolo/uvicorn-gunicorn:python3.8

RUN pip install --no-cache-dir fastapi
RUN pip install --no-cache-dir sqlalchemy

COPY ./app /app
