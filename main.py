#!/usr/local/bin/python3

import json
import asyncio

import settings
from jimmybot import Jimmybot

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

help_attrs = dict(hidden=True)


def load_auth():
    with open('auth/bot_auth.json') as data_file:
        return json.load(data_file)


def main():
    bot = Jimmybot(command_prefix=settings.PREFIX,
                   description=settings.DESCRIPTION,
                   pm_help=None,
                   help_attrs=help_attrs)
    auth = load_auth()
    discord_token = auth['discord_token']
    bot.client_id = auth['discord_client_id']

    for extension in settings.INITIAL_EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

    bot.run(discord_token)


if __name__ == "__main__":
    main()
