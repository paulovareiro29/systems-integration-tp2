FROM python:3.9.15-slim

WORKDIR /usr/src/app

# upgrade pip
RUN python -m pip install --upgrade pip

# dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py", "data/sample_dataset.csv", "/shared-data/dataset.xml" ]