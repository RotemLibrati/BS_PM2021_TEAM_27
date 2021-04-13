FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR .

COPY . .

//CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]