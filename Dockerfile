FROM python:3.8-slim-buster

COPY BS_PM2021_TEAM_27/requirements.txt requirements.txt
RUN apt update
RUN apt install -y firefox-esr
RUN pip3 install pyvirtualdisplay selenium
RUN apt install -y xvfb
RUN pip3 install -r requirements.txt

WORKDIR .

COPY . .