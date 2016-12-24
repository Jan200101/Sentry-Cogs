import discord
from discord.ext import commands
from cogs.utils.chat_formatting import box

class mathematics:
    """Math interpreter in Discord"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["mathematics"])
    async def math(self, ctx, *, math):
        """Does math you are too lazy for"""

        math = math.replace(" ", "")

        try:
            calculation = eval(math)
        except:
            await self.bot.say("Could not do math with `{}`".format(math))
            return

        await self.bot.say(box("{}={}".format(math, calculation,), "Prolog"))



def setup(bot):
    bot.add_cog(mathematics(bot))
