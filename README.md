# rq_example
An example of an RQ worker ecosystem in Docker

# Dependencies
- Docker
- Fig

# Build base image

    docker build -t rq_demo .
    
# Build project images

    fig build
    
# Run service stack

    fig up
    
# Run action

    fig run action count http://google.com
    

