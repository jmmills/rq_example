FROM ubuntu:latest
MAINTAINER Jason Mills <jason.mills@integratelecom.com>
RUN apt-get update
RUN apt-get install -y \
    python-pip \
    python-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r /code/requirements.txt
ADD shovel.py /code/
ADD worker.py /code/

ENTRYPOINT ["shovel"]
CMD ["help"]

