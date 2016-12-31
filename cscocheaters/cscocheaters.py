import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import box
from __main__ import send_cmd_help
import os

class cheaters:
    """Moderation tools."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/csco/cheaters/settings.json")

    @commands.command(pass_context=True, no_pm=True)
    async def cheater(self, ctx, cheaterid, *, cheatername :str):
        """
        Put cheaters onto display
        cheatedid is the cheaters SteamID (steamID3 or steamID64 wont work adding support to it soon)
        cheatername is a alias for the cheater
        """

        if not cheaterid.startswith("STEAM_")
            await self.bot.say("{} is not a normal steamID".format(cheaterid))
        cheater = discord.Embed(color=discord.Colour.red())

        cheater.add_field(name="Cheater", value = "Name {}\nID {}\n\n".format(cheatername, cheaterid), inline=False)
        cheater.add_field(name="Markes as cheater by", value="{}".format(ctx.message.author), inline=False)
        cheater.set_footer(text=ctx.message.timestamp)

        channel = discord.utils.get(self.bot.get_all_channels(), id=self.settings['CHANNEL_ID'])

        if not channel:
            await self.bot.say(box("No Channel was set\nUse [p]cheaterchannel <channel> to set a channel"))
            return
        await self.bot.send_message(channel, embed=cheater)

    @commands.command(no_pm=True, pass_context=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def cheaterchannel(self, ctx, channel: discord.Channel=None):  # Also by Paddo
        """
        Set the channel to which the bot will sent cheaters.
        """
        if channel:
            self.settings['CHANNEL_ID'] = str(channel.id)
            dataIO.save_json('data/playtest/settings.json', self.settings)
            message = 'Channel set to {}'.format(channel.mention)
        elif not self.settings['CHANNEL_ID']:
            message = box("No Channel set")
            await send_cmd_help(ctx)
        else:
            channel = discord.utils.get(
                self.bot.get_all_channels(), id=self.settings['CHANNEL_ID'])
            if channel:
                message = box('Current channel is #{}'.format(channel))
                await send_cmd_help(ctx)
            else:
                self.settings['CHANNEL_ID'] = None
                message = box("No Channel set")
                await send_cmd_help(ctx)

        await self.bot.say(message)

def check_folder():  # Paddo is great
    if not os.path.exists("data/csco"):
        print("Creating data/csco folder...")
        os.makedirs("data/csco")

    if not os.path.exists("data/csco/cheaters"):
        print("Creating data/csco/cheaters folder...")
        os.makedirs("data/csco/cheaters")

def check_file():
    data = {}
    data['CHANNEL_ID'] = ''
    f = "data/csco/cheaters/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default settings.json...")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    n = cheaters(bot)
    bot.add_cog(n)
