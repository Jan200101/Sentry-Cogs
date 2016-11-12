import discord
from discord.ext import commands
from cogs.utils.chat_formatting import pagify
from cogs.utils.chat_formatting import box
from cogs.utils.chat_formatting import escape_mass_mentions

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

    @commands.command(pass_context=True, alias=["chaninfo"])
    async def channelinfo(self, ctx, channel : discord.Channel = None):
        """Shows channel informations"""
        author = ctx.message.channel
        server = ctx.message.server
        if not channel:
            channel = author

        data = "Name: {}\n".format(escape_mass_mentions(str(channel)))
        data += "ID: {}\n".format(channel.id)
        if "{}".format(channel.is_default)=="True":
            data += "Default Channel: Yes\n"
        else:
            data += "Default Channel: No\n"
        if channel.is_private == True:
            data += "Private: Yes\n"
        if "{}".format(channel.type)=="text":
            if channel.topic != "":
                data += """Topic:\n"{}"\n""".format(channel.topic)
        data += "Position: {}\n".format(channel.position)
        passed = (ctx.message.timestamp - channel.created_at).days
        data += "Created: {} ({} days ago)\n".format(channel.created_at, passed)
        data += "Type: {}\n".format(channel.type)
        if "{}".format(channel.type)=="voice":
            data += "Users: {}\n".format(len(channel.voice_members))
            data += "User limit: {}\n".format(channel.user_limit)
            data += "Bitrate: {}\n".format(channel.bitrate)
        for page in pagify(data, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, 'Prolog'))

    @commands.command(pass_context=True)
    async def userinfo(self, ctx, user : discord.Member = None):
        """Shows user informations"""
        author = ctx.message.author
        server = ctx.message.server
        if not user:
            user = author
        roles = [x.name for x in user.roles if x.name != "@everyone"]
        if not roles: roles = ["None"]

        data = "Name: {}\n".format(escape_mass_mentions(str(user)))
        data += "Nickname: {}\n".format(escape_mass_mentions(str(user.nick)))
        data += "ID: {}\n".format(user.id)
        data += "Status: {}\n".format(user.status)
        if user.game is None:
            pass
        elif user.game.url is None:
            data += "Playing: {}\n".format(escape_mass_mentions(str(user.game)))
        else:
            data += "Streaming: {} ({})\n".format(escape_mass_mentions(str(user.game)),
                                                      escape_mass_mentions(user.game.url))
        passed = (ctx.message.timestamp - user.created_at).days
        data += "Created: {} ({} days ago)\n".format(user.created_at, passed)
        joined_at = self.fetch_joined_at(user, server)
        passed = (ctx.message.timestamp - joined_at).days
        data += "Joined: {} ({} days ago)\n".format(joined_at, passed)
        data += "Roles: {}\n".format(", ".join(roles))
        data+= "AFK: {}\n".format(user.is_afk)
        if user.avatar_url != "":
            data += "Avatar:"
            for page in pagify(data, ["\n"], shorten_by=13, page_length=2000):
                await self.bot.say(box(page, 'Prolog'))

            await self.bot.say("{}".format(user.avatar_url))
        else:
            for page in pagify(data, ["\n"], shorten_by=13, page_length=2000):
                await self.bot.say(box(page, 'Prolog'))

    @commands.command(pass_context=True, no_pm=True)
    async def serverinfo(self, ctx):
        """Shows server informations"""
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
        data += "Emojis: {}\n".format(len(server.emojis))
        data += "Roles: {}\n".format(len(server.roles))
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

    def fetch_joined_at(self, user, server):
        """Just a replacement incase Im gonna merge it with general"""
        return user.joined_at

def setup(bot):
    n = Info(bot)
    bot.add_cog(n)
