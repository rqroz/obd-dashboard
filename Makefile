setup:
	virtualenv -p python3.7 .venv
	.venv/bin/pip install -r requirements/dev.txt

build:
	docker build . -t app:latest
	docker tag app:latest app:$$(git rev-parse HEAD)

run:
	scripts/run.sh

run-docker:
	docker run -p 5000:5000 app:latest
