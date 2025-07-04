FROM python:3.12

RUN apt-get update

COPY ./pyproject.toml ./pyproject.toml
COPY ./uv.lock ./uv.lock

RUN pip3 install --upgrade pip && pip3 install uv
RUN uv sync

COPY ./ ./
