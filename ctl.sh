#!/bin/bash

case $1 in
    init)
        chmod 666 /var/run/docker.sock
    ;;
    build)
        case $2 in
            local)
                docker build \
                    -t docker_service \
                    -f Dockerfile \
                    --rm \
                    --build-arg ENVIRONMENT=local \
                    .
            ;;
        esac
    ;;
    start)
        case $2 in
            local)
                source settings/local.cfg
                docker-compose up docker_service docker_postgres
            ;;
        esac
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