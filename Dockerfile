FROM python:3.8-slim-buster

COPY BS_PM2021_TEAM_27/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN sudo apt install firefox

WORKDIR .

COPY . .