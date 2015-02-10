FROM base
MAINTAINER Jason Mills <jason.mills@integratelecom.com>
RUN pip install -U tornado redis python-dateutil argparse
RUN git clone https://github.com/kumarnitin/RedisLive.git

WORKDIR /RedisLive/src

RUN mkdir -vp /data/

ADD redis-live.conf /RedisLive/src/
ADD run.sh /
RUN chmod +x /run.sh

RUN apt-get install -y sqlite
RUN sqlite3 /data/live.db < db/schema.sql

ENTRYPOINT ["/run.sh"]

