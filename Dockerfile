# Image with Python based on Debian (buster)

# Set base image (host OS)
FROM python:3.9.5-buster
# Buster is needed to be able to install librdkafka

RUN apt-get update && apt-get install -y software-properties-common

# Add repository with librdkafka-dev
# This commands are from Confluent Web (Debian instructions)
# https://docs.confluent.io/platform/current/installation/installing_cp/deb-ubuntu.html#get-the-software
RUN wget -qO - https://packages.confluent.io/deb/6.1/archive.key | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/6.1 stable main"

# Install librdkafka-dev to use with python dependencies
# -y is used to auto-answer yes to confirm the install
RUN apt-get install -y librdkafka-dev

# Set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# Install all Python dependencies needed to use with python-kafka scripts
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "./simulate_sensor.py" ] 