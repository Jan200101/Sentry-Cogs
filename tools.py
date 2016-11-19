import discord
from discord.ext import commands
from .utils.chat_formatting import pagify
from .utils.chat_formatting import box

class tools:
    """Shows user, channel and role lists to the user."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden="true", alias=["chanlist"])
    async def channellist(self, ctx):
        """Lists all Channels"""

        list = "{}".format([c.name for c in ctx.message.server.channels])
        for page in pagify(list, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, "Prolog"))

    @commands.command(pass_context=True, hidden="true")
    async def userlist(self, ctx):
        """Lists all Users"""

        list = "{}".format([m.name for m in ctx.message.server.members])
        for page in pagify(list, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, "Prolog"))


    @commands.command(pass_context=True, hidden="true")
    async def rolelist(self, ctx):
        """Lists all Roles"""

        list = "{}".format([r.name for r in ctx.message.server.role_hierarchy])
        for page in pagify(list, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, "Prolog"))


    @commands.command(pass_context=True, hidden="true")
    async def emojilistlist(self, ctx):
        """Lists all Emojis"""

        list = "{}".format([e.name for e in ctx.message.server.emojis])
        for page in pagify(list, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, "Prolog"))

def setup(bot):
    n = tools(bot)
    bot.add_cog(n)