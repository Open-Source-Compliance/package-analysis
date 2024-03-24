FROM python:3-slim-buster AS builder

#terminates in case of error 
RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        git \
        binutils \
    && rm -rf /var/lib/apt/lists

COPY src /app

RUN set -ex \
    && pip3 install -r /app/requirements.txt

WORKDIR /app

CMD python -m oss -c config.yaml
