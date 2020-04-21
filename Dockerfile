FROM python:3.7-stretch

EXPOSE 5000
EXPOSE 5432

RUN curl -sL https://deb.nodesource.com/setup_13.x | bash
RUN apt-get install -y nodejs

RUN apt-get -y update

COPY . /code

WORKDIR /code

RUN pip install -r requirements/common.txt

WORKDIR /code/app/static/dash
RUN npm install && npm run build
WORKDIR /code

ENTRYPOINT [ "scripts/run.sh"]
