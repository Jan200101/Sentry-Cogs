import discord
from discord.ext import commands
import valve.source.a2s

class src:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def getserver(self, ctx, serverip:str):

        serverip = serverip.replace(":", " ")
        serverip = serverip.split()
        serverip = [str(serverip[0]), int(serverip[1])]
        serverip = tuple(serverip)

        try:
            server = valve.source.a2s.ServerQuerier(serverip)
            info = server.info()
        except valve.source.a2s.NoResponseError:
            em = discord.Embed(title="Could not fetch Server",colour=discord.Colour.red())
            return
        except:
            await self.bot.say("Could not fetch Server")
            return

        map = info.values['map']

        game = info.values['folder']
        gamemode = info.values['game']

        servername = info.values['server_name']

        playernumber = str(info.values['player_count'] - info.values['bot_count'])
        botnumber = str(info.values['bot_count'])
        maxplayers = str(info.values['max_players'])


        em = discord.Embed(title="Infos about {}".format(serverip[0]),colour=discord.Colour.green())
        em.add_field(name="Game", value=game)
        em.add_field(name="Gamemode", value=gamemode)
        em.add_field(name="servername", value=servername)
        if botnumber != '0':
            em.add_field(name="Playernumber", value="{}/{}\n*{} Bots*".format(playernumber, maxplayers, botnumber))
        else:
            em.add_field(name="Playernumber", value="{}/{}\n".format(playernumber, maxplayers))
        em.add_field(name="Map", value=map)

        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(src(bot))
