#!/usr/local/bin/python3

from random import randint
import itertools
import json

from bs4 import BeautifulSoup
from discord.ext import commands

from utils import web


class Image(commands.Cog):
    """Google Image Searcher"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def i(self, ctx):
        """[search]. Get the first Google Image result"""
        url = Image.build_url_from_view(ctx.view)
        page = await web.download_page(url)

        if not page:
            await ctx.send("Couldn't grab the requested page")
            return

        link = Image.get_image_link(page)

        if not link:
            await ctx.send("Page returned wasn't Google Images")
            return

        await ctx.send(link)

    @commands.command()
    async def ri(self, ctx):
        """[search]. Get a random Google Image result"""
        url = Image.build_url_from_view(ctx.view)
        page = await web.download_page(url)

        if not page:
            await ctx.send("Couldn't grab the requested page")
            return

        link = Image.get_image_link(page, random=True)

        if not link:
            await ctx.send("Page returned wasn't Google Images")
            return

        await ctx.send(link)

    @staticmethod
    def build_url_from_view(view):
        view.skip_ws()
        request = view.read_rest()
        search = request.replace(' ', '%20')
        url = 'https://www.google.com/search?q=' + search + \
            '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        return url

    @staticmethod
    def get_image_link(page, random=False):
        page.encode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        url_data = []
        img_class = soup.find_all("div", class_="rg_meta")
        for img in itertools.islice(img_class, 0, 10):
            img_string = img.string
            img_json = json.loads(img_string)
            url_data.append(img_json['ou'])

        if random:
            return url_data[randint(1, len(url_data)-1)]

        return url_data[0]


def setup(bot):
    bot.add_cog(Image(bot))
