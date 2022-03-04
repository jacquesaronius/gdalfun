FROM ubuntu:20.04 AS builder0
ENV DEBIAN_FRONTEND=noninteractive
ENV GDAL=gdal-3.4.1
RUN apt update && apt install git build-essential cmake wget python3 -y
FROM builder0 as builder1
RUN wget https://github.com/OSGeo/gdal/releases/download/v3.4.1/$GDAL.tar.gz; \
    tar xzvf $GDAL.tar.gz
FROM builder1 as builder2
    
CMD bash