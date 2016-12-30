import discord
import os
from discord.ext import commands
import asyncio
import requests

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
        response = self.bot.loop.run_in_executor(None, self._get_version)
        result = await asyncio.wait_for(response, timeout=20)
        
        try:
            await self.bot.say(embed=result)
        except discord.HTTPException:
            await self.bot.say("Could not embed")
        except:
            await self.bot.say("a error happend")

    def _get_behind(self):

        branch = os.popen(r'git rev-parse --abbrev-ref HEAD') #gets current branch
        branch = branch.read().strip()

        os.popen(r'git fetch') # fetches remote

        status = os.popen(r'git status -uno') #checks if local is out of date
        status = status.read().strip()

        if status.find("Your branch is behind") != -1:
            behind = "Your bot is out of date by {} commits".format("".join([str(s) for s in status.split() if s.isdigit()]))
            color = discord.Colour.red()
        elif status.find("Your branch is up-to-date") != -1:
            behind = "Your bot is up to date"
            color = discord.Colour.green()
        else:
            behind = "Unable to check if out of date"
            color = discord.Colour.orange()


        embed = discord.Embed(title=behind,
                                  colour=color)

        return embed

    def _get_version(self):

        branch = os.popen(r'git rev-parse --abbrev-ref HEAD')
        branch = branch.read().strip()
        allbranches = os.popen(r'git branch')
        allbranches = allbranches.read().strip()
        url = os.popen(r'git config --get remote.origin.url')
        url = url.read().strip()[:-4]
        branchurl = "{}/tree/{}".format(url, branch)
        repo_name = url.split("/")[-1]
        author_name = url.split("/")[-2]

        if allbranches.find("* " + branch) != -1:
            defaultbranch = True
        else:
            defaultbranch = False

        travisbuildstatus = "{}.png?branch={}".format(url.replace("github.com", "api.travis-ci.org"), branch)


        if defaultbranch:
            embed = discord.Embed(title="travis-ci build status of {} by {}".format(repo_name, author_name),
                                  colour=discord.Colour.orange(),
                                  url=branchurl)
        else:

            embed = discord.Embed(title="travis-ci build status of {} in {} by {}".format(branch, repo_name, author_name),
                                  colour=discord.Colour.orange(),
                                  url=branchurl)


        request = requests.get(travisbuildstatus)
        if request.status_code == 200:
            embed.set_image(url=travisbuildstatus)
        else:
            embed.add_field(name="Could not reach travis page of", value=str(repo_name))

        return embed


def setup(bot):
    n = status(bot)
    bot.add_cog(n)
