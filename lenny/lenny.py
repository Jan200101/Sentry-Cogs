import discord
from discord.ext import commands
import re
import urllib.request
import sys

class lenny:
    """Lenny Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lenny(self):
        """Lenny Command"""

        regex = r':"(\S+)"'
        lenny = urllib.request.urlopen('http://lenny.today/api/v1/random?limit=1').read().decode('utf-8')

        matches = re.findall(regex, lenny)

        for match in matches:
            try:
                await self.bot.say(match)
            except:
                await self.bot.say("Could Lenny")


def setup(bot):
    bot.add_cog(lenny(bot))
