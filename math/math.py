import discord
from discord.ext import commands
from cogs.utils.chat_formatting import box

class math:
    """Math interpreter in Discord"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def math(self, ctx, *, math):
        """Does math you are too lazy for"""

        math = math.replace(" ", "")

        calculation = eval(math)

        await self.bot.say(box("{} = {}".format(math, calculation,), "Prolog"))



def setup(bot):
    bot.add_cog(math(bot))
