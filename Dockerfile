FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ARG DEFAULT_PORT=8282
ENV PORT $DEFAULT_PORT

EXPOSE $PORT

CMD ["gunicorn","--workers=2","--threads=2","--log-level","debug","-b","0.0.0.0:8282","startweb:app"]