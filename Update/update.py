import discord
from os import popen
from time import sleep
from discord.ext import commands
from asyncio import wait_for
from cogs.utils import checks


class Update: #thanke sentrie
    """update bot :ok_hand:\nIdea by WreckRox"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @checks.is_owner()
    async def update(self):
        """xd"""

        response = self.bot.loop.run_in_executor(None, self._get_update)
        result = await wait_for(response, timeout=20)

        if not result:
            return

        try:
            await self.bot.say(embed=result)
        except discord.HTTPException:
            await self.bot.say("Could not embed")
        except:
            await self.bot.say("a error happend")

    def _get_update(self):

        popen(r'LC_ALL=C git fetch')
        popen(r'LC_ALL=C git pull')

        sleep(1)

        status = popen(r'LC_ALL=C git status -uno').read().strip()

        if status.find("Changes not staged") != -1:
            await self.bot.say('```There are unstaged changes.\nScrap them ?```')
            answer = await self.bot.wait_for_message(timeout=10, author=ctx.message.author)

            if answer.content.lower().strip() == 'yes':
                popen(r'LC_ALL=C git stash')
                popen(r'LC_ALL=C git pull')

                sleep(1)

                status = popen(r'LC_ALL=C git status -uno').read().strip()

                if status.find("Your branch is up-to-date") != -1:
                    behind = "Update successfull"
                    color = discord.Colour.green()

                else status.find("Your branch is behind") != -1:
                    behind = "Update unsuccessfull"
                    color = discord.Colour.red()
            else:
                await self.bot.say('Returning')
                return None


        elif status.find("Your branch is up-to-date") != -1:
            behind = "Update successfull"
            color = discord.Colour.green()

        elif status.find("Your branch is behind") != -1:

        else:
            behind = "Unable to update"  # just here in the worst case
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
