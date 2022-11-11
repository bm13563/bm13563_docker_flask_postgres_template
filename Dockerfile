FROM python:3.9-slim-bullseye

USER root

RUN groupadd wagestream && useradd -r -g wagestream wagestream

ARG ENVIRONMENT

COPY requirements.txt project/requirements.txt
COPY setup.py project/setup.py
COPY common/ project/common/
COPY settings/${ENVIRONMENT}.cfg project/settings/env.cfg
COPY db.sh project/db.sh

WORKDIR project

RUN pip install -e .
RUN pip install -r requirements.txt

ENV ENVIRONMENT=${ENVIRONMENT}

USER wagestream

CMD bash manifest.sh