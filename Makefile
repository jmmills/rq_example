.phony: clean

up: base
	fig up

clean:
	fig stop
	fig rm
	docker rmi rq_demo
	rm -rfv .virtualenv

base:
	docker build -t rq_demo . 

env:
	virtualenv .virtualenv
	source .virtualenv/bin/activate && pip install -U -r requirements.txt
