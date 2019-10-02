FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app

ENV STATIC_URL /static