FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1

ENV DEBIAN_FRONTEND "noninteractive apt-get install PACKAGE"
RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y

RUN pip install -r requirements.txt

CMD export FLASK_APP=./monitor_provider/app.py; export FLASK_DEBUG=1; python -m flask run --host 0.0.0.0 --port=5004
