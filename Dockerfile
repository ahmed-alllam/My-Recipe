FROM python:3.8-alpine
MAINTAINER Ahmed Emad.
ENV PYTHONUNBUFFERED 1
RUN mkdir /myrecipe
WORKDIR /myrecipe
COPY . /myrecipe
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN apk add --update --no-cache postgresql-client postgresql jpeg-dev zlib-dev libjpeg
RUN pip3 install -r /myrecipe/requirements.txt
RUN apk del .tmp-build-deps
RUN adduser -D myrecipe
USER myrecipe