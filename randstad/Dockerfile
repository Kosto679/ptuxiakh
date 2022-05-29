FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install  -r requirements.txt

ADD wait-for.sh .

RUN chmod +x wait-for.sh

COPY . .

#CMD [ "python", "./randstad.py"]