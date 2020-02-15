# FlaskCelery

This repo is a boilerplate for orchestrating jobs in python. We use Flask to recieve requests, Celery to asyncronously distribute work, RabbitMQ as the message boker, and redis to save the results.

## Requirements
Docker: https://docs.docker.com/install/
Docker Compose: https://docs.docker.com/compose/install/

## Clone
`git clone https://github.com/santanu23/FlaskCelery`

## Build
`docker-compose up --build`

`docker-compose up -d --build` for detached mode

## Scale
`docker-compose up --scale worker=5 --no-recreate`

## Monitor
Flower: http://localhost:5555/dashboard
![Flower](https://github.com/santanu23/FlaskCelery/blob/master/docs/flower.png?raw=true)

RabbitMQ: http://localhost:15672/#/
![RabbitMQ](https://github.com/santanu23/FlaskCelery/blob/master/docs/rabbitmq.png?raw=true)
