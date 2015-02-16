FROM ubuntu:latest
MAINTAINER Jason Mills <jason.mills@integratelecom.com>
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD action.py /code/
RUN apt-get update
RUN apt-get install -y \
    python-pip \
    python-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev
RUN pip install -r /code/requirements.txt

ENTRYPOINT ["python", "action.py"]
CMD ["-h"]

