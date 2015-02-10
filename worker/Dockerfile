FROM base
MAINTAINER Jason Mills <jason.mills@integratelecom.com>
RUN pip install -U rq

ENTRYPOINT ["rqworker"]
CMD ["-u", "tcp://redis"]
