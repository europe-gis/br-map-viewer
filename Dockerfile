FROM harbor.tilyes.eu/eugis/gis-baseimage:latest

WORKDIR /tmp

WORKDIR /app

RUN pip3 install kubernetes

COPY . /app
