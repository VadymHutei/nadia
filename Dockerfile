FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app
run pip install --upgrade pip
RUN pip install -r requirements.txt