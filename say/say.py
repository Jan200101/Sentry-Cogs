from discord.ext import commands
from cogs.utils import checks

class say:
    """Makes the bot say things for you. Great with the Schedule cog"""

    def __init__(self, bot):
        self.bot = bot
        if self.bot.get_cog("Admin") != None:
            raise Exception("This Cog does not work with the Admin cog from Squid-Plugins")

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(administrator=True)
    async def adminsay(self, ctx, *, text):
        """Says Something as the bot without anyone knowing who wrote it"""

        await self.bot.delete_message(ctx.message)
        await self.bot.say(text + "")

    @commands.command(pass_context=True, no_pm=True)
    async def say(self, ctx, *, text):
        """Says Something as the bot without the needs special rights"""

        await self.bot.say(text + " (" + ctx.message.author.mention + ")")

def setup(bot):
    bot.add_cog(say(bot))
