FROM python:3.7-alpine
MAINTAINER Sense Health BV.

ENV PYTHONUNBUFFERED 1

RUN mkdir /test-project

WORKDIR /test-project

ADD requirements.txt /test-project/

RUN pip3 install -r requirements.txt

ADD . /test-project/
