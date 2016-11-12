import discord
from discord.ext import commands
from cogs.utils.chat_formatting import pagify
from cogs.utils.chat_formatting import box
from cogs.utils.chat_formatting import escape_mass_mentions

class Channelinfo:
    """Shows Channel infos."""

    def __init__(self, bot):
        self.bot = bot
        if self.bot.get_cog("Info") != None:
            raise Exception("This cog does not work with my Info cog")

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

def setup(bot):
    bot.add_cog(Channelinfo(bot))
