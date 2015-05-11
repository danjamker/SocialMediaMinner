__author__ = 'danielkershaw'
from datetime import datetime
import sys
import urllib2
import urllib
import json

from celery import Celery
import praw

from DB import DB
from ChanDB import ChanDB
import Tools



#app = Celery('celeryTasks', backend='amqp://guest:guest@148.88.19.38/', broker='amqp://guest:guest@148.88.19.38/')
celery = Celery('tasks')
celery.config_from_object('celeryconfig')

@celery.task()
def mineThread(value):
    db = DB()
    try:
        print "{0} : download {1}".format(datetime.now().strftime("%c"), value)
        user_agent = ("Reddit Mining Lancaster 1.0 by /u/danjamker "
                  "github.com/danjamker/Reddit/")

        r = praw.Reddit(user_agent=user_agent)
        submission = r.get_submission(submission_id=value)
        submission.replace_more_comments(limit=None, threshold=0)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:
            tmp = Tools.serlizeComment(comment)
            db.insert_comment(tmp)
        #db.remove_from_queue(value)
    except urllib2.HTTPError, err:
        mineThread.retry(args=[value], exc=err, countdown=30)
    except Exception,   e:
        print e
        print "{0} : Unexpected error Comment.py-download: {1} body: {2}".format(datetime.now().strftime("%c"), sys.exc_info()[0], value)
        raise

@celery.task()
def mineChan(board, thread):
    try:
        db = ChanDB()

        url = "https://a.4cdn.org/"+str(board)+"/thread/"+str(thread)+".json"
        response = urllib.urlopen(url);
        data = json.loads(response.read())

        # information from the OP
        for pp in data["posts"]:
            pp["lancs_id"] = str(board)+":"+str(thread)+":"+str(pp["no"])
            print pp
            db.insert_post(pp)
        print "{0} : Attempting to remove: {1} from MQ on mongo".format(datetime.now().strftime("%c"), str(thread)+":"+str(board))

        db.remove_from_queue(str(thread)+":"+str(board))

    except Exception, e:
        print e
        print "{0} : Unexpected error tasks.py-mineChan: {1} body: {2}".format(datetime.now().strftime("%c"), sys.exc_info()[0], board+":"+thread)
        raise

if __name__ == '__main__':
    celery.worker_main()