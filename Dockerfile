FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY . /app

#CMD python manage.py runserver 0.0.0.0:8000