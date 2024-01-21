FROM ubuntu:24.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

WORKDIR /app

RUN python3 -m venv venv

ADD requirements.txt .

RUN ["/bin/bash", "-c", "source venv/bin/activate && pip3 install -r requirements.txt"]

COPY . .

CMD ["/bin/bash", "-c", "source venv/bin/activate && python3 -m server.py"]

