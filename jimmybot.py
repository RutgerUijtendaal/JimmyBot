#!/usr/local/bin/python3

import logging

from discord.ext import commands
from discord.ext.commands.view import StringView

from utils.db import Database
import settings

logger = logging.getLogger('discord')


class Jimmybot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Database()

    async def close(self):
        self.db.close()
        logger.info('closing bot')
        await super().close()

    async def on_message(self, message):
        # If no prefix is found discard the message
        if not message.content.startswith(settings.PREFIX):
            return

        # If the message has a prefix but no known command we
        # convert the message to an !i command before passing it
        view = StringView(message.content)
        view.skip_string(settings.PREFIX)
        invoker = view.get_word()

        for command in self.commands:
            if invoker == command.name:
                break
        else:
            message.content = message.content[:1] + "i " + message.content[1:]

        # if invoker not in self.commands.name:
        #     message.content = message.content[:1] + "i " + message.content[1:]

        # Allow for the command to be processed by discord.py
        await self.process_commands(message)

        # Put the message in the database queue to be stored
        self.db.add_message_to_queue(message)
