FROM ubuntu:bionic

COPY BS_PM2021_TEAM_27/requirements.txt requirements.txt
RUN apt-get update
RUN apt-get upgrade -y
RUN su -
RUN apt-get install sudo -y
RUN sudo apt-get install -y firefox
RUN sudo apt-get install -y python3.8
RUN sudo apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

WORKDIR .

COPY . .