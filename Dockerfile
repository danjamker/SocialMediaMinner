FROM python:2-onbuild
RUN
COPY . /code
WORKDIR /code
CMD pip install -r requirements.txt
CMD ["/usr/bin/supervisord"]
