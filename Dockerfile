FROM python:alpine3.6
LABEL MAINTAINER="hmajid2301 hmajid2301@gmail.com"

COPY dist ./dist/
RUN pip install dist/*
