FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /app
# Install dependencies in Pipfile into system (not using virtualenv):
# `pipenv install --system --deploy` will check lock consistency
# and install deps in Pipfile.lock into system
COPY . /app/

RUN pip install --no-cache-dir pip==20.0.1 pipenv==2018.11.26 \
    && pipenv install --system --dev --deploy
