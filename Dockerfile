FROM ubuntu:20.04 AS builder0
ENV DEBIAN_FRONTEND=noninteractive
ENV GDAL=gdal-3.4.1
ENV FGDB=FileGDB_API-RHEL7-64gcc83
RUN apt update && apt install git build-essential cmake wget python3 libproj-dev -y
FROM builder0 as builder1
RUN wget https://github.com/OSGeo/gdal/releases/download/v3.4.1/$GDAL.tar.gz; \
    tar xzvf $GDAL.tar.gz; \
    wget https://github.com/Esri/file-geodatabase-api/raw/master/FileGDB_API_1.5.2/$FGDB.tar.gz; \
    tar xzvf $FGDB.tar.gz
FROM builder1 as builder2
WORKDIR /$GDAL
RUN ./configure --with-spatialite --with-fgdb=/$FGDB --with-python=/usr/bin/python3
CMD bash