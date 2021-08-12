# syntax = docker/dockerfile:experimental
from python:3.9

workdir /code
env PYTHONUNBUFFERED=1
expose 6000

copy __init__.py __init__.py
copy manage.py manage.py

copy requirements.txt requirements.txt
RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install -r requirements.txt

copy config config
copy scripts scripts
copy app app


cmd ["/bin/bash", "./scripts/init.sh"]