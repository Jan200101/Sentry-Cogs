import discord
from discord.ext import commands
import aiohttp
import asyncio
import sys

class lenny:
    """Lenny Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lenny(self, count:int=1):
        """Lenny Command"""

        if count > 10:
            await self.bot.say("Cannot post more then 10 lennys")
            return

        gateway = 'http://lenny.today/api/v1/random?limit={}'.format(count)
        payload = {}
        payload['limit'] = 1
        headers = {'user-agent': 'Red-cog/1.0'}
        session = aiohttp.ClientSession()
        async with session.get(gateway, params=payload, headers=headers) as r:
            lenny = await r.json()
        session.close()

        try:
            lennylist = []
            for x in lenny:
                lennylist.append("{}\n".format(x['face']))

            lenny = "".join(lennylist)

            await self.bot.say(lenny)
            return
        except:
            return





def setup(bot):
    bot.add_cog(lenny(bot))
