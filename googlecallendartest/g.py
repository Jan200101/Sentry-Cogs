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

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json

start = ""
te = ""
eve = ""

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
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

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming event')
    eventsResult = service.events().list(
        calendarId='fkcvr5iio1kgdib061u7tgkg5o@group.calendar.google.com', timeMin=now, maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        global start
        start = 'No upcoming events found.'
    for event in events:

        global start
        global time
        global eve
        start = event['start'].get('dateTime', event['start'].get('date'))
        eve = event['summary']
        start = start.replace("-06:00", "")
        start = start.replace("T", " ")
        time = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')


        return

class googlecallendartest:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def gcal(self):


        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)

        main()

        try:
            test_at = time.strftime("%d %b %Y %H:%M")
            test_in = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()

            data = discord.Embed(colour=discord.Colour(value=colour))
            data.add_field(name=str(eve), value="At **{}**\n*(in {})*".format(test_at, test_in))
            await self.bot.say(embed=data)
        except:
            await self.bot.say("error")
            print(start + eve)






def setup(bot):
    bot.add_cog(googlecallendartest(bot))
