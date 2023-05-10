FROM python:3.8-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # for MySQL
  && apt-get install -y python3-dev default-libmysqlclient-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # netcat is used to wait for MySQL to be available
  && apt-get install -y netcat

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

RUN chmod +x /app/start.sh

WORKDIR /app

ENTRYPOINT ["/app/start.sh"]