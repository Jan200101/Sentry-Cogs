import discord
from discord.ext import commands

class math:
    """Math interpreter in Discord"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def math(self, ctx, math):
        """Does math you are too lazy for"""

        math = math.replace(" ", "")

        calculation = eval(math)

        await self.bot.say("{} **=** {}".format(math, calculation))



def setup(bot):
    bot.add_cog(math(bot))
