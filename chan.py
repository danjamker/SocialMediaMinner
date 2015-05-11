__author__ = 'danielkershaw'

from datetime import datetime
import urllib
import json
import time

import basc_py4chan

from ChanDB import ChanDB
from tasks import mineChan


class main:

    def __init__(self):
        self.run = True
        self.db = ChanDB()

    def start(self):
        try:
            url = "https://a.4cdn.org/boards.json"
            response = urllib.urlopen(url);
            data = json.loads(response.read())
            while self.run:
                for b in data["boards"]:
                    time.sleep(1)
                    board = basc_py4chan.Board(b["board"])
                    thread_ids = board.get_all_thread_ids()
                    for tid in thread_ids:
                        self.db.insert_to_mq(str(tid)+":"+str(b["board"]))
                        mineChan.delay(b["board"], tid)
                    time.sleep(10)
        except Exception as e:
            print "{0} : Unexpected error GetAllComment.py-start: {1}".format(datetime.now().strftime("%c"), e.args)

    def stop(self):
        self.run = False

if __name__ == "__main__":
    main().start()