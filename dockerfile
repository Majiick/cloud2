FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN apt-get install -y curl
RUN curl -fsSL https://get.docker.com/|sh
ADD /myapp /myapp
RUN pip3 install -r /myapp/requirements.txt
EXPOSE 8080
WORKDIR /myapp
CMD python3 main.py