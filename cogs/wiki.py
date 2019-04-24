#!/usr/local/bin/python3

import wikipedia
import discord
from discord.ext import commands


class Wiki(commands.Cog):
    """Wiki Articles"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wiki(self, ctx):
        """[search]. Summerize and embed the Wiki article"""
        ctx.view.skip_ws()
        search = ctx.view.read_rest()

        try:
            wiki_page = wikipedia.page(search)
        except wikipedia.exceptions.DisambiguationError as e:
            await ctx.send("Ambiguous request, grabbing '" + e.options[0] + "' instead.")
            wiki_page = wikipedia.page(e.options[0])
        except Exception:
            await ctx.send("Failed to grab article")

        if wiki_page:
            embed = discord.Embed(title=wiki_page.title,
                                  url=wiki_page.url, colour=0xFF1493)
            embed.set_thumbnail(url=wiki_page.images[0])
            embed.add_field(name="Summary", value=wiki_page.summary[0:1000])
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Wiki(bot))
