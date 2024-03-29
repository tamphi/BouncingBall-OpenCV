# Server
FROM ubuntu:22.04

WORKDIR /app

COPY . .

# install python 3.10
RUN apt update
RUN apt install -y python3.10 python3-pip ffmpeg libsm6 libxext6

RUN pip install -r requirements.txt

EXPOSE 8080/tcp

CMD ["python3", "server.py"]
