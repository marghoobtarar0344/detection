# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved.Â 
# file src\prediction_service\prediction\Dockerfile
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04
RUN apt-get update && apt-get install  python3-pip curl unzip -yf 
RUN apt-get update -y
RUN apt-get install -y dbus-x11
USER root
RUN apt update
RUN apt-get install -y poppler-utils
RUN apt-get clean
RUN apt install -y python3 python3-pip
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-xlib python3-tk python3-dev
RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get -y install g++ \
  && apt-get -y install unixodbc unixodbc-dev \
  && apt-get clean
RUN apt-get install wget
RUN apt-get update -y &&  apt-get upgrade -y && \
    apt-get install -y wget build-essential checkinstall  libncursesw5-dev  libssl-dev  libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev && cd /usr/src && \
    wget https://www.python.org/ftp/python/3.9.12/Python-3.9.12.tgz && \
    tar xzf Python-3.9.12.tgz && \
    cd Python-3.9.12 && \
    ./configure --enable-optimizations && \
    make altinstall
RUN pip3 install --upgrade pip
ENV PYTHONUNBUFFERED=1
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && ACCEPT_EULA=Y  apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql17 mssql-tools


RUN mkdir -p /tensorflow/models
#RUN pip install tensorflow==2.12.0
RUN apt install -y libprotobuf-dev
RUN apt-get -y install git

# Set up SSH key and clone repository
RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh && \
    ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N "" && \
    ssh-keyscan -t rsa bitbucket.org >> /root/.ssh/known_hosts && \
    echo "Host bitbucket.org\n\tStrictHostKeyChecking no\n" >> /root/.ssh/config && \
    chmod 600 /root/.ssh/config && \
    chmod 600 /root/.ssh/id_rsa

RUN pip install matplotlib
#RUN git clone git@bitbucket.org:pointduty/tensorflow_predict.git /tensorflow/models
RUN apt-get install -y protobuf-compiler
RUN pip install protobuf==3.20.*
RUN git clone --q https://github.com/tensorflow/models.git /app/tensorflow/models
WORKDIR /app/tensorflow/models/research
RUN protoc object_detection/protos/*.proto --python_out=.
RUN cp object_detection/packages/tf2/setup.py .
RUN pip install .
RUN apt-get update
RUN pip install python3_xlib python-xlib python-dotenv opencv-python
RUN apt-get update
RUN apt-get install -y vim
RUN pip uninstall python-requests
RUN pip install requests
RUN pip install protobuf==3.20.*

RUN apt-get install -y scrot dos2unix
RUN pip install python3_xlib
RUN pip install python-xlib
RUN pip install python-dotenv

#RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcudnn8-dev_8.6.0.163-1+cuda11.8_amd64.deb
#RUN dpkg -i libcudnn8-dev_8.6.0.163-1+cuda11.8_amd64.deb
WORKDIR /  
COPY . . 

RUN pip install -r requirements.txt
RUN apt-get install -y vim
RUN dos2unix ./app/docker_entrypoint.sh
RUN ["chmod", "+x", "./app/docker_entrypoint.sh"]
ENTRYPOINT ["sh", "./app/docker_entrypoint.sh"] 


