FROM ubuntu:latest
MAINTAINER Jason Mills <jason.mills@integratelecom.com>
RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install -U redis
