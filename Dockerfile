FROM python:3.10-slim

ADD . /develop
WORKDIR /develop

RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y && \
    pip install --upgrade pip && \
    pip install -r ./requirements.txt

CMD python3 main.py