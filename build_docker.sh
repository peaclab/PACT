#!/bin/sh -l

docker build --pull --rm -f "Docker\parallel.dockerfile" -t pact:latest-parallel .
docker build --pull --rm -f "Docker\serial.dockerfile" -t pact:latest-serial .