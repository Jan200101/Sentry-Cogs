import discord
import os
from discord.ext import commands
import asyncio
import requests

if not os.path.isdir(".s"):
    gitexist = False
else:
    gitexist = True

class status:
    """See infos about your current red installation"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def behind(self):
        """Shows how many commits you are behind"""
        response = self.bot.loop.run_in_executor(None, self._get_behind)
        result = await asyncio.wait_for(response, timeout=20)

        try:
            await self.bot.say(embed=result)
        except discord.HTTPException:
            await self.bot.say("Could not embed")
        except:
            await self.bot.say("a error happend")

    @commands.command(aliases=["travis-ci"])
    async def travis(self):
        """Shows travis status of your reds installation"""
        response = self.bot.loop.run_in_executor(None, self._get_travis)
        result = await asyncio.wait_for(response, timeout=20)

        try:
            await self.bot.say(embed=result)
        except discord.HTTPException:
            await self.bot.say("Could not embed")
        except:
            await self.bot.say("a error happend")

    def _get_behind(self):

        branch = os.popen(r'git rev-parse --abbrev-ref HEAD')
        branch = branch.read().strip()

        os.popen(r'git fetch')

        # checks if local is out of date, needs the fetch first
        status = os.popen(r'git status -uno')
        status = status.read().strip()

        if status.find("Your branch is up-to-date") != -1:
            behind = "Your bot is up to date"
            color = discord.Colour.green()

        elif status.find("Your branch is behind") != -1:
            behind = "Your bot is out of date by {} commits".format(
                "".join([str(s) for s in status.split() if s.isdigit()])) # finds the number of commits behind and adds it
            color = discord.Colour.red()

        else:
            behind = "Unable to check if out of date" # just here in the worst case
            color = discord.Colour.orange()

        embed = discord.Embed(title=behind,
                              colour=color)

        return embed

    def _get_travis(self):
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

        # makes a quick test if the image is even accessable if not gives out a error
        request = requests.get(travisbuildstatus)
        if request.status_code == 200:
            embed.set_image(url=travisbuildstatus)
        else:
            embed.add_field(
                name="Could not reach travis page of", value=str(repo_name))

        return embed

def check_folder():
    if not os.path.exists(".git"):
        raise Exception("\n\nThis is not a valid git clone. Please return to the guide and follow it")

def setup(bot):
    check_folder()
    n = status(bot)
    bot.add_cog(n)
