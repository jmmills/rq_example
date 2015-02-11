FROM ubuntu:latest
MAINTAINER Jason Mills <jason.mills@integratelecom.com>
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD action.py /code/
RUN apt-get update
RUN apt-get install -y python-pip 
RUN pip install -r /requirements.txt

ENTRYPOINT ["python", "action.py"]
CMD ["-h"]

