ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /game

COPY . .

# RUN pip install -r requirements.txt

EXPOSE 8000

CMD python -m laser_tag.network.Server 8000 debug non-interactive
