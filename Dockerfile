FROM python:3.8

COPY . /opt/

WORKDIR /opt

RUN python setup.py install
