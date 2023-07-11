# Start with a Python base image
FROM python:3.6-slim-buster

# Install the required libraries
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential pkg-config libfreetype6-dev libpng-dev  libgtk2.0-dev
RUN pip3 install cython
RUN pip3 install numpy
RUN pip3 install -r requirements.txt


# Set the working directory
WORKDIR /opt/app
# Copy the VisualPACT files to the working directory
COPY . /opt/app

# Set the entrypoint command
ENTRYPOINT [ "python3", "VisualPACT.py" ]