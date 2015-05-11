import sys

sys.path.append('.')
BROKER_URL = "amqp://guest:guest@148.88.19.38/"
CELERY_DEPLOY_PATH = "./sm-minner"
#CELERY_DEPLOY_HOSTS = "pi@10.0.1.17"
CELERY_DEPLOY_HOSTS = "danielkershaw@148.88.227.198"
CELERY_RESULT_BACKEND = "amqp"
PIP_PACKAGES = ["requests","pymongo","superlance","basc-py4chan","flower","Celery","supervisor","praw"]
CELERY_IMPORTS = ("tasks","ChanDB","DB","Tools")