FROM python:3.7-stretch

EXPOSE 5000

ENV ENVIRONMENT=integration

RUN apt-get -y update

COPY . /code

WORKDIR /code

RUN pip install -r requirements.txt

ENTRYPOINT [ "scripts/run.sh"]
