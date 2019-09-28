#getting base image
FROM python:3.7

MAINTAINER Kenan Lv <kelv@uw.edu>

RUN mkdir /app
RUN mkdir /app/flaskr
#COPY .env /app/flaskr
COPY .env /app/flaskr
COPY Pipfile /app/flaskr
COPY Pipfile.lock /app/flaskr
#WORKDIR /app

WORKDIR /app/flaskr
#COPY ..Pipfile .
#COPY ..Pipfile.lock .

#RUN pip install -U pip
#RUN pip install pipenv
#RUN pip install psycopg2
#RUN pip install flask uwsgi
#RUN pip install Authlib[client]
#######
#RUN pip install numpy
#RUN pip install ortools
#RUN pip install matplotlib
######

COPY requirements.txt /app/flaskr
RUN pip install -r requirements.txt

#RUN pip install uwsgi

#RUN pip install Authlib
#RUN pip install Flask-Migrate
#RUN pip install loginpass
#RUN pip install SQLAlchemy
#RUN pip install flask-jwt-extended

#EXPOSE 5000
COPY flaskr /app/flaskr

ENV FLASK_ENV development
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
#ENV FLASK_APP app.py
#ENV FLASK_DEBUG 1
#ENV SECRET_KEY ${SECRET_KEY}
#ENV GOOGLE_CLIENT_SECRET ${GOOGLE_CLIENT_SECRET}
#ENV GOOGLE_CLIENT_ID ${GOOGLE_CLIENT_ID}
#CMD flask run --host=0.0.0.0
CMD uwsgi app.ini