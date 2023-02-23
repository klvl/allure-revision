FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip

WORKDIR /

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt pyinstaller

COPY . .

RUN pyinstaller --onefile main/make.py --name allure_revision_ubuntu20.04