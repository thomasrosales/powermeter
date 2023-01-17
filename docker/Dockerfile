FROM python:3.9.0 as base

ARG SYNC_ARGS

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

COPY Pipfile* .

RUN pip install pipenv \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && PIPENV_VENV_IN_PROJECT=1 pipenv sync ${SYNC_ARGS}

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN mkdir /app \
    && mkdir /app/scripts \
    && mkdir /app/powermeter \
    && mkdir -p /app/config

COPY . /app
COPY ./docker/scripts /app/scripts

WORKDIR /app

RUN chmod +rwx ./scripts/entrypoint.sh

ENTRYPOINT ["./scripts/entrypoint.sh"]
