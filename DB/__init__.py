__author__ = 'danielkershaw'
from pymongo import MongoClient
from datetime import datetime
from pprint import pprint


class DB:
    def __init__(self, database):

        self.client = MongoClient("148.88.19.38", 27017)
        self.db = self.client.reddit

        # Top 100 threads at the top of reddit and there indexes.
        self.threads = self.db.threads

        #Store for all the comments that are mined
        self.comments = self.db.comments
        self.comments.ensure_index('id', unique=True)

        #List of what currently in the messaging queue for comment mining
        self.mq = self.db.mq

        #list of history threads mined
        self.his_threads = self.db.his_threads
        self.his_threads.ensure_index('id', unique=True)

        #list of history threads mined
        self.stream_threads = self.db.stream_threads

    def get_from_history(self, limit=1):
        tmp = []
        for method_frame, properties, body in self.historic_channel.consume('historic_threads'):

            tmp.append(body)

            self.channel.basic_ack(method_frame.delivery_tag)

            if len(tmp) > 20:
                break;
            print body

        requeued_messages = self.channel.cancel()
        return tmp

    def get_from_channel(self, limit=1):
        tmp = []
        for method_frame, properties, body in self.channel.consume('comments'):

            tmp.append(body)

            self.channel.basic_ack(method_frame.delivery_tag)

            if len(tmp) > 20:
                break;
            print body

        requeued_messages = self.channel.cancel()
        return tmp

    def insert_thread(self, index, value):
        try:
            value["index"] = index
            value["mined_at"] = datetime.now().strftime("%c")
            if not self.is_in_mq(value["id"]):
                self.threads.insert(value)
        except Exception as x:
            print "{0} : Unexpected error DB.py-insert_thread: {1} id: {2}".format(datetime.now().strftime("%c"),
                                                                                   x.args, value["id"])

    def insert_histroic_thread(self, value):
        try:
            print "{0} : insert_histroic_thread {1}".format(datetime.now().strftime("%c"), value["id"])
            if not self.is_in_mq(value["id"]):
                print value["id"]
                self.add_to_queue(value["id"])
            self.his_threads.update({'id': value["id"]}, value, upsert=True)
        except Exception as x:
            print "{0} : Unexpected error DB.py-insert_histroic_thread: {1} id: {2}".format(
                datetime.now().strftime("%c"), x.args, value["id"])

    def insert_stream_thread(self, value):
        try:
            print "{0} : insert_stream_thread {1}".format(datetime.now().strftime("%c"), value["id"])
            tmp = self.is_in_mq(value["id"])
            if not tmp:
                self.add_to_queue(value["id"])
            tmptmp = self.stream_threads.update({'id': value["id"]}, value, upsert=True)
            return tmp
        except Exception as x:
            print "{0} : Unexpected error DB.py-insert_histroic_thread: {1} id: {2}".format(
                datetime.now().strftime("%c"), x.args, value["id"])
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

    def add_to_historic_queue(self, thread_id):
        try:
            print "{0} : add_to_historic_queue {1}".format(datetime.now().strftime("%c"), thread_id)
            self.historic_channel.basic_publish(exchange='',
                                                routing_key='historic_threads',
                                                body=thread_id)

        except Exception as x:
            self._init_RadbbitMQhis()
            self.add_to_historic_queue(thread_id)
            print "{0} : Unexpected error DB.py-add_to_historic_queue: {1} id: {2}".format(
                datetime.now().strftime("%c"), x, thread_id)

    def insert_comment(self, value):
        try:
            print "{0} : insert_comment {1}".format(datetime.now().strftime("%c"), value["id"])
            self.comments.update({'id': value['id']}, value, upsert=True)
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