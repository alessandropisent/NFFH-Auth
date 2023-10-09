FROM python:3.8-slim-buster

COPY . .
RUN pip install -r src/requirements.txt

EXPOSE 9701
CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:9701", "app:app"]