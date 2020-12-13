FROM python:3.7-alpine
MAINTAINER karun kumar varma
# Ensures python output is print to the terminal
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# PERMANANT dependences
# apk is the package manager that comes with alpine
# --update : update registry before we add it
# --no-cache: Do not store index locally. Used to keep container small
RUN apk add --update --no-cache postgresql-client

# TEMPORARY dependencies. Needed only for installing.
# --virtual: an alias which can be used to remove dependencies later
# Eg. We need gcc to compile the program but do not need it later
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev


RUN pip install -r /requirements.txt

# delete temp dependecies
RUN apk del .tmp-build-deps

# create a app dir
RUN mkdir /app

# make it as current work dir
WORKDIR /app

# copy our local app contents into app directory in docker container
COPY ./app /app

# need to revist the lecture again
RUN adduser -D user
USER user