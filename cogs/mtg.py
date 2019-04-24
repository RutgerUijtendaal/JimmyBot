#!user/local/bin/python3

from discord.ext import commands
from utils import web
import json


class MTG(commands.Cog):
    """MTG Card images"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mtg(self, ctx):
        """[search]. Get the closest matching MTG card"""
        ctx.view.skip_ws()
        search = ctx.view.read_rest()
        search = search.strip()
        search = search.replace(' ', '+')
        url = 'https://api.scryfall.com/cards/named?fuzzy=' + search

        response = await web.download_page(url)

        if not response:
            await ctx.send('Could not find any cards matching this search.')
            return

        card = json.loads(response)

        if card['object'] == 'error':
            return

        if card['object'] == 'card':
            await ctx.send(card['image_uris']['normal'])


def setup(bot):
    bot.add_cog(MTG(bot))
