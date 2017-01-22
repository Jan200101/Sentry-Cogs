from google import search
from random import randint
from discord.ext import commands

class google:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def google(self, searchterm:str):
        """This does stuff!"""

        maxsearch = 3 # Defines the max amounts of search. Has to be integer.
        # TODO make maxsearch changable

        results = []
        results.append("**Here are your search results:**\n")
        # Message you get before the result post.
        # TODO Make result message changeable

        for url in search(searchterm, pause=randint(1.0, 2.0)): # Generates the list of google results
            results.append("<{}>".format(url))
            maxsearch = maxsearch - 1
            if maxsearch < 1:
                break

        await self.bot.say("\n".join(results)) # Post all results.

def setup(bot):
    bot.add_cog(google(bot))
