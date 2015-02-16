__author__ = 'danielkershaw'
from ChanDB import ChanDB
from pprint import pprint
from celeryTasks import mineChan
class main:

    def __init__(self):
        self.db = ChanDB()
        self.run = True

    def start(self):
        for m in self.db.get_queue():
            pprint(m)
            mineChan.delay(m["id"])


if __name__ == "__main__":
    main().start()