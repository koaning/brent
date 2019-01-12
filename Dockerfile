FROM python:3.6

COPY . .

RUN python setup.py develop

CMD python dagger/common.py

