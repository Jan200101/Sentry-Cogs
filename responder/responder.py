import discord
from discord.ext import commands
from os import path, makedirs
from cogs.utils.dataIO import dataIO
from __main__ import send_cmd_help
from cogs.utils.chat_formatting import box
from cogs.utils import checks

__author__ = 'Sentry'

class Responder:
    """Let the bot repeat a message to certain users"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/repeat/settings.json')
        self.author = self.settings['user']
        self.message = self.settings['message']
        self.enabled = self.settings['enabled']

    @commands.group(aliases=['responsesettings'], pass_context=True)
    @checks.admin()
    async def respondersettings(self, ctx):
        """Allows you to change settings of this cog"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @respondersettings.command(name='user', pass_context=True)
    @checks.admin()
    async def _user(self, ctx, user:discord.Member=None):
        """Set the users that can trigger the message"""

        if user is None:
            name = list(set([x.name for x in self.bot.get_all_members() if x.id in self.author]))
            await send_cmd_help(ctx)
            if name:
                userlist = ', '.join(name)
            else:
                userlist = "No one"
            await self.bot.say(box(userlist))
            return

        authors = self.author

        if user.bot:
            await self.bot.say('`Cannot add Bots`')
            return
        elif user.id in authors:
            authors.remove(user.id)
            await self.bot.say('`removed \'{}\'`'.format(user))
        else:
            authors.append(user.id)
            await self.bot.say('`added \'{}\'`'.format(user))

        dataIO.save_json('data/repeat/settings.json', self.settings)

    @respondersettings.command(name="message", pass_context=True)
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

    @respondersettings.command(name="toggle", pass_context=True)
    @checks.admin()
    async def _toggle(self, ctx):

        if self.enabled == True:
            self.enabled = False
            await self.bot.say('`disabled responder`')
        elif self.enabled == False:
            self.enabled = True
            await self.bot.say('`enabled responder`')
        else:
            self.enabled = True
            await self.bot.say('`enabled responder`')

        dataIO.save_json('data/repeat/settings.json', self.settings)

    async def on_message(self, message):
        if self.enabled == True:
            if message.author.id in self.author:
                for x in self.bot.settings.prefixes:
                    if not message.content.startswith(x):
                        if not message.author.bot:
                            await self.bot.send_message(message.channel, self.message)


def check_folder():
    if not path.exists("data/repeat"):
        print("[Repeat]Creating data/repeat folder...")
        makedirs("data/repeat")


def check_file():
    data = {}
    data['enabled'] = True
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
