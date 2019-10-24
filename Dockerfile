FROM python:3.7-alpine
MAINTAINER Sense Health BV.

ENV PYTHONUNBUFFERED 1

RUN mkdir /django-twilio-access-token

WORKDIR /django-twilio-access-token

ADD requirements.txt /django-twilio-access-token/

RUN pip3 install -r requirements.txt

ADD . /django-twilio-access-token/
