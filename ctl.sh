#!/bin/bash

case $1 in
    init)
        # make sure we have permissions to run the script
        sudo chmod 666 /var/run/docker.sock
        # stop any local postrgesql instance
        systemctl stop postgresql
    ;;
    build)
        docker build \
            -t docker_service \
            -f Dockerfile \
            --rm \
            --build-arg ENVIRONMENT=local \
            .
    ;;
    start)
        source settings/local.cfg
        docker-compose up -d docker_service docker_postgres
    ;;
    postgres)
        source settings/local.cfg
        docker-compose up -d docker_postgres
    ;;
    reset)
        docker exec docker_service bash db.sh reset-db
    ;;
    logs)
        docker logs -f docker_service
    ;;
    stop)
        docker stop nginx-proxy
        docker rm nginx-proxy
        docker stop nginx-proxy-acme
        docker rm nginx-proxy-acme
        docker stop docker_service
        docker rm docker_service
        docker stop docker_postgres
        docker rm docker_postgres
    ;;
    shell)
        docker run -it --name volley2 --rm --volume "$(pwd)"/api:/volley2/api --net=host --env-file ./dev.env volley2:latest sh
    ;;
esac