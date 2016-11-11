from discord.ext import commands
from cogs.utils import checks
from cogs.utils.chat_formatting import pagify, box
from subprocess import check_output, os, CalledProcessError

class pip:
    """pip inside Discord"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def sudopip(self, *, command : str):
        """sudo pip inside Discord"""

        if os.name == "posix":
            pip = "sudo pip "
        elif os.name == "nt":
            raise Exception("Sudo does not exist on Windows")
        else:
            raise Exception("Sudo does not exist on this operating system")
        pip += command
        try:
            output = check_output(pip, shell=True)
        except CalledProcessError as e:
            output = e.output

        shell = output.decode('utf_8')
        if shell == "":
            shell = "No Output recieved from '{}'".format(command)

        for page in pagify(shell, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, 'Python'))

    @commands.command()
    @checks.is_owner()
    async def sudopip3(self, *, command : str):
        """sudo pip3 inside Discord"""

        if os.name == "posix":
            pip = "sudo pip3 "
        elif os.name == "nt":
            raise Exception("Sudo does not exist on Windows")
        else:
            raise Exception("Sudo does not exist on this operating system")
        pip += command
        try:
            output = check_output(pip, shell=True)
        except CalledProcessError as e:
            output = e.output

        shell = output.decode('utf_8')
        if shell == "":
            shell = "No Output recieved from '{}'".format(command)

        for page in pagify(shell, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, 'Python'))

    @commands.command()
    @checks.is_owner()
    async def pip(self, *, command : str):
        """pip inside Discord"""

        pip = "pip "
        pip += command
        try:
            output = check_output(pip, shell=True)
        except CalledProcessError as e:
            output = e.output

        shell = output.decode('utf_8')
        if shell == "":
            shell = "No Output recieved from '{}'".format(command)

        for page in pagify(shell, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, 'Python'))

    @commands.command()
    @checks.is_owner()
    async def pip3(self, *, command : str):
        """pip3 inside Discord"""

        pip = "pip3 "
        pip += command
        try:
            output = check_output(pip, shell=True)
        except CalledProcessError as e:
            output = e.output

        shell = output.decode('utf_8')
        if shell == "":
            shell = "No Output recieved from '{}'".format(command)

        for page in pagify(shell, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, 'Python'))

def setup(bot):
    n = pip(bot)
    bot.add_cog(n)
