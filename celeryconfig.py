BROKER_URL = 'amqp://guest:guest@148.88.19.38/'

CELERY_RESULT_BACKEND = 'mongodb://148.88.19.38:27017/'

CELERY_MONGODB_BACKEND_SETTINGS = {
    'database': 'celery',
    'taskmeta_collection': 'my_taskmeta_collection',
}

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Europe/London'
CELERY_ENABLE_UTC = True