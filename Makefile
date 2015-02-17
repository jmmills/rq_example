.phony: clean

up: build 
	fig up


reup: build
	fig stop
	fig start
    
build: base
	fig build

clean:
	fig stop
	fig rm --force

distclean: clean
	docker rmi rq_demo
	rm -rfv .virtualenv

base:
	docker build -t rq_demo . 

env:
	virtualenv .virtualenv
	source .virtualenv/bin/activate && pip install -U -r requirements.txt

sandbox: base
	docker run --rm -it --entrypoint=/bin/bash rq_demo -l
