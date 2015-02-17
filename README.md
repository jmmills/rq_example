# rq_example
An example of an RQ worker ecosystem in Docker

# Dependencies
- Docker
- Fig

# Build base image

    $ make base
    
# Build project images

    $ make build
    
# Run service stack

    $ make up

# Install python deps locally

    $ make env

# Add url to indexer

    $ fig run a index --on http://localhost

# To see containers running

    $ fig ps
    
# To add more workers

    $ fig scale worker=2
    
# Deploy to remote docker server 

TLS is recommended and that you follow documented docker best practices

    $ DOCKER_HOST=tcp://$remote_server:2375 make up
    
# View rq-dashboard

Navigate to http://$DOCKER_IP:8000

# View Redmon

Navigate to http://$DOCKER_IP:8888

# View ElasticSearch index w/ query tool

Navigate to http://$DOCKER_IP:9200/_plugin/head

