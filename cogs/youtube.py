#!/usr/local/bin/python3

from random import randint
import itertools

import re

from discord.ext import commands

from utils import web


class Youtube:
    """Youtube Video Searcher"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def yt(self, ctx):
        """[search]. Get the first Youtube result"""
        url = Youtube.build_url_from_view(ctx.view)
        page = await web.download_page(url)

        if not page:
            await self.bot.say("Couldn't grab the requested page")
            return

        link = Youtube.get_youtube_link(page)

        if not link:
            await self.bot.say("Page returned wasn't Youtube")

        await self.bot.say(link)

    @commands.command(pass_context=True)
    async def ryt(self, ctx):
        """[search]. Get a random Youtube result"""
        url = Youtube.build_url_from_view(ctx.view)
        page = await web.download_page(url)

        if not page:
            await self.bot.say("Couldn't grab the requested page")
            return

        link = Youtube.get_youtube_link(page, random=True)

        if not link:
            await self.bot.say("Page returned wasn't Youtube")

        await self.bot.say(link)

    @staticmethod
    def build_url_from_view(view):
        view.skip_ws()
        request = view.read_rest()
        search = request.replace(' ', '+')
        url = 'https://www.youtube.com/results?search_query=' + search
        return url

    @staticmethod
    def get_youtube_link(page, random=False):
        page.encode('utf-8')
        url_data = []
        # Youtube builds pages dynamically from scripts so we're searching the scripts with regex
        search_results = re.findall(r'\"url\":\"\/watch\?v=(.{11})', page)
        for search_result in itertools.islice(search_results, 0, 10):
            url_data.append("http://www.youtube.com/watch?v=" + search_result)

        if random:
            return url_data[randint(1, len(url_data)-1)]

        return url_data[0]


def setup(bot):
    bot.add_cog(Youtube(bot))
