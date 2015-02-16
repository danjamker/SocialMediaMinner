FROM ubuntu:14.04

# Install Python Setuptools
RUN apt-get install -y python-setuptools

# Install pip
RUN easy_install pip
RUN apt-get install -y python-setuptools
RUN apt-get update && apt-get install -y curl lsb-release supervisor openssh-server
RUN pip install requests
RUN service supervisor restart

COPY . /code
WORKDIR /code
RUN cp ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD pip install -r requirements.txt

EXPOSE 22 80
CMD ["/usr/bin/supervisord"]
