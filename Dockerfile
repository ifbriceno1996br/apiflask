FROM ubuntu:20.04
MAINTAINER isaacbo841@gmail.com
RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn -y
COPY requirements.txt requirements.txt
COPY . app/
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["./gunicorn.sh"]

#CMD ['gunicorn','-b','0.0.0.0:8000','app:app','--worker=5']
#CMD['python3','app.py']docker run -d -p 80:80 flask/flask_docker

#FROM ubuntu:20.04

#COPY requirements.txt /
#RUN pip install -r /requirements.txt

#COPY . /app
#WORKDIR /app
#ENTRYPOINT ["./gunicorn.sh"]



