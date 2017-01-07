from discord.ext import commands
from cogs.utils import checks
import time
import sys
import subprocess
import os


class restart:
    """Cog to restart the bot without the need of any special tools."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def ttest(self, ctx):

        await self.bot.say("This is `oldrestart`\n{}".format(oldrestart))

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def restart(self, ctx):
        """Restarts the bot"""

        await self.bot.say("Do you really want to restart? (yes/no)")
        answer = await self.bot.wait_for_message(timeout=10,
                                                 author=ctx.message.author)

        if answer == None:
            await self.bot.say("Canceling restart...")

        elif answer.content.lower().strip() == "yes":
            await self.bot.say("Restarting now.")
            print("Restarting Red...")
            time.sleep(1)
            cd = "{}/{}".format(os.getcwd(), sys.argv[0])
            child = subprocess.Popen(["{} {}".format(sys.executable, cd)],shell=True,stdout=subprocess.PIPE)
            output,error = child.communicate()
            print("Output\n{}\nError\n{}\n".format(output, error))
            sys.exit()

        else:
            await self.bot.say("Canceling restart...")

def __unload(self):
    print("This shows you didnt screw up. Hooray")

def setup(bot):

    global oldrestart
    oldrestart = bot.get_command("restart")

    if oldrestart:
        bot.remove_command(oldrestart.name)

    bot.say("Beep Boop, Load")
    n = restart(bot)
    bot.add_cog(n)
