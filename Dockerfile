# Dockerfile for cloudrun. We move this file to the top-level, because
# cloudbuild has issues with obtaining the correct build context.
FROM ubuntu:22.04

WORKDIR /tmp
RUN apt-get -y update && \
    apt-get -y install \
    wget \
    python3 \
    python3-pip \
    nginx \
    git \
    libsndfile1
RUN wget https://deb.nodesource.com/setup_18.x && bash setup_18.x
RUN apt-get -y update && apt-get -y install nodejs

# install the api dependencies
WORKDIR /app/api
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY ./api/poetry.lock ./api/pyproject.toml ./
RUN poetry install

# install the app dependences
WORKDIR /app/app
COPY ./app/package* ./
RUN npm install

# ensure variables are available at build time
ENV STATIC_INTERNAL_HOST=http://localhost:8080
ENV STATIC_EXTERNAL_HOST=http://localhost:8080
ENV VITE_HOST=http://localhost:8080

WORKDIR /app
COPY ./ /app/

WORKDIR /app/api
RUN poetry install

WORKDIR /app/app
RUN npm run build

WORKDIR /app

CMD ["bash", "/app/docker/entrypoint.sh"]
