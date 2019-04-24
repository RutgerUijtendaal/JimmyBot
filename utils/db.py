#!/usr/local/bin/python3

from threading import Thread
from queue import Queue
import logging

from discord.ext.commands.view import StringView

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from google.cloud.exceptions import Conflict

logger = logging.getLogger('firebase')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='firebase.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


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

        if message.guild.id not in self._server_cache:
            self.add_server(message.guild)

        self.add_message(message)

    def add_user(self, author):
        author_id = str(author.id)

        user_data = {
            "user_id": author_id,
            "user_name": author.name
        }

        # If user already exists ignore
        if self.firestore.collection('users').document(author_id).get().exists:
            return

        try:
            self.firestore.collection('users').add(
                document_data=user_data, document_id=author_id)
        except Conflict as e:
            logger.error(e)

        self._user_cache.append(author_id)

    def add_server(self, server):
        server_id = str(server.id)

        server_data = {
            "server_id": server_id,
            "server_name": server.name
        }

        # If server already exists ignore
        if self.firestore.collection('servers').document(server_id).get().exists:
            return

        try:
            self.firestore.collection('servers').add(
                document_data=server_data, document_id=server_id)
        except Conflict as e:
            logger.error(e)

        self._server_cache.append(server_id)

    def add_message(self, message):
        view = StringView(message.content)
        command = view.get_word()

        request_data = {
            "message_id": str(message.id),
            "user_id": str(message.author.id),
            "server_id": str(message.guild.id),
            "command": command,
            "content": view.read_rest(),
            "timestamp": message.created_at
        }

        try:
            self.firestore.collection('requests').add(document_data=request_data, document_id=str(message.id))
        except Conflict as e:
            logger.error(e)
