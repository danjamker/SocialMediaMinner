__author__ = 'danielkershaw'
from pymongo import MongoClient
from datetime import datetime
from pprint import pprint


class ChanDB:
    def __init__(self):

        self.client = MongoClient("148.88.19.38", 27017)
        self.db = self.client.chan

        #Store for all the comments that are mined
        self.post = self.db.post
        self.post.ensure_index('lancs_id', unique=True)

        #List of what currently in the messaging queue for comment mining
        self.mq = self.db.mq

        #list of history threads mined
        self.board = self.db.board
        self.board.ensure_index('id', unique=True)

        #Store for all the comments that are mined
        self.thread = self.db.thread
        self.thread.ensure_index('id', unique=True)


    def insert_post(self, value):
        try:
            print "{0} : insert_comment {1}".format(datetime.now().strftime("%c"), value["lancs_id"])
            self.post.update({'lancs_id': value["lancs_id"]}, value, upsert=True)
        except Exception as x:
            print "{0} : Unexpected error DB.py-insert_comment: {1} id: {2}".format(datetime.now().strftime("%c"),
                                                                                    x.args, value["id"])

    def is_in_mq(self, thread_id):
        try:
            if self.mq.find_one({'id': thread_id}) != None:
                print "{0} : {1} is in queue".format(datetime.now().strftime("%c"), thread_id)
                return True
            else:
                print "{0} : {1} is not in queue".format(datetime.now().strftime("%c"), thread_id)
                return False
        except Exception as x:
            print "{0} : Unexpected error DB.py-is_in_mq: {1} id: {2}".format(datetime.now().strftime("%c"), x.args,
                                                                              thread_id)

    def remove_from_queue(self, thread_id):
        try:
            self.mq.remove({'id': thread_id})
        except Exception as x:
            print "{0} : Unexpected error DB.py-remove_from_queue: {1} id: {2}".format(datetime.now().strftime("%c"),
                                                                                       x.args, thread_id)

    def in_queue(self, thread_id):
        try:
            self.mq.update({'id': thread_id}, {'id': thread_id}, upsert=True)
        except Exception as x:
            print "{0} : Unexpected error DB.py-in_queue: {1} id: {2}".format(datetime.now().strftime("%c"), x.args,
                                                                              thread_id)

    def insert_to_mq(self, value):
        try:
            print "{0} : insert_stream_thread {1}".format(datetime.now().strftime("%c"), value)
            tmp = self.is_in_mq(value)
            if not tmp:
                self.add_to_queue(value)
            return tmp
        except Exception as x:
            print "{0} : Unexpected error DB.py-insert_histroic_thread: {1} id: {2}".format(
                datetime.now().strftime("%c"), x.args, value)
            return False

    def add_to_queue(self, thread_id):
        try:
            print "{0} : add_to_queue {1}".format(datetime.now().strftime("%c"), thread_id)
            t = "{0}".format(thread_id)
            self.in_queue(thread_id)
        except Exception as x:
            print "{0} : Unexpected error DB.py-add_to_queue: {1} id: {2}".format(datetime.now().strftime("%c"), x.args)

    def get_queue(self):
        try:
            return self.mq.find()
        except Exception, e:
            print "{0} : Unexpected error DB.py-add_to_queue: {1}".format(datetime.now().strftime("%c"))

    def in_queue(self, thread_id):
        try:
            self.mq.update({'id': thread_id}, {'id': thread_id}, upsert=True)
        except Exception as x:
            print "{0} : Unexpected error DB.py-in_queue: {1} id: {2}".format(datetime.now().strftime("%c"), x.args,
                                                                              thread_id)