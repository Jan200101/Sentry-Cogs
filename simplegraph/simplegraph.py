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
        self.normalsize =  self.settings['GRIDSIZE']
        self.position = self.normalposition
        self.size = self.normalsize

    @commands.command()
    async def reset(self):

        self.position = self.normalposition
        self.size = self.normalsize

        await self.bot.say('Reset values')

    @commands.command(pass_context=True)
    async def move(self, ctx, x:int=0, y:int=0):

        if x == 0 and y == 0:
            await send_cmd_help(ctx)
            await self.bot.say('```Current Position\nX:{}\nY:{}```'.format(self.position['x'], self.position['y']))
            return

        if self.size['w'] - self.size['w'] * 2 <= self.position['x'] + x <= self.size['w']:
            self.position = {'x':self.position['x'] + x, 'y':self.position['y']}
        else:
            await self.bot.say('You cannot go past `X {}` and `Y {}` or `X {}` and `Y {}`'.format(self.size['w'], self.size['h'], self.size['w'] - self.size['w'] * 2, self.size['h'] - self.size['h'] * 2))
            return

        if self.size['h'] - self.size['h'] * 2 <= self.position['y'] + y <= self.size['h']:
            self.position = {'x':self.position['x'],'y':self.position['y'] + y}
        else:
            await self.bot.say('You cannot go past `X {}` and `Y {}` or `X {}` and `Y {}`'.format(self.size['w'], self.size['h'], self.size['w'] - self.size['w'] * 2, self.size['h'] - self.size['h'] * 2))
            return

        await self.bot.say('Move to\n```X:{}\nY:{}```'.format(self.position['x'], self.position['y']))

    @commands.command()
    async def show(self):

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


def check_file():
    data = {}
    data['GRIDSIZE'] = {'h':10, 'w':10}
    f = "data/sgraph/settings.json"
    if not dataIO.is_valid_json(f):
        print("[SimpleGraph]Creating default settings.json...")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(SimpleGraph(bot))
