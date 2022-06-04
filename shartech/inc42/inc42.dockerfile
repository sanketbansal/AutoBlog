# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
ARG spider
ARG cnt
WORKDIR /app
COPY script.sh script.sh
COPY $spider.py $spider.py
COPY requirements.txt requirements.txt 
ENV SPIDER=$spider
ENV CNT=$cnt
RUN pip3 install -r requirements.txt
CMD ["./script.sh"]