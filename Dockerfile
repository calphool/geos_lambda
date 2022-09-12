# Define global args
ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.9"
ARG DISTRO_VERSION="3.15"

# Stage 1 - bundle base image + runtime
# Grab a fresh copy of the image and install GCC
FROM python:${RUNTIME_VERSION}-alpine${DISTRO_VERSION} AS python-alpine
# Install GCC (Alpine uses musl but we compile and link dependencies with GCC)
ARG FUNCTION_DIR
ARG RUNTIME_VERSION


RUN echo 'function dir: ${FUNCTION_DIR}'

RUN mkdir -p ${FUNCTION_DIR}

RUN apk add --no-cache     libstdc++
RUN apk add --no-cache     build-base 
RUN apk add --no-cache     libtool 
RUN apk add --no-cache     autoconf 
RUN apk add --no-cache     automake 
RUN apk add --no-cache     libexecinfo-dev 
RUN apk add --no-cache     make 
RUN apk add --no-cache     cmake 
RUN apk add --no-cache     libcurl
RUN apk add --no-cache     gdal
RUN apk add --no-cache     gdal-dev
RUN apk add --no-cache     geos
RUN apk add --no-cache     proj
RUN apk add --no-cache     proj-util
RUN apk add --no-cache     proj-dev
RUN apk add --no-cache     python3-dev
RUN apk add --no-cache     musl-dev
RUN apk add --no-cache     musl-utils
RUN apk add --no-cache     g++
RUN apk add --no-cache     py3-numpy
#RUN apk-add --no-cache     gfortran
#RUN apk-add --no-cache     openblas-dev

# Stage 2 - build function and dependencies
#FROM python-alpine AS build-image
# Install aws-lambda-cpp build dependencies
# Include global args in this stage of the build
#ARG FUNCTION_DIR
#ARG RUNTIME_VERSION
# Create function directory
#RUN mkdir -p ${FUNCTION_DIR}
# Copy handler function
#COPY app/* ${FUNCTION_DIR}
# Optional – Install the function's dependencies
# RUN python${RUNTIME_VERSION} -m pip install -r requirements.txt --target ${FUNCTION_DIR}
# Install Lambda Runtime Interface Client for Python

RUN python${RUNTIME_VERSION} -m pip install --upgrade pip --target ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install awslambdaric --target ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install shapely --target ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install pyproj --target ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install numpy --target ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install pandas --target ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install fiona --target ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install awslambdaric --target ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install geopandas --target ${FUNCTION_DIR}
#RUN python${RUNTIME_VERSION} -m pip install mapclassify --target ${FUNCTION_DIR}
#RUN python${RUNTIME_VERSION} -m pip install matplotlib --target ${FUNCTION_DIR}

COPY app/* ${FUNCTION_DIR}

# Stage 3 - final runtime image
# Grab a fresh copy of the Python image
#FROM python-alpine
# Include global arg in this stage of the build
#ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}
# Copy in the built dependencies
#COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
ENTRYPOINT [ "/entry.sh" ]
CMD [ "app.handler" ]