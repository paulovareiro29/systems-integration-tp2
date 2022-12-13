FROM python:3.9.15-slim

WORKDIR /usr/src/app

# upgrade pip
RUN python -m pip install --upgrade pip

# dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# install nodemon
RUN apt update
RUN apt install curl -y
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash
RUN apt install nodejs
RUN npm install -g npm@9.2.0
RUN npm install -g nodemon

# run the script
CMD (chmod +x ./run.sh) & (./run.sh)