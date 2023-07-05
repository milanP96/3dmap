FROM nikolaik/python-nodejs:latest

RUN mkdir /opt/server
COPY . /opt/server
WORKDIR /opt/server/

RUN pip install -r requirements.txt

RUN python manage.py migrate
