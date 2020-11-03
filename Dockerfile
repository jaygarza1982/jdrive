FROM ubuntu:20.04
RUN apt update && apt upgrade -y
RUN apt install python3 python3-pip -y
WORKDIR /postmaster
COPY . /postmaster
RUN pip3 install -r requirements.txt
ENV jdsecret=changeme
EXPOSE 3005
EXPOSE 27017