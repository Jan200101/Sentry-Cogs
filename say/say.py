import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.chat_formatting import box,  pagify, escape_mass_mentions
from random import choice, randint
import datetime


class say:
    """Makes the bot say things for you now with embeds"""

    def __init__(self, bot):
        self.bot = bot
        if self.bot.get_cog("Admin") != None:
            raise Exception("This Cog does not work with the Admin cog from Squid-Plugins")

    @commands.command(pass_context=True, no_pm=True)
    async def say(self, ctx, *, text: str):
        """Says Something as the bot"""

        auth = " (message by {})".format(ctx.message.author.mention)

        for text in pagify(text, ["\n"]):
            await self.bot.say(escape_mass_mentions(text) + auth)


    @commands.command(pass_context=True, no_pm=True, aliases=["sayop"])
    @checks.admin_or_permissions(administrator=True)
    async def sayadmin(self, ctx, *, text: str):
        """Says Something as the bot without any trace of the message author"""
        try:
            await self.bot.delete_message(ctx.message)
        except:
            await self.bot.say("I do not have the `Manage Messages` permissions")
            return

        for text in pagify(text, ["\n"]):
            await self.bot.say(escape_mass_mentions(text))

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(administrator=True)
    async def sayclear(self, ctx, *, text):
        """sayadmin for selfbots"""

        for text in pagify(text, ["\n"]):
            await self.bot.say(escape_mass_mentions(text))

    @commands.command(pass_context=True, no_pm=True)
    async def embedsay(self, ctx, *, text: str):
        """Says Something as the bot in a embed"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))

        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name,
                            url=ctx.message.author.avatar_url, icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True, aliases=["embedsayop"])
    @checks.admin_or_permissions(administrator=True)
    async def embedsayadmin(self, ctx, *, text: str):
        """Says Something as the bot without any trace of the message author in a embed"""

        try:
            await self.bot.delete_message(ctx.message)
        except:
            await self.bot.say("I do not have the `Manage Messages` permissions")
            return

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def embedsayclear(self, ctx, *, text: str):
        """embedsayadmin for selfbots"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def embedcolor(self, ctx, color: str, *, text: str):
        """Says Something as the bot in a colored embed"""

        created_at = ("Created on {}".format(
            ctx.message.timestamp.strftime("%d %b %Y %H:%M")))

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        if color == None:
            color = colour
        else:
            color = color.replace("#", "")
            color = int(color, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))

        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name,
                            url=ctx.message.author.avatar_url, icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True, aliases=["embedcolorop"])
    @checks.admin_or_permissions(administrator=True)
    async def embedcoloradmin(self, ctx, color: str, *, text: str):
        """Says Something as the bot without any trace of the message author in a colored embed"""

        try:
            await self.bot.delete_message(ctx.message)
        except:
            await self.bot.say("I do not have the `Manage Messages` permissions")
            return

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        if color == None:
            color = colour
        else:
            color = color.replace("#", "")
            color = int(color, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(
            text), colour=discord.Colour(value=color))

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def embedcolorclear(self, ctx, color: str, *, text: str):
        """embedcoloradmin for selfbots"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        if color == None:
            color = colour
        else:
            color = color.replace("#", "")
            color = color.replace("0x", "")
            color = int(color, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        data = discord.Embed(description=str(
            text), colour=discord.Colour(value=color))

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")


    @commands.command(pass_context=True, no_pm=True)
    async def embedurl(self, ctx, text: str, url: str = None):
        """Embed links into a embed"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        if not url:
            data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))
        else:
            if text.find("]") != -1:
                textnumber = text.find("]") + 1
                url = "({})".format(url)
                text = text[:textnumber] + url  + text[textnumber:]

                data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))

            else:
                data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))


        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name,
                            url=ctx.message.author.avatar_url, icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(administrator=True)
    async def embedurladmin(self, ctx, text: str, url: str = None):
        """Embed links into a embed without knowing who wrote it"""

        try:
            await self.bot.delete_message(ctx.message)
        except:
            await self.bot.say("I do not have the `Manage Messages` permissions")
            return

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        if not url:
            data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))
        else:
            if text.find("]") != -1:
                textnumber = text.find("]") + 1
                url = "({})".format(url)
                text = text[:textnumber] + url  + text[textnumber:]

                data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))

            else:
                data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(administrator=True)
    async def embedurlclear(self, ctx, text: str, url: str = None):
        """embedurladmin for selfbots"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        if not url:
            data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))
        else:
            if text.find("]") != -1:
                textnumber = text.find("]") + 1
                url = "({})".format(url)
                text = text[:textnumber] + url  + text[textnumber:]

                data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))

            else:
                data = discord.Embed(description=str(text), colour=discord.Colour(value=colour))

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True)
    async def embedimage(self, ctx, *, image: str):
        """Embed a image as the bot"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        if image.endswith(".gif") or image.endswith(".png") or image.endswith(".jpeg") or image.endswith(".jpg"):
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.set_image(url=image)
        else:
            await self.bot.say("Not a Valid Link")
            return

        if ctx.message.author.avatar_url:
            data.set_author(name=ctx.message.author.name,
                            url=ctx.message.author.avatar_url, icon_url=ctx.message.author.avatar_url)
        else:
            data.set_author(name=ctx.message.author.name)

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission to send this")

    @commands.command(pass_context=True, no_pm=True, aliases=["embedimageop"])
    @checks.admin_or_permissions(administrator=True)
    async def embedimageadmin(self, ctx, *, image: str):
        """Embed a image as the bot without anyone knowing from who"""

        try:
            await self.bot.delete_message(ctx.message)
        except:
            await self.bot.say("I do not have the `Manage Messages` permissions")
            return

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        if image.endswith(".gif") or image.endswith(".png") or image.endswith(".jpeg") or image.endswith(".jpg"):
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.set_image(url=image)
        else:
            await self.bot.say("Not a Valid Link")
            return

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def embedimageclear(self, ctx, *, image: str):
        """embedimageadmin for selfbots"""

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        randnum = randint(1, 10)
        empty = u"\u2063"
        emptyrand = empty * randnum

        if image.endswith(".gif") or image.endswith(".png") or image.endswith(".jpeg") or image.endswith(".jpg"):
            data = discord.Embed(colour=discord.Colour(value=colour))
            data.set_image(url=image)
        else:
            await self.bot.say("Not a Valid Link")
            return

        try:
            await self.bot.say(emptyrand, embed=data)
        except:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

def setup(bot):
    bot.add_cog(say(bot))
