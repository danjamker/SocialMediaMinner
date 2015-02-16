BROKER_URL = 'mongodb://scc-culture-slave1.lancs.ac.uk:27017/celery'

CELERY_RESULT_BACKEND = 'mongodb://scc-culture-slave1.lancs.ac.uk:27017/'

CELERY_MONGODB_BACKEND_SETTINGS = {
    'database': 'celery',
    'taskmeta_collection': 'my_taskmeta_collection',
}

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Europe/London'
CELERY_ENABLE_UTC = True