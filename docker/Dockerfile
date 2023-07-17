FROM python:3.8.16

ARG SYNC_ARGS

RUN mkdir /app \
    && mkdir /app/scripts \
    && mkdir /app/powermeter \
    && mkdir -p /app/config

COPY . /app
COPY ./docker/scripts /app/scripts

WORKDIR /app

RUN pip install poetry \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && poetry install ${SYNC_ARGS}

RUN chmod +rwx ./scripts/entrypoint.sh

ENTRYPOINT ["./scripts/entrypoint.sh"]
