import discord
from discord.ext import commands
from os import path, makedirs
from cogs.utils.dataIO import dataIO
from __main__ import send_cmd_help
from cogs.utils.chat_formatting import box
from cogs.utils import checks

class Responder:
    """Let the bot repeat a message to certain users"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/repeat/settings.json')
        self.author = self.settings['user']
        self.message = self.settings['message']

    @commands.group(pass_context=True)
    @checks.admin()
    async def responsesettings(self, ctx):
        """Allows you to change settings of this cog"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @responsesettings.command(name='user', pass_context=True)
    @checks.admin()
    async def _user(self, ctx, user:discord.Member=None):
        """Set the users that can trigger the message"""

        if user is None:
            await send_cmd_help(ctx)
            if self.author:
                list = ', '.join(self.author)
            else:
                list = "No one"
            await self.bot.say(box(list))
            return

        authors = self.author

        if user.id in authors:
            await self.bot.say('removed {}'.format(user))
            authors.remove(user.id)
        else:
            await self.bot.say('added {}'.format(user))
            authors.append(user.id)

        dataIO.save_json('data/repeat/settings.json', self.settings)

    @responsesettings.command(name="message", pass_context=True)
    @checks.admin()
    async def _message(self, ctx, *, message:str=None):
        """Set the message"""

        if not message:
            message = box(
                "Current message is {}".format(self.message))
            await send_cmd_help(ctx)
        else:
            self.message = message
            self.settings['message'] = self.message
            dataIO.save_json('data/repeat/settings.json', self.settings)
            message = '`Changed message to {} `'.format(
                self.message)
        await self.bot.say(message)

    async def on_message(self, message):
        if message.author.id in self.author:
            for x in self.bot.settings.prefixes:
                if not message.content.startswith(x):
                    if not message.author.bot:
                        await self.bot.send_message(message.channel, self.message)


def check_folder():  # Paddo is great
    if not path.exists("data/repeat"):
        print("[Repeat]Creating data/repeat folder...")
        makedirs("data/repeat")


def check_file():
    data = {}
    data['user'] = []
    data['message'] = "Placeholder Message"
    f = "data/repeat/settings.json"
    if not dataIO.is_valid_json(f):
        print("[Repeat]Creating default settings.json...")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Responder(bot))
