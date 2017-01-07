from __future__ import print_function
import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import box
from __main__ import send_cmd_help, settings
import httplib2
import asyncio
import os
from random import choice

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

import datetime
from dateutil.relativedelta import relativedelta

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

__VERSION__ = "0.2.1\n"
__VERSION__ += "Changed the way playtestchannel and playtestrefreshrate worked"

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():  # Gets your google credentials to get the calendars with.
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
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


class playtest:
    """Playtest Commands.\n"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/playtest/settings.json')
        self.refresh_rate = self.settings['REFRESH_RATE']
        if settings.owner != "137268543874924544":
            raise Exception("This cog wasnt made for one server only and has no use for you")

    async def get_playtest(self):

        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        time = None

        eventsResult = service.events().list(
            calendarId='fkcvr5iio1kgdib061u7tgkg5o@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()  # Getting the calendar

        events = eventsResult.get('items', [])

        if not events:
            start = "No upcoming events found."
            eve = u"\u2063"
            found = False
            x = start
            time = datetime.datetime.utcnow()

        for event in events:
            if not time:
                start = event['start'].get(
                    'dateTime', event['start'].get('date'))
                eve = event['summary']
                found = True
                x = start
                x = x.replace("T", " ")
                x = x.replace("-06:00", "")
                if len(x) > 10:
                    try:
                        time = datetime.datetime.strptime(
                            x, '%Y-%m-%d %H:%M:%S')
                    except:
                        time = datetime.datetime.strptime(
                            x, '%Y-%m-%d %H:%M:%S')

        if not time:
            start = "No upcoming events found or there has been a error"
            eve = u"\u2063"
            found = False
            x = start
            time = datetime.datetime.utcnow()

        x = time.strftime("**%d %b %Y**\nat %H:%M CT")
        z = relativedelta(time, datetime.datetime.utcnow() - datetime.timedelta(hours=6))

        color = "585858"
        color = int(color, 16)

        k = ""

        if z.years != 0:  # just adding the certain time if it exist
            k += "{} years ".format(z.years)

        if z.months != 0:
            k += "{} months ".format(z.months)

        if z.days != 0:
            k += "{} days ".format(z.days)

        if z.hours != 0:
            k += "{} hours ".format(z.hours)

        if z.minutes != 0:
            k += "{} minutes ".format(z.minutes)

        if z.seconds != 0:  # Bunch of color code stuff for certain times
            color = discord.colour.Color.blue()

        if z.minutes != 0:
            if z.minutes < 16:
                color = discord.colour.Color.green()
            else:
                color = discord.colour.Color.red()

        if z.hours != 0:
            if z.hours < 1:
                color = discord.colour.Color.red()
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

        data.add_field(
            name=eve, value="{}\n\nin {}".format(x, k), inline=False)
        data.add_field(
            name=u"\u2063", value="[**Playtest Calendar**](http://playtesting.tophattwaffle.com/)", inline=False)

        return data

    @commands.command()
    @checks.is_owner()
    async def playtestversion(self):
        """Prints out the playtest cogs version"""

        await self.bot.say("`{}`".format(__VERSION__))

    @commands.command(aliases=["nextplaytest", "playtest"])
    async def playtestinfo(self):
        """Gives out information for the nextp playtest"""

        msg = await self.get_playtest()

        try:
            await self.bot.say(embed=msg)
        except:
            await self.bot.say("a unkown error has occured")

    @commands.command(pass_context=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def playtestrefreshrate(self, ctx, seconds: int=0):  # By Paddo
        """Sets how often the playtest information gets updated"""

        if not self.refresh_rate:  # If statement incase someone removes it or sets it to 0
            self.refresh_rate = 5

        if seconds == 0:
            message = box(
                "Current refresh rate is {}".format(self.refresh_rate))
            await send_cmd_help(ctx)
        elif seconds < 5:
            message = '`I can\'t do that, the refresh rate has to be above 5 seconds`'
        else:
            self.refresh_rate = seconds
            self.settings['REFRESH_RATE'] = self.refresh_rate
            dataIO.save_json('data/playtest/settings.json', self.settings)
            message = '`Changed refresh rate to {} seconds`'.format(
                self.refresh_rate)
        await self.bot.say(message)

    @commands.command(no_pm=True, pass_context=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def playtestchannel(self, ctx, channel: discord.Channel=None):  # Also by Paddo
        """
        Set the channel to which the bot will sent its continues updates.
        """
        if channel:
            self.settings['CHANNEL_ID'] = str(channel.id)
            dataIO.save_json('data/playtest/settings.json', self.settings)
            message = 'Channel set to {}'.format(channel.mention)
        elif not self.settings['CHANNEL_ID']:
            message = box("No Channel set")
            await send_cmd_help(ctx)
        else:
            channel = discord.utils.get(
                self.bot.get_all_channels(), id=self.settings['CHANNEL_ID'])
            if channel:
                message = box('Current channel is #{}'.format(channel))
                await send_cmd_help(ctx)
            else:
                self.settings['CHANNEL_ID'] = None
                message = box("No Channel set")
                await send_cmd_help(ctx)

        await self.bot.say(message)

    # Reloads the automated playtest. Thank Paddo
    async def reload_playtest(self):
        await asyncio.sleep(30)
        while self == self.bot.get_cog('playtest'):
            if self.settings['CHANNEL_ID']:
                msg = await self.get_playtest()
                channel = discord.utils.get(
                    self.bot.get_all_channels(), id=self.settings['CHANNEL_ID'])
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


def check_folder():  # Paddo is great
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
    bot.loop.create_task(n.reload_playtest())
