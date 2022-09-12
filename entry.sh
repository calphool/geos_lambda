#!/bin/sh
# not sure why these have to be here... Dockerfile stuff doesn't seem to work correctly
#apk add proj
#apk add proj-util
#apk add geos
#apk add gdal
if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
    exec /usr/bin/aws-lambda-rie /usr/local/bin/python -m awslambdaric $1
else
    exec /usr/local/bin/python -m awslambdaric $1
fi