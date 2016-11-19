import discord
from discord.ext import commands
from .utils.chat_formatting import *
from random import choice
import datetime
import time


class Channelinfo:
    """Shows Channel infos."""

    def __init__(self, bot):
        self.bot = bot
        if self.bot.get_cog("Info") != None:
            raise Exception("This cog does not work with my Info cog")

        list = "{}".format([c.name for c in ctx.message.server.channels])
        for page in pagify(list, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, "Prolog"))


    @commands.command(pass_context=True, no_pm=True, alias=["chaninfo"])
    async def channelinfo(self, ctx, channel : discord.Channel = None):
        """Shows channel informations"""
        author = ctx.message.channel
        server = ctx.message.server

        if not channel:
            channel = author

        randnum = randint(1,10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        passed = (ctx.message.timestamp - channel.created_at).days
        created_at = ("Created on {} ({} days ago!)"
                      "".format(channel.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(description="Channel ID: " + channel.id, colour=discord.Colour(value=colour))
        if "{}".format(channel.is_default)=="True":
            data.add_field(name="Default Channel", value="Yes")
        else:
            data.add_field(name="Default Channel", value="No")
        data.add_field(name="Type", value=str(channel.type))
        data.add_field(name="Position", value=str(channel.position))
        if "{}".format(channel.type)=="voice":
            data.add_field(name="Users", value=len(channel.voice_members))
            data.add_field(name="User limit", value=str(channel.user_limit))
            data.add_field(name="Bitrate", value=str(channel.bitrate))
        elif "{}".format(channel.type)=="text":
            data.add_field(name="Topic", value=str(channel.topic), inline=False)
        if channel.is_private == True:
            data.add_field(name="Direct Message", value="yes", inline=False)

        data.set_footer(text=created_at)
        data.set_author(name=channel.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")


def setup(bot):
    bot.add_cog(Channelinfo(bot))
