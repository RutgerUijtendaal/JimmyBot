#!/usr/local/bin/python3

import re

from bs4 import BeautifulSoup
from discord.ext import commands
from utils import web


class MonsterHunter:
    """Monster Hunter Skill list"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mh(self, ctx):
        """[search]. Get the full description for a spell in Monsterhunter"""
        url = MonsterHunter.build_link_from_view(ctx.view)
        page = await web.download_page(url)

        if not page:
            await self.bot.say("Couldn't grab the requested page")
            return

        message = MonsterHunter.build_message_from_page(page)

        await self.bot.say(message)

    @staticmethod
    def build_link_from_view(view):
        view.skip_ws()
        request = view.read_rest()
        search = request.replace(' ', '-')
        search = search.lower()
        url = "https://mhworld.kiranico.com/skill/" + search
        return url

    @staticmethod
    def build_message_from_page(page):
        page = page.encode("windows-1252")
        soup = BeautifulSoup(page, 'lxml')
        message = []

        # Get the title
        title = soup.find('h1')
        message.append("# " + title.text)
        effect = soup.find('p', class_="lead")
        # MH site is bad so we gotta get rid of useless whitespaces
        message.append(re.sub(' +', ' ', effect.text))
        message.append("< " + "-" * 40 + " >")

        # Get the shit it does
        body = soup.find('table', class_="table table-sm")
        rowCount = 0
        text = "# "
        for row in body.findAll('td'):
            if rowCount % 2 == 0:
                text += row.text
            else:
                text = text + "\n" + row.text
                message.append(text)
                text = "# "
            rowCount += 1

        # Make it into a proper message
        message = "\n\n".join(message)
        message = "```md\n" + message[0:1980] + "```"
        return message


def setup(bot):
    bot.add_cog(MonsterHunter(bot))
