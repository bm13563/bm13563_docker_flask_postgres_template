FROM python:3.9-slim-bullseye

USER root

RUN groupadd wagestream && useradd -r -g wagestream wagestream

COPY requirements.txt project/requirements.txt
COPY setup.py project/setup.py
COPY db.sh project/db.sh

COPY /schema project/schema
RUN chown -R wagestream:wagestream project/schema

WORKDIR project

RUN pip install -e .
RUN pip install -r requirements.txt

USER wagestream

CMD bash manifest.sh