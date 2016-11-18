import discord
from discord.ext import commands
from .utils.chat_formatting import pagify
from .utils.chat_formatting import box
from random import choice
import datetime
import time

class Info:
    """Shows Client, Channel and Server infos to the user."""

    def __init__(self, bot):
        self.bot = bot
        if self.bot.get_cog("Channelinfo") != None:
            raise Exception("This cog does not work with my Channelinfo cog")


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

    @commands.command(pass_context=True, no_pm=True, alias=["chaninfo"])
    async def channelinfo(self, ctx, channel : discord.Channel = None):
        """Shows channel informations"""
        author = ctx.message.channel
        server = ctx.message.server

        if not channel:
            channel = author

        passed = (ctx.message.timestamp - channel.created_at).days
        created_at = ("Created on {} ({} days ago!)"
                      "".format(channel.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(description="ID: " + channel.id, colour=discord.Colour(value=colour))
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
            await self.bot.say(embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def userinfo(self, ctx, user: discord.Member=None):
        """Shows users's informations"""
        author = ctx.message.author
        server = ctx.message.server

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        joined_at = user.joined_at
        since_created = (ctx.message.timestamp - user.created_at).days
        since_joined = (ctx.message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        statususer = "{}".format(user.status)



        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description="User ID : " + user.id, colour=user.colour)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Status", value=statususer)
        if user.nick != None:
            data.add_field(name="Nickname", value=str(user.nick))
        data.add_field(name="Roles", value=roles, inline=False)
        if user.game != None:
            data.add_field(name="Playing", value=str(user.game))

        if user.avatar_url:
            data.set_author(name=user.name, url=user.avatar_url,
                            icon_url=user.avatar_url)
        else:
            data.set_author(name=user.name)

        try:
            await self.bot.say(embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        """Shows server's informations"""
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Created on {} ({} days ago!)"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(
            description="ID: " + server.id,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text=created_at)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url,
                            icon_url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await self.bot.say(embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfofull(self, ctx):
        """Shows server's full informations"""
        server = ctx.message.server
        online = str(len([m.status for m in server.members if str(m.status) == "online" or str(m.status) == "idle"]))
        total_users = str(len(server.members))
        text_channels = len([x for x in server.channels if str(x.type) == "text"])
        voice_channels = len(server.channels) - text_channels

        data = "Name: {}\n".format(server.name)
        data += "ID: {}\n".format(server.id)
        data += "Region: {}\n".format(server.region)
        data += "Users: {}/{}\n".format(online, total_users)
        data += "Text channels: {}\n".format(text_channels)
        data += "Voice channels: {}\n".format(voice_channels)
        data += "Channel names:\n{}\n".format([c.name for c in server.channels])
        data += "Emojis: {}\n{}\n".format(len(server.emojis), [e.name for e in server.emojis])
        data += "Roles: {} \n{}\n".format(len(server.roles), [r.name for r in server.role_hierarchy])
        passed = (ctx.message.timestamp - server.created_at).days
        data += "Created: {} ({} days ago)\n".format(server.created_at, passed)
        data += "Owner: {}\n".format(server.owner)
        if server.icon_url != "":
            data += "Icon:"
            for page in pagify(data, ["\n"], shorten_by=13, page_length=2000):
                await self.bot.say(box(page, 'Prolog'))

            await self.bot.say("{}".format(server.icon_url))
        else:
            for page in pagify(data, ["\n"], shorten_by=13, page_length=2000):
                await self.bot.say(box(page, 'Prolog'))

def setup(bot):
    n = Info(bot)
    bot.add_cog(n)
