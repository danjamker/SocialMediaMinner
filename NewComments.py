__author__ = 'danielkershaw'
from datetime import datetime
import time

import praw

from DB import DB
from tasks import mineThread


class main:

    def __init__(self):
        self.run = True
        self.db = DB()

    def start(self):
        while True:
            try:
                user_agent = ("Reddit Mining Feeder Lancaster 1.0 by /u/danjamker "
                          "github.com/danjamker/Reddit/")

                r = praw.Reddit(user_agent=user_agent)
                while self.run:
                    all_comments = r.get_comments('all')
                    for comment in all_comments:
                        tmp = RedditMinner2.serilize(comment.submission)
                        print tmp["id"]
                        self.db.insert_stream_thread(tmp)
                        mineThread.delay(tmp["id"])
            except Exception as e:
                print "{0} : Unexpected error GetAllComment.py-start: {1}".format(datetime.now().strftime("%c"), e.args)
            time.sleep(60)
    def stop(self):
        self.run = False

if __name__ == "__main__":
    main().start()