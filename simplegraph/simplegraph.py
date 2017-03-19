from pylab import scatter, plot, grid, show, savefig
from matplotlib import pyplot as plt
from discord.ext import commands
from __main__ import send_cmd_help
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from os import path, makedirs

class SimpleGraph:

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/sgraph/settings.json')
        self.normalposition = {'x':0, 'y':0}
        self.position = self.normalposition

    @commands.command()
    async def reset(self):
        """Reset all values"""

        self.position = self.normalposition
        self.size = self.normalsize

        await self.bot.say('Reset values')

    @commands.command(pass_context=True)
    async def move(self, ctx, x:int=None, y:int=None):
        """Move the coordinates (set command comming)"""

        if x == None and y == None:
            await send_cmd_help(ctx)
            await self.bot.say('```Current Position\nX:{}\nY:{}```'.format(self.position['x'], self.position['y']))
            return

        self.position['x'] = x
        self.position['y'] = y
        
        await self.bot.say('Set coordinates to\n```X:{}\nY:{}```'.format(self.position['x'], self.position['y']))

    @commands.command()
    async def show(self):
        """Print out a graph"""

        if self.position == {'x':0, 'y':0}:
            await self.bot.say('```Move the line first using [p]move```')
            return

        message = await self.bot.say('Uploading graph...')

        x = [self.position['x']]
        y = [self.position['y']]
        color=['m','g','r','b']

        fig = plt.figure()
        ax = fig.add_subplot(111)

        scatter(x,y, s=100 ,marker='o', c=color)

        [ plot( [dot_x,dot_x] ,[0,dot_y], '-', linewidth = 3 ) for dot_x,dot_y in zip(x,y) ]
        [ plot( [0,dot_x] ,[dot_y,dot_y], '-', linewidth = 3 ) for dot_x,dot_y in zip(x,y) ]

        left,right = ax.get_xlim()
        low,high = ax.get_ylim()

        grid()

        filename = 'graph.png'
        filepath = 'data/sgraph/temp/' + filename

        with open(filepath, 'wb') as f:
            savefig(f)

        await self.bot.delete_message(message)
        await self.bot.upload(filepath)

def check_folder():  # Paddo is great
    if not path.exists("data/sgraph"):
        print("[SimpleGraph]Creating data/sgraph folder...")
        makedirs("data/sgraph")

    if not path.exists("data/sgraph/temp"):
        print("[SimpleGraph]Creating data/sgraph/temp folder...")
        makedirs("data/sgraph/temp")



def setup(bot):
    check_folder()
    bot.add_cog(SimpleGraph(bot))
