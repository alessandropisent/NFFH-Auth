FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app

COPY /app/requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

EXPOSE 9701
CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:9701", "app:app"]