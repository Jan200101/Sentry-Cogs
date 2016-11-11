from discord.ext import commands
from cogs.utils import checks

class IsLoaded:
    "Checks if a Cog is loaded or not"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="IsLoaded", no_pm=True)
    @checks.is_owner()
    async def cog_loaded(self, cog: str):
        """Checks if a Cog is loaded or not (unmaintained)"""

        if self.bot.get_cog(cog)== None:
            await self.bot.say("""```Py\n Module with the class "{}" is not loaded```""".format(cog))
        else:
            await self.bot.say("""```Py\n Module with the class "{}" is loaded```""".format(cog))

def setup(bot):
    n = IsLoaded(bot)
    bot.add_cog(n)
