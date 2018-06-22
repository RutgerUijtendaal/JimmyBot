#!/usr/local/bin/python3

from threading import Thread
from queue import Queue

from discord.ext.commands.view import StringView

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from google.cloud.exceptions import Conflict


class Database(Thread):

    def __init__(self):
        super().__init__(name="firebase")
        cred = credentials.Certificate('auth/admin_firebase.json')
        firebase_admin.initialize_app(cred)
        self.firestore = firestore.client()
        self._user_cache = []
        self._server_cache = []
        self.messages = Queue()
        self.start()

    def run(self):
        while True:
            message = self.messages.get()

            if message == '--close--':
                break

            self.handle_message(message)

    def close(self):
        self.messages.put('--close--')

    def add_message_to_queue(self, message):
        self.messages.put(message)

    def handle_message(self, message):
        if message.author.id not in self._user_cache:
            self.add_user(message.author)

        if message.server.id not in self._server_cache:
            self.add_server(message.server)

        self.add_message(message)

    def add_user(self, author):
        user_data = {
            "user_id": author.id,
            "user_name": author.name
        }

        try:
            self.firestore.collection('users').add(
                document_data=user_data, document_id=author.id)
        except Conflict as e:
            print(e)

        self._user_cache.append(author.id)

    def add_server(self, server):
        server_data = {
            "server_id": server.id,
            "server_name": server.name
        }

        try:
            self.firestore.collection('servers').add(
                document_data=server_data, document_id=server.id)
        except Conflict as e:
            print(e)

        self._server_cache.append(server.id)

    def add_message(self, message):
        view = StringView(message.content)
        command = view.get_word()

        request_data = {
            "message_id": message.id,
            "user_id": message.author.id,
            "server_id": message.server.id,
            "command": command,
            "content": view.read_rest(),
            "timestamp": message.timestamp
        }

        self.firestore.collection('requests').add(
            document_data=request_data, document_id=message.id)
