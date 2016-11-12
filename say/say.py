from discord.ext import commands
from cogs.utils import checks
from cogs.utils.chat_formatting import box
from cogs.utils.chat_formatting import pagify

class say:
    """Makes the bot say things for you. Great with the Schedule cog"""

    def __init__(self, bot):
        self.bot = bot
        if self.bot.get_cog("Admin") != None:
            raise Exception("This Cog does not work with the Admin cog from Squid-Plugins")

    @commands.command(pass_context=True, no_pm=True, aliases=["opsay"])
    @checks.admin_or_permissions(administrator=True)
    async def adminsay(self, ctx, *, text):
        """Says Something as the bot without anyone knowing who wrote it"""
        try:
            await self.bot.delete_message(ctx.message)
        except:
            raise Exception("I do not have the permissions needed")
        await self.bot.say(text + "")

    @commands.command(pass_context=True, no_pm=True)
    async def say(self, ctx, *, text):
        """Says Something as the bot without the needs special rights"""

        if ctx.message.author == "238685395838042113":
            await self.bot.say("Stop using my bot for making it say simple stuff")
        else:
            text += "(message by"
            text += ctx.message.author
            text += ")"
            for page in pagify(text, ["\n"], shorten_by=13, page_length=2000):
                await self.bot.say(page)

def setup(bot):
    bot.add_cog(say(bot))

        for page in pagify(data, ["\n"], shorten_by=13, page_length=2000):
            await self.bot.say(box(page, 'Prolog'))
