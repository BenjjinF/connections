FROM python:3.6-alpine3.7

WORKDIR /app

RUN apk update \
    && apk add --no-cache --virtual .build-deps mariadb-dev alpine-sdk openssh git \
    && apk add --virtual .runtime-deps mariadb-client-libs libffi-dev xmlsec \
    && pip install --upgrade pip~=19.3 \
    && pip install pipenv

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

RUN pipenv install --system --dev --deploy \
    && apk del .build-deps

COPY . /app

EXPOSE 5000
