from __future__ import print_function
import discord
from discord.ext import commands
import httplib2
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


    @commands.command()
    async def playtest(self):

        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        eventsResult = service.events().list(
            calendarId='fkcvr5iio1kgdib061u7tgkg5o@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
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
                if z.day > 6:
                    color = "fafafa"
                    color = int(color, 16)
                else:
                    color = "f4f142"
                    color = int(color, 16)

        data = discord.Embed(description="Next Playtest is", color=color)
        try:
            data.add_field(name=eve, value="{}\n\nin {}".format(x, k), inline=False)
            data.add_field(name=u"\u2063", value="[**Playtest Calendar**](https://calendar.google.com/calendar/embed?src=fkcvr5iio1kgdib061u7tgkg5o%40group.calendar.google.com&ctz=America/Chicago)", inline=False)
        except:
            await self.bot.say("A error has occured while trying to embed")
            return

        try:
            await self.bot.say(embed=data)
        except:
            await self.bot.say("a unkown error has occured")






def setup(bot):
    bot.add_cog(playtest(bot))
