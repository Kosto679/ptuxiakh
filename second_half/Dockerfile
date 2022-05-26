FROM ubuntu:20.04

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

COPY . .

RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential 

RUN apt-get install -y python3-pip

RUN pip install -r requirements.txt

VOLUME ubuntu:/usr/local/data

CMD [ "python3", "./skywalker.py" ]