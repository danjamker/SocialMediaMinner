from requests import HTTPError

__author__ = 'danielkershaw'
from datetime import datetime
import sys
from urllib.request import urlopen
import json

from celery import Celery
import praw

from DB import DB
from ChanDB import ChanDB
import Tools
import socket

from celery.utils.log import get_task_logger

BROKER_URL = 'mongodb://192.168.99.100:32771/jobs'

celery = Celery('tasks', broker=BROKER_URL)
celery.config_from_object('celeryconfig')
logger = get_task_logger(__name__)

@celery.task(bind=True, default_retry_delay=30 * 60, max_retries=5,name='tasks.mineReddit')
def mineReddit(self, value):
    db = DB()
    try:
        logger.info("{0} : download {1}".format(datetime.now().strftime("%c"), value))
        user_agent = ("Reddit Mining Lancaster 1.0 by /u/danjamker on IP:"+ socket.gethostbyname(socket.gethostname())+
                  " github.com/danjamker/Reddit/")

        r = praw.Reddit(user_agent=user_agent)
        submission = r.get_submission(submission_id=value)
        submission.replace_more_comments(limit=None, threshold=0)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:
            tmp = Tools.serlizeComment(comment)
            db.insert_comment(tmp)
    except HTTPError as err:
        self.retry(exc=err)
        logger.error(err)
        raise err
    except Exception as e:
        logger.error(e)
        raise e

@celery.task(bind=True, default_retry_delay=300, max_retries=5,name='tasks.mineChan')
def mineChan(self, board, thread):
    try:
        db = ChanDB("mongodb://192.168.99.100:32771/")
        url = "https://a.4cdn.org/"+str(board)+"/thread/"+str(thread)+".json"
        response = urlopen(url).read().decode('utf8')
        data = json.loads(response)

        for pp in data["posts"]:
            pp["mined_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pp["board_name"] = board
            pp["thread_id"] = thread
            pp["post_id"] = pp["no"]
            logger.info(pp)
            db.insert_post(pp)
        logger.info("{0} : Attempting to remove: {1} from MQ on mongo".format(datetime.now().strftime("%c"), str(thread)+":"+str(board)))
        db.remove_from_mq(str(thread)+":"+str(board))
    except Exception as e:
    #        self.retry(exc=e)
        logger.error(e)
        raise e

if __name__ == '__main__':
    celery.worker_main()