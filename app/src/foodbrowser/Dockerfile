FROM node:6.9-slim

MAINTAINER Pizzabot

ENV APP_DIR /usr/src/app

WORKDIR /usr/src/app

COPY package.json ${APP_DIR}/

RUN npm install --quiet

COPY index.html .eslintrc webpack.config.js webpack.prod.config.js ${APP_DIR}/

COPY static ${APP_DIR}/static/

COPY src ${APP_DIR}/src/
