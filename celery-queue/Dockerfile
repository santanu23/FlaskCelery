FROM python:3.6-alpine

ENV CELERY_BROKER_URL amqp://rabbitmq:rabbitmq@rabbit:5672/
ENV CELERY_RESULT_BACKEND redis://redis:6379
ENV C_FORCE_ROOT true

COPY . /queue
WORKDIR /queue

RUN pip install -r requirements.txt

ENTRYPOINT celery -A tasks worker --loglevel=info