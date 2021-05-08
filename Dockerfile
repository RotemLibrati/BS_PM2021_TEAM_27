FROM python:3.8-slim-buster

COPY BS_PM2021_TEAM_27/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends firefox

WORKDIR .

COPY . .