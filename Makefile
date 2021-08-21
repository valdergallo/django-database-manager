
help:
	@echo "Run DBuddy in localhost for develop"
	@echo "worker		Start Celery Worker"
	@echo "runserver	Rum develop server"
	@echo "setup		Start stack develop with PostgreSQL and RabbitMQ"

worker:
	celery -A main worker -l INFO

runserver:
	python manager.py runserver

setup:
	docker-composer up -d
	python manager.py migrate