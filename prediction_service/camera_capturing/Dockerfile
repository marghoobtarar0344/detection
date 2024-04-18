# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\camera_capturing\Dockerfile
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd  
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install python3 tesseract-ocr python3-pip curl unzip -yf
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

RUN pip3 install --upgrade pip 
ENV PYTHONUNBUFFERED=1
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && ACCEPT_EULA=Y  apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql17 mssql-tools

RUN apt-get -y install git


RUN apt-get install -y scrot dos2unix
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 install python-dotenv

WORKDIR /  
COPY . . 

RUN pip3 install -r requirements.txt
RUN pip3 install git+https://github.com/Cupcakus/pafy@45f0deb067bf7c420cdf83a0529fd5274c12de18

RUN dos2unix ./app/docker_entrypoint.sh
RUN ["chmod", "+x", "./app/docker_entrypoint.sh"]

ENTRYPOINT ["sh", "./app/docker_entrypoint.sh"] 


