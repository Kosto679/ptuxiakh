FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

VOLUME [ "/data" ]
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./jooble.py" ]