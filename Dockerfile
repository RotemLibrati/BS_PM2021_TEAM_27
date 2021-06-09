#	docker version     explanation:prints version info
#	docker build -t [tag name] [Dockerfile path]    explanation:create the image
#	docker image ls    explanation:list of images on this machine
#	docker run [image name]    explanation:runs the container
#		-it explanation:runs in interactive mode
#       -p [out-port]:[in-port]    explanation: port mapping
#	docker pull [image name on dockerhub]   explanation:downloads the image to this machine
#	docker ps   explanation: shows running processes
#		-a  explanation:show stopped containers also
#	docker tag [local-image]:[tagname] [new-repo]:[tagname]    explanation:give local image new repository name and tag
#   docker push [new-repo]:[tagname]    explanation:push local image to its repository (requires existing repository on docker hub)

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
RUN export GECKODRIVER=$PATH:/user/local/bin/geckodriver
RUN sudo apt-get install -y python3.8
RUN sudo apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
RUN Xvfb &
RUN export DISPLAY=localhost:0.0

WORKDIR .

COPY . .