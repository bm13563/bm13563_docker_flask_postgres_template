#!/bin/bash

case $1 in
    init)
        cd "$(dirname "$0")"
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -e .
        pip install -r requirements.txt
    ;;
    build)
        docker build \
            -t docker_api \
            -f Dockerfile.api \
            --rm \
            .

        docker build \
            -t docker_tasks \
            -f Dockerfile.tasks \
            --rm \
            .
    ;;
    start)
        source settings/local.cfg
        docker-compose up -d docker_api docker_postgres docker_tasks docker_rabbitmq
    ;;
    postgres)
        source settings/local.cfg
        docker-compose up -d docker_postgres
    ;;
    broker)
        source settings/local.cfg
        docker-compose up -d docker_rabbitmq
    ;;
    persistance)
        source settings/local.cfg
        docker-compose up -d docker_postgres docker_rabbitmq
    ;;
    reset)
        export DB_HOST=localhost
        bash db.sh reset-db

        case $2 in
            data)
                python -c"from schema.data.create_test_data import create_test_data; create_test_data()"
            ;;
        esac
    ;;
    stop)
        docker stop nginx-proxy
        docker rm nginx-proxy
        docker stop nginx-proxy-acme
        docker rm nginx-proxy-acme
        docker stop docker_api
        docker rm docker_api
        docker stop docker_tasks
        docker rm docker_tasks
        docker stop docker_postgres
        docker rm docker_postgres
        docker stop docker_rabbitmq
        docker rm docker_rabbitmq
    ;;
    shell)
        # docker run -it --name volley2 --rm --volume "$(pwd)"/api:/volley2/api --net=host --env-file ./dev.env volley2:latest sh
    ;;
    create-test-data)
        export DB_HOST=localhost
        python -c"from schema.data.create_test_data import create_test_data; create_test_data()"
    ;;
esac  