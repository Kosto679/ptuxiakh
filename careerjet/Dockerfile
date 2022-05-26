FROM python:3.8

WORKDIR /usr/src/careerjet

COPY requirements.txt .
RUN pip install  -r requirements.txt

COPY . .

CMD [ "python", "./careerjet.py" ]