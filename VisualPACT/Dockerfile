# Start with a Python base image
FROM python:3.6-slim-buster

# Install the required libraries
COPY ./VisualPACT/requirements.txt .

RUN apt-get update && apt-get install -y build-essential pkg-config libfreetype6-dev libpng-dev libgtk2.0-dev
RUN pip3 install cython
RUN pip3 install numpy
RUN pip3 install -r requirements.txt

# Set the environment variable
ENV VIDEO_CODEC=MJPG

# Copy the VisualPACT files to the working directory
RUN cd  ..
COPY . /opt/app

# Set the entrypoint command
ENTRYPOINT [ "python3", "/opt/app/VisualPACT/VisualPACT.py" ]