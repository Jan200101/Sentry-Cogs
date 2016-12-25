from discord.ext import commands
from cogs.utils.chat_formatting import box


class mathematics:
    """Math interpreter in Discord"""

    def __init__(self, bot):
        self.bot = bot

    async def __calculation__(self, n):  # For people to use as a example
        try:
            result = eval(n)
        except:
            result = None

        return result

    @commands.command()
    async def math(self, *, math: str):
        """Does math for you inside Discord"""

        # puts what is in math into the __calculation__ definition and takes
        # the mathematical result of it
        calculation = await self.__calculation__(math)

        if not calculation:
            await self.bot.say("Could not do math with " + math)
        else:
            await self.bot.say(box(calculation, "Prolog"))


def setup(bot):
    n = mathematics(bot)
    bot.add_cog(n)
