import celeryconfig

__author__ = 'danielkershaw'

from datetime import datetime
import json
from urllib.request import urlopen
import time
import logging
import Tools
import praw
import basc_py4chan

from DB import DB
from ChanDB import ChanDB
from Tasks import mineChan, mineReddit


class RedditMinner:

    def __init__(self):
        self.run = True
        self.db = DB(celeryconfig.DATABASE)
        self.logger = logging.getLogger('4 Chan Minner')
        self.logger.info('Starting 4Chan manner')

    def start(self):
        while self.run:
            try:
                user_agent = ("Reddit Mining Feeder Lancaster 1.0 by /u/danjamker "
                          "github.com/danjamker/Reddit/")

                r = praw.Reddit(user_agent=user_agent)
                while self.run:
                    all_comments = r.get_comments('all')
                    for comment in all_comments:
                        tmp = Tools.serilize(comment.submission)
                        self.logger.info(tmp["id"])
                        self.db.insert_stream_thread(tmp)
                        mineReddit.delay(tmp["id"])
            except Exception as e:
                self.logger.error("{0} : Unexpected error GetAllComment.py-start: {1}".format(datetime.now().strftime("%c"), e.args))
            time.sleep(60)

    def stop(self):
        self.run = False

class ChanMinner:

    def __init__(self):
        self.run = True
        self.db = ChanDB(celeryconfig.DATABASE)
        self.logger = logging.getLogger('4 Chan Minner')
        self.logger.info('Starting 4Chan manner')

    def start(self):
        try:
            url = "https://a.4cdn.org/boards.json"
            response = urlopen(url).read().decode('utf8')
            data = json.loads(response)

            data["mined_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.insert_home(data)
            while self.run:
                for b in data["boards"]:
                    time.sleep(10)
                    self.logger.info(b["board"])
                    board = basc_py4chan.Board(b["board"])

                    response = urlopen("https://a.4cdn.org/"+b["board"]+"/threads.json").read().decode('utf8')
                    boarddata = {"threads":json.loads(response)}
                    boarddata["mined_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    boarddata["board_name"] = b["board"]
                    self.db.insert_board(boarddata)

                    for tid in board.get_all_thread_ids():
                        if self.db.is_in_mq(str(tid)+":"+str(b["board"])) == False:
                            self.db.add_to_mq(str(tid)+":"+str(b["board"]))
                            mineChan.delay(b["board"], tid)
                time.sleep(10)
        except Exception as e:
            self.logger.error(e)

    def stop(self):
        self.run = False


if __name__ == "__main__":
    ChanMinner().start()
