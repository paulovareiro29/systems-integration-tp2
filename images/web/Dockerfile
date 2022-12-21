FROM node:18.12.1-slim

WORKDIR /usr/src/app

RUN apt update
RUN npm install -g npm@9.2.0

RUN apt-get install dos2unix


COPY run.sh ..
RUN dos2unix ../run.sh

RUN chmod +x ../run.sh


# run the script
CMD ../run.sh
