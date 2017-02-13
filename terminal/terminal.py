from discord.ext import commands
from cogs.utils import checks
from cogs.utils.chat_formatting import pagify, box
from subprocess import Popen, CalledProcessError, PIPE, STDOUT
from platform import system, release
from __main__ import settings
from os import name
import time


class Terminal:
    """Terminal inside Discord"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def os(self):
        """Displays your current Operating System"""

        await self.bot.say(box(system() + "\n" + release(), 'Bash'))

    @commands.command()
    @checks.is_owner()
    async def osname(self):
        """Displays your current Operating System name"""

        await self.bot.say(box(system(), 'Bash'))

    @commands.command(alias=["osver"])
    @checks.is_owner()
    async def osversion(self):
        """Displays your current Operating System version"""

        await self.bot.say(box(release(), 'Bash'))

    @commands.command(aliases=["cmd", "terminal"])
    @checks.is_owner()
    async def shell(self, *, command: str):
        """Terminal inside Discord"""

        # List of blocked commands
        # Keeping Blacklist and Whitelist for other usets
        # Make sure commands are in lowercase
        blacklist = []
        whitelist = []


        if command.find("&") != -1:
            command = command.split("&")[0]

        if whitelist:
            for x in whitelist:
                if command.lower().find(x) == -1:
                    await self.bot.say("'{}' is on the command whitelist".format(command))
                    return

        for x in blacklist:
            if command.lower().find(x) != -1:
                await self.bot.say("'{}' is on the command blacklist".format(command))
                return

        if command.lower().find("apt-get") != -1 and command.lower().find("-y") == -1:
            command = "{} -y".format(command)

        try:
            output = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT).communicate()[0]
            error = False
        except CalledProcessError as e:
            try:
                output = e.output
            except:
                output = b'a error has occured'
            error = True

        # Decode to unicode for full character support
        shell = output.decode('utf_8')

        if shell == "" and not error:
            # in the case no output is given but no error has happened
            return

        for page in pagify(shell, shorten_by=20):
            await self.bot.say(box(page, 'Prolog'))


def setup(bot):
    bot.add_cog(Terminal(bot))
