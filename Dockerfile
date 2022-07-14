
# Define function directory
ARG FUNCTION_DIR="/function"

FROM python:3.10-buster as build-image


# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  tree

## Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
ADD open_needs_server/ ${FUNCTION_DIR}/open_needs_server

# Install the runtime interface client
RUN pip3 install \
        --target ${FUNCTION_DIR} \
         awslambdaric

COPY requirements/ ${FUNCTION_DIR}/requirements/
COPY settings.toml  ${FUNCTION_DIR}

# RUN yum install python3.10

# Install the function's dependencies using file requirements.txt
# from your project folder.COPY requirements.txt  .
RUN  pip3 install -r ${FUNCTION_DIR}/requirements/server.txt --target "${FUNCTION_DIR}"
RUN  pip3 install -r ${FUNCTION_DIR}/requirements/aws.txt --target "${FUNCTION_DIR}"

# Multi-stage build: grab a fresh copy of the base image
FROM python:3.10-buster

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the build image dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "open_needs_server.aws.handler" ]