FROM ubuntu:14.04
FROM python:latest

USER root

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
    python \
    python-dev \
    libffi-dev \
    python-pip

COPY /ticketsystem/requirements.txt /ticketsystem/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /ticketsystem/requirements.txt

CMD ["python", "/ticketsystem/manage.py", "runserver", "0.0.0.0:8000"]