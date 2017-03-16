import discord
import os
from time import sleep
from discord.ext import commands
from asyncio import wait_for
from requests import get


class UpdateStatus:
    """See infos about your current red installation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def behind(self):
        """Shows how many commits you are behind"""

        response = self.bot.loop.run_in_executor(None, self._get_behind)
        result = await wait_for(response, timeout=20)

        try:
            await self.bot.say(embed=result)
        except discord.HTTPException:
            await self.bot.say("Could not embed")
        except:
            await self.bot.say("a error happend")

    @commands.command(aliases=["travis-ci"], hidden=True)
    async def travis(self):
        """Shows travis status of your reds installation"""
        response = self.bot.loop.run_in_executor(None, self._get_travis)
        result = await wait_for(response, timeout=20)

        try:
            await self.bot.say(embed=result)
        except discord.HTTPException:
            await self.bot.say("Could not embed")
        except:
            await self.bot.say("a error happend")


    @commands.command(pass_context=True)
    @checks.is_owner()
    async def update(self, ctx):
        """Shows how many commits you are behind"""

        await self.bot.say('This will get rid of any edits you havent saved. Continue ? (yes/no)')
        answer = await self.bot.wait_for_message(timeout=10, author=ctx.message.author)

        if answer == None:
            await self.bot.say('Canceling Update')
            return
        elif answer.content.lower().strip() != 'yes':
            await self.bot.say('Canceling Update')
            return

        response = self.bot.loop.run_in_executor(None, self._update)
        result = await wait_for(response, timeout=20)

        await self.bot.say(embed=result)

    def _get_behind(self):

        if os.name != 'nt':
            os.popen('LC_ALL=C')

        os.popen(r'git fetch')

        sleep(1)

        # checks if local is out of date, needs the fetch first
        status = os.popen(r'git status -uno').read().strip()

        if status.find("Your branch is up-to-date") != -1:
            behind = "Your bot is up to date"
            color = discord.Colour.green()

        elif status.find("Your branch is behind") != -1:
            behind = "Your bot is out of date by {} commits".format(
                "".join([str(s) for s in status.split() if s.isdigit()]))  # finds the number of commits behind and adds it
            color = discord.Colour.red()

        else:
            behind = "Unable to check if out of date"  # just here in the worst case
            color = discord.Colour.orange()

        embed = discord.Embed(title=behind,
                              colour=color)

        return embed

    def _get_travis(self):

        if os.name != 'nt':
            os.popen('LC_ALL=C')

        branch = os.popen(r'git rev-parse --abbrev-ref HEAD')
        branch = branch.read().strip()

        allbranches = os.popen(r'git branch')
        allbranches = allbranches.read().strip()

        url = os.popen(r'git config --get remote.origin.url')
        url = url.read().strip()
        if url.endswith(".git"):
            url = url[:-4]

        # formats the url and branch together to get the branches repo link
        branchurl = "{}/tree/{}".format(url, branch)

        repo_name = url.split("/")[-1]

        author_name = url.split("/")[-2]

        # sees if the branch currently in use is the default branch
        if allbranches.find("* " + branch) != -1:
            defaultbranch = True
        else:
            defaultbranch = False

        # generates the travis status image based on repo and branch
        travisbuildstatus = "{}.png?branch={}".format(
            url.replace("github.com", "api.travis-ci.org"), branch)

        if defaultbranch:
            embed = discord.Embed(title="travis-ci build status of {} by {}".format(repo_name, author_name),
                                  colour=discord.Colour.orange(),
                                  url=branchurl)
        else:

            embed = discord.Embed(title="travis-ci build status of {} in {} by {}".format(branch, repo_name, author_name),
                                  colour=discord.Colour.orange(),
                                  url=branchurl)

        # makes a quick test if the image is even accessable if not gives out a
        # error
        request = get(travisbuildstatus)
        if request.status_code == 200:
            embed.set_image(url=travisbuildstatus)
        else:
            embed.add_field(
                name="Could not reach travis page of", value=str(repo_name))

        return embed

    def _update(self):

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
    n = UpdateStatus(bot)
    bot.add_cog(n)
