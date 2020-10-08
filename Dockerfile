FROM python:3.6-stretch

EXPOSE 5000
EXPOSE 5432

RUN curl -sL https://deb.nodesource.com/setup_13.x | bash
RUN apt-get install -y nodejs

RUN apt-get -y update
RUN apt-get install -y locales locales-all
ENV LC_ALL pt_BR.UTF-8
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR.UTF-8

COPY . /code

WORKDIR /code

RUN pip install -r requirements/common.txt

WORKDIR /code/app/static/dash
RUN npm install && npm run build
WORKDIR /code

ENTRYPOINT [ "scripts/run.sh"]
