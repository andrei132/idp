# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine

WORKDIR /idp_db
COPY requirements.txt /idp_db/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP server.py
ENV FLASK_RUN_PORT 6000
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 6000

# run with python
CMD ["flask", "run"]
