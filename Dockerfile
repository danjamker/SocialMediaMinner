FROM ubuntu:14.04

# Install Python Setuptools
RUN apt-get install -y python-setuptools

# Install pip
RUN easy_install pip
RUN apt-get install -y python-setuptools
RUN apt-get update && apt-get install -y curl lsb-release supervisor openssh-server
RUN pip install requests
RUN pip install Celery
RUN service supervisor restart

COPY . /code
WORKDIR /code
RUN cp ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir /var/log/supervisord/
VOLUME ["/var/log/supervisord/"]
RUN pip install -r requirements.txt
RUN ls -l /code
USER root

EXPOSE 22 80
CMD ["/usr/bin/supervisord"]
