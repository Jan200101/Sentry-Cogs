import discord
from discord.ext import commands
from .utils.chat_formatting import pagify, box
from .utils import checks


class tools:
    """Shows user, channel and role lists to the user."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden="true", alias=["chanlist"])
    @checks.is_owner()
    async def channellist(self, ctx):
        """Lists all Channels"""

        list = ", ".join([c.name for c in ctx.message.server.channels])
        for page in pagify(list, ["\n"], shorten_by=7, page_length=2000):
            await self.bot.say(box(page))

    @commands.command(pass_context=True, hidden="true")
    @checks.is_owner()
    async def voicechannellist(self, ctx):
        """Lists all voice Channels"""

        list = ", ".join(
            [c.name for c in ctx.message.server.channels if c.type == discord.ChannelType.voice])
        for page in pagify(list, ["\n"], shorten_by=7, page_length=2000):
            await self.bot.say(box(page))

    @commands.command(pass_context=True, hidden="true")
    @checks.is_owner()
    async def textchannellist(self, ctx):
        """Lists all text Channels"""

        list = ", ".join(
            [c.name for c in ctx.message.server.channels if c.type == discord.ChannelType.text])
        for page in pagify(list, ["\n"], shorten_by=7, page_length=2000):
            await self.bot.say(box(page))

    @commands.command(pass_context=True, hidden="true")
    @checks.is_owner()
    async def userlist(self, ctx):
        """Lists all Users"""

        list = ", ".join([m.name for m in ctx.message.server.members])
        for page in pagify(list, ["\n"], shorten_by=7, page_length=2000):
            await self.bot.say(box(page))

    @commands.command(pass_context=True, hidden="true")
    @checks.is_owner()
    async def rolelist(self, ctx):
        """Lists all Roles"""

        list = ", ".join(
            [x.name for x in ctx.message.server.role_hierarchy if x.name != "@everyone"])
        for page in pagify(list, ["\n"], shorten_by=7, page_length=2000):
            await self.bot.say(box(page))

    @commands.command(pass_context=True, hidden="true")
    @checks.is_owner()
    async def emojilist(self, ctx):
        """Lists all Emojis"""

        x = -1
        l =  []
        while x < len([r for r in self.bot.get_all_emojis()]) -1:
            x = x + 1
            l.append("<:{}:{}>".format([r for r in self.bot.get_all_emojis()][x].name, [r for r in self.bot.get_all_emojis()][x].id))

        l = " ".join(l)
        for page in pagify(l, ["\n"], shorten_by=7, page_length=2000):
            await self.bot.say(page)

    @commands.command(pass_context=True, hidden="true")
    @checks.is_owner()
    async def banlist(self, ctx):
        """Lists all banned users"""
        x = None

        try:
            x = await self.bot.get_bans(ctx.message.server)
        except discord.HTTPException:
            await self.bot.say("I need the `Ban Members` permission to do this")
            return
        except:
            await self.bot.say("Unkown error")
            return

        if x:
            list = ", ".join(x)
        else:
            list = "None"
        for page in pagify(list, ["\n"], shorten_by=7, page_length=2000):
            await self.bot.say(box(page))


def setup(bot):
    n = tools(bot)
    bot.add_cog(n)
