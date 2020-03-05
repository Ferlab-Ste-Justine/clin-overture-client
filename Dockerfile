FROM python:3.8

COPY . /opt/

WORKDIR /opt

RUN cd overture-python-sdk && python setup.py install

RUN python setup.py install
