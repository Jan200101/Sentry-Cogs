import discord
from discord.ext import commands
from .utils.chat_formatting import pagify, box
from random import choice, randint
import datetime
import time


class Info:
    """Shows Client, Channel and Server infos to the user."""

    def __init__(self, bot):
        self.bot = bot
        if self.bot.get_cog("Channelinfo") != None:
            raise Exception("This cog does not work with my Channelinfo cog")

        elif self.bot.get_cog("General") != None:
            raise Exception("This cog does not work with the General cog")

    @commands.command(pass_context=True, no_pm=True)
    async def channelinfo(self, ctx, channel: discord.Channel=None):
        """Shows channel informations"""
        author = ctx.message.channel
        server = ctx.message.server

        if not channel:
            channel = author

        userlist = [r.display_name for r in channel.voice_members]
        if userlist == []:
            userlist = None
        else:
            userlist = ", ".join(userlist)

        passed = (ctx.message.timestamp - channel.created_at).days
        created_at = ("Created on {} ({} days ago!)"
                      "".format(channel.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(description="Channel ID: " +
                             channel.id, colour=discord.Colour(value=colour))
        if "{}".format(channel.is_default) == "True":
            data.add_field(name="Default Channel", value="Yes")
        else:
            data.add_field(name="Default Channel", value="No")
        data.add_field(name="Type", value=channel.type)
        data.add_field(name="Position", value=channel.position)
        if "{}".format(channel.type) == "voice":
            if channel.user_limit != 0:
                data.add_field(
                    name="User Number", value="{}/{}".format(len(channel.voice_members), channel.user_limit))
            else:
                data.add_field(name="User Number", value="{}".format(
                    len(channel.voice_members)))
            data.add_field(name="Users", value=userlist)
            data.add_field(name="Bitrate", value=channel.bitrate)
        elif "{}".format(channel.type) == "text":
            if channel.topic != "":
                data.add_field(name="Topic", value=channel.topic, inline=False)

        data.set_footer(text=created_at)
        data.set_author(name=channel.name)

        try:
            await self.bot.say(emptyrand, embed=data)
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

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        joined_at = user.joined_at
        since_created = (ctx.message.timestamp - user.created_at).days
        since_joined = (ctx.message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")

        created_on = "{}\n({} days go)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        statususer = "{}".format(user.status)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        if user.bot == False:
            data = discord.Embed(description="User ID : " +
                                 user.id, colour=user.colour)
        elif author.is_afk == True:
            data = discord.Embed(description="AFK | User ID : " +
                                 user.id, colour=user.colour)
        else:
            data = discord.Embed(
                description="Bot | User ID : " + user.id, colour=user.colour)

        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Status", value=statususer)
        if user.nick != None:
            data.add_field(name="Nickname", value=str(user.nick))
        if user.game != None:
            data.add_field(name="Playing", value=str(user.game))
        data.add_field(name="Roles", value=roles, inline=False)
        if user.avatar_url:
            data.set_author(name=user.name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=user.name, url=user.default_avatar_url)
            data.set_thumbnail(url=user.default_avatar_url)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx, server=None):
        """Shows server's informations"""

        server = self.bot.get_server(server)
        if server is None:
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

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        data = discord.Embed(
            description="Server ID: " + server.id,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text=created_at)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def getserverinvite(self, ctx):
        """Get a invite to the current server"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        invite = await self.bot.create_invite(ctx.message.server)
        server = ctx.message.server

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(
            colour=discord.Colour(value=colour))
        data.add_field(name=server.name, value=invite, inline=False)

        if server.icon_url:
            data.set_thumbnail(url=server.icon_url)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True, aliases=["getbotinvite"])
    async def getinvite(self, ctx):
        """Get a invite to the bot"""

        invite = self.bot.oauth_url
        server = ctx.message.server

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(
            colour=server.me.colour)
        data.add_field(name="{} #{}".format(server.me.name, server.me.discriminator), value=invite, inline=False)

        if server.me.avatar_url:
            data.set_thumbnail(url=server.me.avatar_url)
        else:
            data.set_thumbnail(url=server.me.default_avatar_url)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")


def setup(bot):
    n = Info(bot)
    bot.add_cog(n)
