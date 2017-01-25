import discord
from discord.ext import commands
from __main__ import send_cmd_help
import valve.source.a2s

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

class GameServer:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def getserver(self, ctx, serverip:str):
        """Get infos about a gameserver"""

        if serverip.find(":") == -1:
            await self.bot.say("You also need to specify a port\n"
                               "Example : `123.123.123.123.25701`")
            return

        serverc = serverip.replace(":", " ")
        serverc = serverc.split()
        serverc = [str(serverc[0]), int(serverc[1])]
        serverc = tuple(serverc)


        if not validate_ip(str(serverc[0])):
            await send_cmd_help(ctx)
            return

        try:
            server = valve.source.a2s.ServerQuerier(serverc)
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

        servername = info.values['server_name'].strip()

        playernumber = str(info.values['player_count'] - info.values['bot_count'])
        botnumber = str(info.values['bot_count'])
        maxplayers = str(info.values['max_players'])


        em = discord.Embed(colour=discord.Colour.green())
        em.add_field(name="Game", value=game)
        em.add_field(name="Gamemode", value=gamemode)
        em.add_field(name="servername", value=servername)
        em.add_field(name="IP", value=serverc[0])
        if botnumber != '0':
            em.add_field(name="Playernumber", value="{}/{}\n*{} Bots*".format(playernumber, maxplayers, botnumber))
        else:
            em.add_field(name="Playernumber", value="{}/{}\n".format(playernumber, maxplayers))
        em.add_field(name="Map", value=map)
        em.add_field(name=u"\u2063", value="[Connect](steam://connect/{})".format(serverip), inline=False)

        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(GameServer(bot))
