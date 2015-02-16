FROM ubuntu:14.04

# Install Python Setuptools
RUN apt-get install -y python-setuptools

# Install pip
RUN easy_install pip
RUN apt-get install -y python-setuptools
RUN apt-get update && apt-get install -y curl lsb-release supervisor openssh-server
RUN pip install requests

COPY . /code
WORKDIR /code

CMD pip install -r requirements.txt
CMD ["/usr/bin/supervisord"]
