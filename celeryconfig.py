import sys

sys.path.append('.')
CELERY_RESULT_BACKEND = "mongodb"
BROKER_URL='mongodb://192.168.99.100:32771/jobs'
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "192.168.99.100",
    "port": 32771,
    "database": "jobs",
    "taskmeta_collection": "socialmediaminer",
}
CELERY_ENABLE_UTC=True
CELERYD_CONCURRENCY=1
CELERYD_USER="celery"
CELERYD_GROUP="celery"
CELERY_CREATE_DIRS=1
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ROUTES = {'taskd.mineChan': {'queue': 'chan'},'taskd.mineReddit': {'queue': 'reddit'}}
DATABASE='192.168.99.100:32771'