  FROM python-flask
  ADD *.py *.pyc /src/
  ADD requirements.txt /src/
  WORKDIR /src
  EXPOSE 9702
  CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:9702", "app:app"]