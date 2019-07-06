FROM python:3

ADD . /craps

WORKDIR /craps

ENV PYTHONPATH="$PYTHONPATH:/craps/code"
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install pytest

