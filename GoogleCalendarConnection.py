from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from datetime import timedelta
import pytz
from datetime import datetime, date, time
import calendar

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
        
        #print("Getting calendar events from " + str(startTime) + " to " + str(endTime))
        events_result = self.service.events().list(calendarId='jeffkt95@gmail.com', timeMin=startTime, timeMax=endTime,
                                              singleEvents=True, orderBy='startTime').execute()
        self.jeffCalendarEvents = events_result.get('items', [])
            
        events_result = self.service.events().list(calendarId='ktjeff95@gmail.com', timeMin=startTime, timeMax=endTime,
                                              singleEvents=True, orderBy='startTime').execute()
        self.ktCalendarEvents = events_result.get('items', [])

    def formatEvents(self):
        eventsStr = "\n" + "Google calendar events"
        
        eventsStr = eventsStr + "\n" + "-Jeff's calendar events:"
        if not self.jeffCalendarEvents:
            eventsStr = eventsStr + "\n" + "  * None"
        for event in self.jeffCalendarEvents:
            start = event['start'].get('dateTime', event['start'].get('date'))
            startStr = getPrettyDateTimeString(start)
            eventsStr = eventsStr + "\n" + "  * " + startStr + ": " + event['summary']
            
        eventsStr = eventsStr + "\n" + "-Katie's calendar events:"
        if not self.ktCalendarEvents:
            eventsStr = eventsStr + "\n" + " * None"
        for event in self.ktCalendarEvents:
            start = event['start'].get('dateTime', event['start'].get('date'))
            startStr = getPrettyDateTimeString(start)
            eventsStr = eventsStr + "\n" + "  * " + startStr + ": " + event['summary']
            
        return eventsStr

            
def getUtcTimeAtMidnight(date):
    tz = pytz.timezone("America/New_York")
    midnight_without_tzinfo = datetime.combine(date, time())
    midnight_with_tzinfo = tz.localize(midnight_without_tzinfo)
    
    utcTimeIso = midnight_with_tzinfo.astimezone(pytz.utc).isoformat()
    #Strip the last 6 characters off, the +/- part at the end
    utcTime = utcTimeIso[:-6] + 'Z'
    
    return utcTime
    
def getPrettyDateTimeString(dateTimeStr):
    dateTimeObj = getDateTimeFromString(dateTimeStr)
    
    dayStr = calendar.day_name[dateTimeObj.weekday()]
    dayStr = dayStr[:3]
    
    dateStr = str(dateTimeObj.month) + "/" + str(int(dateTimeObj.day))
    
    
    #dateStr = calendar.day_name[dateTimeObj.weekday()] + ", " + calendar.month_name[dateTimeObj.month] + " " + str(int(dateTimeObj.day))
    timeStr = dateTimeObj.strftime('%#I:%M%p')
    return dayStr + " " + dateStr + ", " + timeStr
    
def getDateTimeFromString(dateTimeStr):
    #If the dateTimeStr is only 10 long, then it's just a date with no time; an all-day event. Just return date.
    if (len(dateTimeStr) == 10):
        hasTime = False
    else:
        hasTime = True
        
    dateStr = dateTimeStr[:10]
    if (hasTime):
        timeStr = dateTimeStr[11:-9]
    
    year = dateStr[:4]
    month = dateStr[5:7]
    day = dateStr[8:10]
    if (hasTime):
        hour = timeStr[:2]
        minute = timeStr[4:5]

    if (hasTime):
        ret = datetime(int(year), int(month), int(day), int(hour), int(minute))
    else:
        ret = datetime(int(year), int(month), int(day))
    return ret
        
    