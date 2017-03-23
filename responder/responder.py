import discord
from discord.ext import commands
from os import path, makedirs
from cogs.utils.dataIO import dataIO
from __main__ import send_cmd_help
from cogs.utils.chat_formatting import box
from cogs.utils import checks
from asyncio import sleep

__author__ = 'Sentry'


class Responder:
    """Let the bot responde to certain users with a set message"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/responder/settings.json')
        self.author = self.settings['user']
        self.message = self.settings['message']
        self.enabled = self.settings['enabled']
        self.timeout = self.settings['timeout']

    @commands.group(aliases=['responsesettings'], pass_context=True)
    @checks.admin()
    async def respondersettings(self, ctx):
        """Allows you to change settings of this cog"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @respondersettings.command(name='user', pass_context=True)
    @checks.admin()
    async def _user(self, ctx, user: discord.Member=None):
        """Set the users that can trigger the message"""

        if user is None:
            name = list(
                set([x.name for x in self.bot.get_all_members() if x.id in self.author]))
            await send_cmd_help(ctx)
            if name:
                userlist = ', '.join(name)
            else:
                userlist = "No one"
            await self.bot.say(box(userlist))
            return

        if user.bot:
            await self.bot.say('`Cannot add Bots`')
            return
        elif user.id in self.author:
            self.author.remove(user.id)
            await self.bot.say('`removed \'{}\'`'.format(user))
        else:
            self.author.append(user.id)
            await self.bot.say('`added \'{}\'`'.format(user))

        self.settings['user'] = self.author
        dataIO.save_json('data/responder/settings.json', self.settings)

    @respondersettings.command(name="message", pass_context=True)
    @checks.admin()
    async def _message(self, ctx, *, message: str=None):
        """Set the message"""

        if not message:
            message = box(
                "Current message is {}".format(self.message))
            await send_cmd_help(ctx)
        else:
            self.message = message
            self.settings['message'] = self.message
            dataIO.save_json('data/responder/settings.json', self.settings)
            message = '`Changed message to {} `'.format(
                self.message)
        await self.bot.say(message)

    @respondersettings.command(name="toggle")
    @checks.admin()
    async def _toggle(self):
        """Disable any response"""

        if self.enabled == True:
            self.enabled = False
            await self.bot.say('`disabled responder`')
        elif self.enabled == False:
            self.enabled = True
            await self.bot.say('`enabled responder`')
        else:
            self.enabled = True
            await self.bot.say('`enabled responder`')

        self.settings['enabled'] = self.enabled

        dataIO.save_json('data/responder/settings.json', self.settings)

    @respondersettings.command(name="timeout", pass_context=True)
    async def _timeout(self, ctx, time: int=None):
        """Set the amount of time passing before reacting again\n"""

        if -1 >= self.timeout:  # If statement incase someone removes it or sets it to 0
            self.timeout = 0

        if time == None:
            message = box(
                "Current max search result is {}".format(self.timeout))
            await send_cmd_help(ctx)
        elif time < 0:
            await self.bot.say('`Cannot set timeout lower then 0`')
            return
        else:
            self.timeout = time
            self.settings['timeout'] = self.timeout
            dataIO.save_json('data/responder/settings.json', self.settings)
            message = '`Changed timeout to {} `'.format(
                self.timeout)
        await self.bot.say(message)

    async def on_message(self, message):
        await sleep(self.timeout)
        if self.enabled == True:
            if message.author.id in self.author:
                for x in self.bot.settings.prefixes:
                    if not message.content.startswith(x):
                        if not message.author.bot:
                            await self.bot.send_message(message.channel, self.message)


def check_folder():
    if not path.exists("data/responder"):
        print("[Responder]Creating data/responder folder...")
        makedirs("data/responder")


def check_file():
    data = {}
    data['enabled'] = True
    data['timeout'] = 0
    data['user'] = []
    data['message'] = "Placeholder Message"
    f = "data/responder/settings.json"
    if not dataIO.is_valid_json(f):
        print("[Responder]Creating default settings.json...")
        dataIO.save_json(f, data)


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Responder(bot))
