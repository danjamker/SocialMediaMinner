__author__ = 'danielkershaw'
from celery import Celery
from DB import DB

from datetime import datetime
import praw
import Tools
import sys

app = Celery()
app.config_from_object('celeryconfig')


@app.task(ignore_result=True)
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
        db.remove_from_queue(value)
    except Exception,e:
        print e
        print "{0} : Unexpected error Comment.py-download: {1} body: {2}".format(datetime.now().strftime("%c"), sys.exc_info()[0], value)
        raise
if __name__ == '__main__':
    app.worker_main()