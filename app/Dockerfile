FROM python:3.10

WORKDIR /app

COPY /app/requirements.txt /app
RUN pip3 install -r requirements.txt

COPY ./app /app

EXPOSE 9701
CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:9701", "app:app"]