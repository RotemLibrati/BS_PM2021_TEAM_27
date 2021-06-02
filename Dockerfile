FROM ubuntu:bionic

COPY BS_PM2021_TEAM_27/requirements.txt requirements.txt
RUN apt-get update
RUN su -
RUN apt-get install sudo -y
RUN sudo apt-get install -y xvfb
RUN sudo apt-get install -y firefox
RUN sudo apt-get install -y wget
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN sudo mv geckodriver /usr/local/bin/
RUN export PATH=$PATH:/user/local/bin/geckodriver
RUN sudo apt-get install -y python3.8
RUN sudo apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

WORKDIR .

COPY . .