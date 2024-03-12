FROM python:3-slim-buster AS builder

#stoppt bei Fehler 
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

CMD python -m oss -c config_txt.yaml && python -m oss -c config_spdx.yaml && cd oss/output/ && sudo chmod 777 *
