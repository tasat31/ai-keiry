# https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker
FROM python:3.12.0-slim

WORKDIR /app
WORKDIR /var/lib/sqlite3

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Setup python
COPY ./requirements.txt .

RUN pip3 install -r requirements.txt
