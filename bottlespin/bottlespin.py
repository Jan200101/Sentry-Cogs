import discord
from discord.ext import commands
from random import choice


class Bottlespin:
    """Spins a bottle and lands on a random user."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def spin(self, ctx, role:str='@everyone'):
        """Spin the bottle"""

        roles = [r.name for r in ctx.message.server.roles]
        author = ctx.message.author
        server = ctx.message.server

        if len(server.members) < 2:
            await self.bot.say("`Not enough people are around to spin the bottle`")
            return

        if role in roles:
            roleexist = True
        else:
            await self.bot.say("`{} is not a exising role`".format(role))
            return

        if roleexist:
            target = [m.name for m in server.members if m != author and role in [s.name for s in m.roles] and str(m.status) == "online" or str(m.status) == "idle"]
        else:
            target = [m.name for m in server.members if m != author and str(m.status) == "online" or str(m.status) == "idle"]

        if not target:
            if role:
                await self.bot.say("`Sorry I couldnt find anyone to point the bottle at with the role {}`".format(role))
            else:
                await self.bot.say("`Sorry I couldnt find anyone to point the bottle at`")
            return
        else:
            target = choice(list(target))


        await self.bot.say("`{} spinned the bottle and it landed on {}`".format(author, target))


def setup(bot):
    n = Bottlespin(bot)
    bot.add_cog(n)
