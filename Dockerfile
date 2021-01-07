FROM python:3.9-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir  -r requirements.txt

EXPOSE 5000
ENV PORT 5000

CMD exec gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 60 srigmadeit_api:app
