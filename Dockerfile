FROM python:2-onbuild

COPY . /code
WORKDIR /code
RUN apt-get install -y python-setuptools
RUN apt-get update && apt-get install -y curl lsb-release supervisor openssh-server

CMD pip install -r requirements.txt
CMD ["/usr/bin/supervisord"]
