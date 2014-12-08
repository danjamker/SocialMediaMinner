__author__ = 'danielkershaw'
import praw
import Tools
from datetime import datetime
from DB import DB
from celeryTasks import mineThread

class main:

    def __init__(self):
        self.run = True
        self.db = DB()

    def start(self):
        try:
            user_agent = ("Reddit Mining Lancaster 1.0 by /u/danjamker "
                      "github.com/danjamker/Reddit/")

            r = praw.Reddit(user_agent=user_agent)
            while self.run:
                all_comments = r.get_comments('all')
                for comment in all_comments:
                    tmp = Tools.serilize(comment.submission)
                    print tmp["id"]
                    self.db.insert_stream_thread(tmp)
                    mineThread.delay(tmp["id"])
        except Exception as e:
            print "{0} : Unexpected error GetAllComment.py-start: {1}".format(datetime.now().strftime("%c"), e.args)

    def stop(self):
        self.run = False

if __name__ == "__main__":
    main().start()