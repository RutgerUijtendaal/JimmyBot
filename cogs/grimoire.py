#!/usr/local/bin/python3

import itertools

from bs4 import BeautifulSoup
from discord.ext import commands

from utils import web


class Grimoire(commands.Cog):
    """Grimoire Spell descriptions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def grim(self, ctx):
        """[search]. Get the full description for a spell on Grimoire"""
        url = Grimoire.build_url_from_view(ctx.view)
        page = await web.download_page(url)

        if not page:
            await ctx.send("That probably isn't a spell")
            return

        message = Grimoire.build_message_from_page(page)

        await ctx.send(message)

    @staticmethod
    def build_url_from_view(view):
        view.skip_ws()
        request = view.read_rest()
        search = request.replace(' ', '-')
        url = "https://thegrimoire.xyz/spells/" + search.lower()
        return url

    @staticmethod
    def build_message_from_page(page):
        # Prep the page, get the soup
        page = page.encode("windows-1252")
        soup = BeautifulSoup(page, 'lxml')
        message = []

        # Spell name
        spell_name = soup.find('h2')
        message.append("# " + spell_name.text)
        message.append("< " + "-" * 40 + " >")

        # Spell details
        spell_details_raw = soup.find("div", class_="four columns well")
        spell_details = spell_details_raw.find_all('p')
        for details in itertools.islice(spell_details, 0, len(spell_details) - 1):
            for strong_tag in details.find_all('strong'):
                message.append("[" + strong_tag.text + "]" +
                               "(" + strong_tag.next_sibling[2:] + ")")
        message.append("< " + "-" * 40 + " >")

        # Spell descriptions
        spell_descriptions_raw = soup.article
        spell_descriptions = spell_descriptions_raw.find_all(['p', 'ul'])
        for descriptions in spell_descriptions:
            message.append(descriptions.text)
        # Join all data and make sure it's not too long for a discord message (max 2000 char)
        message = "\n\n".join(message)
        message = "```md\n" + message[0:1980] + "```"
        return message


def setup(bot):
    bot.add_cog(Grimoire(bot))
