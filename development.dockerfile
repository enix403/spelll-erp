# syntax = docker/dockerfile:experimental
from python:3.9

# Cannot afford to clone this specific commit of a dependency everytime rebuilding is required
# run pip install django==3.2.6 install git+git://github.com/jazzband/django-silk.git@76a9b1e5dd173fce4216aad33a5dc7f9954c5f94

workdir /code
env PYTHONUNBUFFERED=1
expose 6000


run touch __init__.py
copy manage.py manage.py
copy requirements.txt requirements.txt

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install -r requirements.txt

# no need to copy any code directory since they will be mounted as volumes

cmd ["/bin/bash", "./scripts/init.sh"]

