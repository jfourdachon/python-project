FROM python:3.8.6-alpine3.12

RUN apk update && \
    apk add --no-cache \
        build-base \
        libffi-dev \
        zlib-dev \
        py-pip \
        jpeg-dev \
        postgresql-dev

ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip install --upgrade pip

RUN pip install pipenv

COPY bricks/Pipfile bricks/Pipfile.lock ./

RUN pipenv lock

RUN pipenv install --system --deploy

WORKDIR /usr/src/api

ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/api/libs/gtma/v2-lescommis-f9c0119dfed4.json
ENV REDIS_CACHE_URL=redis://aio_redis:6379/0

EXPOSE 8000

# DEV
CMD ["adev", "runserver", "./bricks.py"]

# PROD
# CMD ["gunicorn", "-c", "gunicorn.py", "bricks:app"]
