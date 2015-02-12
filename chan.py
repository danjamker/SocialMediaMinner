__author__ = 'danielkershaw'
import praw
import Tools
from datetime import datetime
from ChanDB import ChanDB
import basc_py4chan
import urllib, json
#from celeryTasks import mineChan
import sys
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
                    board = basc_py4chan.Board(b["board"])
                    thread_ids = board.get_all_thread_ids()
                    for tid in thread_ids:
                        if self.db.insert_to_mq(str(tid)+":"+str(b["board"])) == False:
                            print "Adding!!!!!!!"
                            self.mineChan(b["board"], tid)



        except Exception as e:
            print "{0} : Unexpected error GetAllComment.py-start: {1}".format(datetime.now().strftime("%c"), e.args)

    def stop(self):
        self.run = False

    def mineChan(self, board, thread):
        try:
            db = ChanDB()

            url = "https://a.4cdn.org/"+str(board)+"/thread/"+str(thread)+".json"
            response = urllib.urlopen(url);
            data = json.loads(response.read())

            # information from the OP
            for pp in data["posts"]:
                pp["lancs_id"] = str(board)+":"+str(thread)+":"+str(pp["no"])
                db.insert_post(pp)
            db.remove_from_queue(str(thread)+":"+str(board))
        except Exception, e:
            print e
            print "{0} : Unexpected error celeryTasks.py-mineChan: {1} body: {2}".format(datetime.now().strftime("%c"), sys.exc_info()[0], board+":"+thread)
            raise
if __name__ == "__main__":
    main().start()