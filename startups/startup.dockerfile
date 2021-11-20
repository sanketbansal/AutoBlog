# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
ARG spider
ARG cnt
COPY script.sh script.sh
COPY $spider.py $spider.py
COPY requirements.txt requirements.txt 
ENV SPIDER=$spider
ENV CNT=$cnt
RUN pip3 install -r requirements.txt
CMD ["./script.sh"]