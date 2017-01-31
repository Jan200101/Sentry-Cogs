import discord
from discord.ext import commands
import aiohttp
import asyncio
import sys


class lenny:
    """Lenny Cog ( ͡° ͜ʖ ͡°)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lenny(self, count: int=1):
        """(╯°□°）╯︵ ┻━┻"""

        # edit this number for a higher lenny count (updating will reset the
        # cog)
        maxcount = 15

        if count > maxcount:
            await self.bot.say("Cannot post more than {} lennys".format(maxcount))
            return

        # uses lenny.today as a api that returns dicts.
        gateway = 'http://lenny.today/api/v1/random?limit={}'.format(count)
        payload = {}
        payload['limit'] = 1
        headers = {'user-agent': 'Red-cog/1.0'}

        session = aiohttp.ClientSession()
        async with session.get(gateway, params=payload, headers=headers) as r:
            lenny = await r.json()

        session.close()  # closes the session to close the connection to the site

        try:
            lennylist = []
            for x in lenny:
                # gets the face (lenny) out of dict and puts it in a list
                lennylist.append("{}\n".format(x['face']))

            lenny = "".join(lennylist)  # merges the list into a string

            await self.bot.say(lenny)  # says the lennys
            return
        except:
            return


def setup(bot):
    bot.add_cog(lenny(bot))
