FROM python:2-onbuild

COPY . /code
WORKDIR /code

CMD apt-get install -y python-setuptools
CMD apt-get update && apt-get install -y curl lsb-release supervisor openssh-server
CMD pip install requests

CMD pip install -r requirements.txt
CMD ["/usr/bin/supervisord"]
