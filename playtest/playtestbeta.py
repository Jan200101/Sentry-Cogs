from __future__ import print_function
import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
import httplib2
import asyncio
import os
from random import choice

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from dateutil.relativedelta import relativedelta

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials(): #Gets your google credentials to get the calendars with.
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



class playtest:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/playtest/settings.json')
        self.refresh_rate = self.settings['REFRESH_RATE']

def get_playtest():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    eventsResult = service.events().list(
        calendarId='fkcvr5iio1kgdib061u7tgkg5o@group.calendar.google.com',
        timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute() #Getting the calendar

    events = eventsResult.get('items', [])

    if not events:
        start = "No upcoming events found."
        eve = u"\u2063"
        found = False
        x = start

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        eve = event['summary']
        found = True
        x = start
        x = x.replace("T", " ")
        x = x.replace("-06:00", "")
        x = x.replace("00:00:00", "")

    if len(x) < 11:
        time = datetime.datetime.strptime(x, '%Y-%m-%d')
    else:
        time = datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    x = time.strftime("**%d %b %Y**\nat %H:%M CT")
    z = relativedelta(time, datetime.date.today())
    color = "000000"
    color = int(color, 16)
    k = ""

    if z.years != 0: #just adding the certain time if it exist
        k += "{} years ".format(z.years)

    if z.months != 0:
        k += "{} months ".format(z.months)

    if z.days != 0:
        k += "{} days ".format(z.days)

    if z.hours != 0:
        k += "{} hours ".format(z.hours)

    if z.minutes != 0:
        k += "{} minutes ".format(z.minutes)

    if z.seconds != 0:
        k += "{} seconds ".format(z.seconds)

    if z.seconds != 0: #Bunch of color code stuff for certain times
        color = discord.colour.Color.blue()

    if z.minutes != 0:
        if z.minutes < 16:
            color = discord.colour.Color.green()
        else:
            color = discord.colour.Color.red()

    if z.hours != 0:
        if z.hours < 2:
            color = discord.colour.Color.red()
        elif z.hours > -1:
            color = "0047ab"
            color = int(color, 16)
        else:
            color = "f49e42"
            color = int(color, 16)

    if z.days != 0:
        if z.days > 6:
            color = "fafafa"
            color = int(color, 16)
        else:
            color = "f4f142"
            color = int(color, 16)

    data = discord.Embed(description="Next Playtest is", color=color)
    try:
        data.add_field(name=eve, value="{}\n\nin {}".format(x, k), inline=False)
        worked = True
    except:
        worked = False

    if worked == False:
        data = False

    return data

    @commands.command()
    @checks.serverowner_or_permissions(manage_server=True)
    async def playtestrefresh(self, seconds: int): #By Paddo
        """Sets how often the playtest information gets updated"""
        if await self._int(seconds):
            if seconds < 5:
                message = '`I can\'t do that, the refresh rate has to be above 5 seconds`'
            else:
                self.refresh_rate = seconds
                self.settings['REFRESH_RATE'] = self.refresh_rate
                dataIO.save_json('data/playtest/settings.json', self.settings)
                message = '`Changed refresh rate to {} seconds`'.format(self.refresh_rate)
        await self.bot.say(message)

    @commands.command(no_pm=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def playtestchannel(self, channelid :str): #Also by Paddo
        """
        Set the channel to which the bot will sent its continues updates.
        Example: [p]statschannel #statistics
        """
        if not channelid:
            self.settings['CHANNEL_ID'] = None
            await self.bot.say("Channel Removed")
            return

        try:
            channel = ctx.message.server.get_channel(channelid)
        except:
            await self.bot.say("Error")
            return

        if not channel:
            await self.bot.say("{} is not a valid channel".format(channel))
            return

        if len(channel) > 0:
            self.settings['CHANNEL_ID'] = str(channel[0].id)
            dataIO.save_json('data/playtest/settings.json', self.settings)
            message = 'Channel set to {}'.format(channel[0].mention)
        elif not self.settings['CHANNEL_ID']:
            message = 'No channel set!'
        else:
            channel = discord.utils.get(self.bot.get_all_channels(), id=self.settings['CHANNEL_ID'])
            message = 'Current channel is {}'.format(channel.mention)
        await self.bot.say(message)

    @commands.command()
    async def playtest(self):

        msg = get_playtest()

        if not data:
            await self.bot.say("Could not embed")

        try:
            await self.bot.say(embed=msg)
        except:
            await self.bot.say("a unkown error has occured")

    async def reload_stats(self): #Reloads the automated playtest. Thank Paddo
        await asyncio.sleep(30)
        while self == self.bot.get_cog('Statistics'):
            if self.settings['CHANNEL_ID']:
                msg = get_playtest()
                if not data:
                    await self.bot.say("Could not embed")
                channel = discord.utils.get(self.bot.get_all_channels(), id=self.settings['CHANNEL_ID'])
                messages = False
                async for message in self.bot.logs_from(channel, limit=1):
                    messages = True
                    if message.author.name == self.bot.user.name:
                        await self.bot.edit_message(message, embed=msg)
                if not messages:
                    await self.bot.send_message(channel, embed=msg)
            else:
                pass
            await asyncio.sleep(self.refresh_rate)

def check_folder(): #Paddo is great
    if not os.path.exists("data/playtest"):
        print("Creating data/playtest folder...")
        os.makedirs("data/playtest")

def check_file():
    data = {}
    data['CHANNEL_ID'] = ''
    data['REFRESH_RATE'] = 5
    f = "data/playtest/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default settings.json...")
        dataIO.save_json(f, data)

def setup(bot):
    check_folder()
    check_file()
    n = playtest(bot)
    bot.add_cog(n)
    bot.loop.create_task(n.reload_stats())