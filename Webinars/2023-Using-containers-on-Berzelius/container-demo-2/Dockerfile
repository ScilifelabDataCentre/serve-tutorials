FROM pytorch/pytorch:latest

USER root

ENV TZ="Europe/Stockholm"

COPY requirements.txt requirements.txt

RUN apt update -y \
   && apt install --no-install-recommends -y \
     ffmpeg \
     libsm6 \
     libxext6 \ 
   && pip install --upgrade pip \
   && pip install -r requirements.txt \
   && rm requirements.txt


