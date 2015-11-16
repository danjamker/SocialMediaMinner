__author__ = 'danielkershaw'
from pymongo import MongoClient
import pymongo
from datetime import datetime
import logging

class ChanDB:
    def __init__(self, connection_string):

        self.client = MongoClient(connection_string)
        self.db = self.client.chan

        #Store for all the comments that are mined
        self.thread = self.db.thread

        #List of what currently in the messaging queue for comment mining
        self.mq = self.db.mq

        #list of history threads mined
        self.board = self.db.board
        self.post = self.db.post
        self.post.create_index([("board_name", pymongo.TEXT),("thread_id", pymongo.DESCENDING),("post_id", pymongo.DESCENDING)], name="post index", unique=True)
        #Store for all the comments that are mined
        self.home = self.db.home

        self.logger = logging.getLogger('4 Chan Database')
        self.logger.info('Starting 4Chan database')


    def insert_board(self, json):
        self.board.insert_one(json)

    def insert_thread(self, json):
        self.thread.insert_one(json)

    def insert_home(self, json):
        self.home.insert_one(json)

    def is_in_mq(self, key):
        if self.mq.find({"key":key}).count() > 0:
            return True
        else:
            return False

    def insert_post(self, json):
        self.post.update({"board_name": json["board_name"], "":json["thread_id"], "":json["post_id"]}, json, upsert=True)

    def add_to_mq(self, key):
        self.mq.insert_one({"key":key})

    def remove_from_mq(self, key):
        self.mq.remove({"key":key})