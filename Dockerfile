FROM python:3.12-slim
WORKDIR /opt/app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY . .
ENTRYPOINT []
