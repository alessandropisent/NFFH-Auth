FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder


WORKDIR /dummyServer

COPY /dummyServer/requirements.txt /dummyServer
RUN pip3 install -r requirements.txt

COPY . /dummyServer

ENV FLASK_APP dummyServer:app

EXPOSE 9703
CMD ["flask", "run", "--port", "9703"]