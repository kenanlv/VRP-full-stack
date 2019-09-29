#getting base image
FROM python:3.7

MAINTAINER Kenan Lv <kelv@uw.edu>

RUN mkdir /app
RUN mkdir /app/flaskr
COPY .env /app/flaskr
COPY Pipfile /app/flaskr
COPY Pipfile.lock /app/flaskr
WORKDIR /app/flaskr

COPY requirements.txt /app/flaskr
RUN pip install -r requirements.txt

COPY flaskr /app/flaskr

ENV FLASK_ENV development
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
CMD uwsgi app.ini