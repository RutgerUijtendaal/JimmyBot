#!/usr/local/bin/python3

import textwrap
import os

from discord.ext import commands
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


class IASIP:
    """IASIP card maker"""

    font = ImageFont.truetype(
        '/usr/share/fonts/truetype/freefont/Textile.ttf', 85)

    def __init__(self, bot):
        self.bot = bot
        IASIP.make_directory()

    @commands.command(pass_context=True)
    async def sunny(self, ctx):
        """[text]. Create a title card for IASIP."""
        text = IASIP.build_text_from_view(ctx.view)
        img = IASIP.build_image_from_text(text)

        path = "iasip/" + ctx.message.id + ".png"
        img.save(path)

        await self.bot.send_file(ctx.message.channel, path)

        img.close()

        os.remove(path)

    @classmethod
    def build_image_from_text(cls, text):
        MAX_W, MAX_H = 1920, 1080
        img = Image.new("RGBA", (MAX_W, MAX_H), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        para = textwrap.wrap(text, width=40)
        current_h, pad = 480, 10
        for line in para:
            w, h = draw.textsize(line, font=cls.font)
            draw.text(((MAX_W - w) / 2, current_h), line, font=cls.font)
            current_h += h + pad
        return img

    @staticmethod
    def build_text_from_view(view):
        view.skip_ws()
        request = view.read_rest()
        text = "\"" + request.lower().title() + "\""
        return text

    @staticmethod
    def make_directory():
        try:
            os.mkdir('iasip/')
        except Exception:
            pass


def setup(bot):
    bot.add_cog(IASIP(bot))
