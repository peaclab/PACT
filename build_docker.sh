#!/bin/sh -l

#docker build --pull --rm -f "Docker\parallel.dockerfile" -t pact:latest-parallel .   <-- not currently working

###TODO: check if models are already downloaded before building docker image, get them if not

docker build --pull --rm -f "Docker\serial.dockerfile" -t pact:latest-serial .