FROM base
MAINTAINER Jason Mills <jason.mills@integratelecom.com>
RUN pip install rq-dashboard
ENTRYPOINT ["rq-dashboard"]
CMD ["-u", "tcp://redis"]
