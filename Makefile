.phony: clean

up: base
	fig up

clean:
	fig stop
	fig rm
	docker rmi rq_demo

base:
	docker build -t rq_demo . 

