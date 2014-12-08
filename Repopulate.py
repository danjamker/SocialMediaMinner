__author__ = 'danielkershaw'
from DB import DB
from pprint import pprint
from celeryTasks import mineThread
class main:

    def __init__(self):
        self.db = DB()
        self.run = True

    def start(self):
        for m in self.db.get_queue():
            pprint(m)
            mineThread.delay(m["id"])


if __name__ == "__main__":
    main().start()