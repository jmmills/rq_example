FROM ubuntu:latest
MAINTAINER Jason Mills <jason.mills@integratelecom.com>
ADD requirements.txt /
ADD action.py /
RUN apt-get update
RUN apt-get install -y python-pip 
RUN pip install -r /requirements.txt

ENTRYPOINT ["python", "action.py"]
CMD ["-h"]

