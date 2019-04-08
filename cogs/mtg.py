#!user/local/bin/python3

from discord.ext import commands
from utils import web
import json


class MTG:
    """MTG Card images"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mtg(self, ctx):
        """[search]. Get the closest matching MTG card"""
        ctx.view.skip_ws()
        search = ctx.view.read_rest()
        search = search.strip()
        search = search.replace(' ', '+')
        url = 'https://api.scryfall.com/cards/named?fuzzy=' + search

        response = await web.download_page(url)

        if not response:
            await self.bot.send_message(ctx.message.channel, 'Could not find any cards matching this search.')
            return

        card = json.loads(response)

        if card['object'] == 'error':
            return

        if card['object'] == 'card':
            await self.bot.send_message(ctx.message.channel, card['image_uris']['normal'])


def setup(bot):
    bot.add_cog(MTG(bot))
