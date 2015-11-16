__author__ = 'danielkershaw'
from pymongo import MongoClient
from datetime import datetime
import logging

class DB:

    def __init__(self, connection_string):

        self.client = MongoClient(connection_string)
        self.db = self.client.reddit

        # Top 100 threads at the top of reddit and there indexes.
        self.threads = self.db.threads

        #Store for all the comments that are mined
        self.comments = self.db.comments
        self.comments.create_index('id', unique=True)

        #List of what currently in the messaging queue for comment mining
        self.mq = self.db.mq

        #list of history threads mined
        self.his_threads = self.db.his_threads
        self.his_threads.create_index('id', unique=True)

        #list of history threads mined
        self.stream_threads = self.db.stream_threads
        self.logger = logging.getLogger('Reddit Database')
        self.logger.info('Starting Reddit Database')

    def get_from_history(self, limit=1):
        tmp = []
        for method_frame, properties, body in self.historic_channel.consume('historic_threads'):

            tmp.append(body)

            self.channel.basic_ack(method_frame.delivery_tag)

            if len(tmp) > 20:
                break;

        requeued_messages = self.channel.cancel()
        return tmp

    def get_from_channel(self, limit=1):
        tmp = []
        for method_frame, properties, body in self.channel.consume('comments'):

            tmp.append(body)

            self.channel.basic_ack(method_frame.delivery_tag)

            if len(tmp) > 20:
                break;

        requeued_messages = self.channel.cancel()
        return tmp

    def insert_thread(self, index, value):
        try:
            value["index"] = index
            value["mined_at"] = datetime.now().strftime("%c")
            if not self.is_in_mq(value["id"]):
                self.threads.insert(value)
        except Exception as x:
            self.logger.error(x)

    def insert_histroic_thread(self, value):
        try:
            if not self.is_in_mq(value["id"]):
                self.add_to_queue(value["id"])
            self.his_threads.update({'id': value["id"]}, value, upsert=True)
        except Exception as x:
            self.logger.error(x)


    def insert_stream_thread(self, value):
        try:
            tmp = self.is_in_mq(value["id"])
            if tmp == False:
                self.add_to_queue(value["id"])
            tmptmp = self.stream_threads.update({'id': value["id"]}, value, upsert=True)
            return tmp
        except Exception as x:
            self.logger.error(x)
            return False

    def add_to_queue(self, thread_id):
        try:
            t = "{0}".format(thread_id)
            self.in_queue(thread_id)
        except Exception as x:
            self.logger.error(x)

    def get_queue(self):
        try:
            return self.mq.find()
        except Exception as x:
            self.logger.error(x)


    def add_to_historic_queue(self, thread_id):
        try:
            self.historic_channel.basic_publish(exchange='',
                                                routing_key='historic_threads',
                                                body=thread_id)
        except Exception as x:
            self._init_RadbbitMQhis()
            self.add_to_historic_queue(thread_id)
            self.logger.error(x)

    def insert_comment(self, value):
        try:
            self.comments.update({'id': value['id']}, value, upsert=True)
        except Exception as x:
            self.logger.error(x)

    def is_in_mq(self, thread_id):
        try:
            if self.mq.find_one({'id': thread_id}) != None:
                return True
            else:
                return False
        except Exception as x:
            self.logger.error(x)

    def remove_from_queue(self, thread_id):
        try:
            self.mq.remove({'id': thread_id})
        except Exception as x:
            self.logger.error(x)

    def in_queue(self, thread_id):
        try:
            self.mq.update({'id': thread_id}, {'id': thread_id}, upsert=True)
        except Exception as x:
            self.logger.error(x)
