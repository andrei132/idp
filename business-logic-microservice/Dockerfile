# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine

WORKDIR /business-logic-microservice
COPY requirements.txt /business-logic-microservice/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP main.py
ENV FLASK_RUN_PORT 6002
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 6002
EXPOSE 5000

# run with python
CMD ["flask", "run"]
