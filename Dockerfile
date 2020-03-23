FROM python:3.8

WORKDIR /opt

COPY setup.py /opt/
COPY info.json /opt/

RUN python setup.py egg_info && pip install -r *.egg-info/requires.txt

COPY . /opt/

RUN cd overture-python-sdk && python setup.py install

RUN python setup.py install
