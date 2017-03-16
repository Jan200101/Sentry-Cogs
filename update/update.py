import discord
import os
from time import sleep
from discord.ext import commands
from asyncio import wait_for
from cogs.utils import checks


class Update:
    """update bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def update(self):
        """Shows how many commits you are behind"""

        response = self.bot.loop.run_in_executor(None, self._update)
        result = await wait_for(response, timeout=20)

        try:
            await self.bot.say(embed=result)
        except discord.HTTPException:
            await self.bot.say("Could not embed")
        except:
            await self.bot.say("a error happend")

    def _update(self):
        await self.bot.say('This will get rid of any edits you havent saved. Continue ? (yes/no)')
        answer = await self.bot.wait_for_message(timeout=10, author=ctx.message.author)

        if answer.content.lower().strip() != 'yes':
            await self.bot.say('Canceling Update')
            return


        if os.name != 'nt':
            os.popen('LC_ALL=C')

        os.popen(r'git reset --hard')
        os.popen(r'git stash')

        sleep(1)

        os.popen(r'git pull')

        sleep(1)

        # checks if local is out of date, needs the fetch first
        status = os.popen(r'git status -uno').read().strip()

        if status.find("Your branch is up-to-date") != -1:
            behind = "Update successfull"
            color = discord.Colour.green()

        elif status.find("Your branch is behind") != -1:
            behind = "Update unsuccessfull"
            color = discord.Colour.red()

        else:
            behind = "Unable to check if out of date"  # just here in the worst case
            color = discord.Colour.orange()

        embed = discord.Embed(title=behind,
                              colour=color)

        return embed

def check_folder():
    if not os.path.exists(".git"):
        raise Exception(
            "\n\nYou did not clone red using git. Please return to the guide and follow its instructions\n")


def setup(bot):
    check_folder()
    n = Update(bot)
    bot.add_cog(n)
