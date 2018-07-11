from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from datetime import timedelta
import pytz
from datetime import datetime, date, time

#Python calendar API: https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/
class GoogleCalendarConnection:

    def __init__(self):
        # Setup the Calendar API
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        
        self.service = build('calendar', 'v3', http=creds.authorize(Http()))

    def setEvents(self, numDaysInFuture):
        timeNow = datetime.now()
        tz = pytz.timezone("America/New_York")
        midnightToday = datetime(timeNow.year, timeNow.month, timeNow.day, tzinfo=tz)
        
        futureTime = midnightToday + timedelta(days=numDaysInFuture)
    
        startTime = getUtcTimeAtMidnight(midnightToday)
        endTime = getUtcTimeAtMidnight(futureTime)
        
        print("Getting calendar events from " + str(startTime) + " to " + str(endTime))
        events_result = self.service.events().list(calendarId='jeffkt95@gmail.com', timeMin=startTime, timeMax=endTime,
                                              singleEvents=True, orderBy='startTime').execute()
        self.jeffCalendarEvents = events_result.get('items', [])
            
        events_result = self.service.events().list(calendarId='ktjeff95@gmail.com', timeMin=startTime, timeMax=endTime,
                                              singleEvents=True, orderBy='startTime').execute()
        self.ktCalendarEvents = events_result.get('items', [])

    def formatEvents(self):
        if not self.jeffCalendarEvents:
            print('No upcoming events found.')
        for event in self.jeffCalendarEvents:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            
        if not self.ktCalendarEvents:
            print('No upcoming events found.')
        for event in self.ktCalendarEvents:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

            
def getUtcTimeAtMidnight(date):
    tz = pytz.timezone("America/New_York")
    midnight_without_tzinfo = datetime.combine(date, time())
    midnight_with_tzinfo = tz.localize(midnight_without_tzinfo)
    
    utcTimeIso = midnight_with_tzinfo.astimezone(pytz.utc).isoformat()
    #Strip the last 6 characters off, the +/- part at the end
    utcTime = utcTimeIso[:-6] + 'Z'
    
    return utcTime
    