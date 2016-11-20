import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.chat_formatting import box,  pagify
from random import choice, randint
import datetime

class say:
    """Makes the bot say things for you now with embeds"""

    def __init__(self, bot):
        self.bot = bot
        if self.bot.get_cog("Admin") != None:
            raise Exception("This Cog does not work with the Admin cog from Squid-Plugins")

    @commands.command(pass_context=True, no_pm=True, aliases=["opsay"])
    @checks.admin_or_permissions(administrator=True)
    async def adminsay(self, ctx, *, text):
        """Says Something as the bot without anyone knowing who wrote it"""
        try:
            await self.bot.delete_message(ctx.message)
        except:
            raise Exception("I do not have the permissions needed")
        for text in pagify(text, ["\n"]):
            await self.bot.say(text)

    @commands.command(pass_context=True, no_pm=True)
    async def say(self, ctx, *, text):
        """Says Something as the bot without the needs special rights"""

        auth = " (message by "
        auth += ctx.message.author.mention
        auth += ")"
        for text in pagify(text, ["\n"]):
            await self.bot.say(text + auth)

    @commands.command(pass_context=True, no_pm=True)
    async def embedsay(self, ctx, *, text : str):
        """Says Something as the bot without the needs special rights and in a embed"""

        created_at = ("Created on {}".format(ctx.message.timestamp.strftime("%d %b %Y %H:%M")))

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1,10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description="", colour=discord.Colour(value=colour))
        data.add_field(name=str(text), value=u"\u2063")
        data.set_footer(text=created_at)

        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name, url=ctx.message.author.avatar_url,
                            icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True, aliases=["embedopsay"])
    @checks.admin_or_permissions(administrator=True)
    async def embedadminsay(self, ctx, *, text):
        """Says Something as the bot without the needs special rights"""

        try:
            await self.bot.delete_message(ctx.message)
        except:
            raise Exception("I do not have the permissions needed")

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1,10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description="", colour=discord.Colour(value=colour))
        data.add_field(name=str(text), value=u"\u2063")

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

def setup(bot):
    bot.add_cog(say(bot))
