import unittest
from GoogleCalendarConnection import GoogleCalendarConnection
from GoogleCalendarConnection import getUtcTimeAtMidnight
from GoogleCalendarConnection import getDateTimeFromString
from GoogleCalendarConnection import getPrettyDateTimeString
import pytz
from datetime import datetime

class TestGoogleCalendarConnection(unittest.TestCase):

    def setUp(self):
        self.googleCalendar = GoogleCalendarConnection()
        self.googleCalendar.setEvents(4)
        
    def test_formatEvents(self):
        calendarTextMessage = self.googleCalendar.formatEvents()
        pass  #Got here with no crash. Success!

    def test_getUtcTimeAtMidnight(self):
        tz = pytz.timezone("America/New_York")

        resultTimeAtMidnight = getUtcTimeAtMidnight(datetime(2018, 1, 1, tzinfo=tz))
        self.assertEqual('2018-01-01T05:00:00Z', resultTimeAtMidnight)
        
        resultTimeAtMidnight = getUtcTimeAtMidnight(datetime(2020, 10, 12, tzinfo=tz))
        self.assertEqual('2020-10-12T04:00:00Z', resultTimeAtMidnight)
        
        resultTimeAtMidnight = getUtcTimeAtMidnight(datetime(2021, 12, 31, tzinfo=tz))
        self.assertEqual('2021-12-31T05:00:00Z', resultTimeAtMidnight)
        
    def test_getDateTimeFromString(self):
        #Lots of tests on this one as I had lots of bugs for different lengths
        #Test time for all day event
        resultDatetime = getDateTimeFromString("2018-07-24", True)
        self.assertEqual(resultDatetime.year, 2018)
        self.assertEqual(resultDatetime.month, 7)
        self.assertEqual(resultDatetime.day, 24)
        
        #Test time on the hour
        resultDatetime = getDateTimeFromString("2018-12-25T19:00:00-04:00")
        self.assertEqual(resultDatetime.year, 2018)
        self.assertEqual(resultDatetime.month, 12)
        self.assertEqual(resultDatetime.day, 25)
        self.assertEqual(resultDatetime.hour, 19)
        self.assertEqual(resultDatetime.minute, 0)
        
        #Test time with hours and minutes
        resultDatetime = getDateTimeFromString("2018-12-01T18:30:00-04:00")
        self.assertEqual(resultDatetime.year, 2018)
        self.assertEqual(resultDatetime.month, 12)
        self.assertEqual(resultDatetime.day, 1)
        self.assertEqual(resultDatetime.hour, 18)
        self.assertEqual(resultDatetime.minute, 30)

        #Test time with hours and minutes
        resultDatetime = getDateTimeFromString("2018-07-07T18:59:00-04:00")
        self.assertEqual(resultDatetime.year, 2018)
        self.assertEqual(resultDatetime.month, 7)
        self.assertEqual(resultDatetime.day, 7)
        self.assertEqual(resultDatetime.hour, 18)
        self.assertEqual(resultDatetime.minute, 59)
        
        #Test time with hours and minutes
        resultDatetime = getDateTimeFromString("2018-07-23T01:01:00-04:00")
        self.assertEqual(resultDatetime.year, 2018)
        self.assertEqual(resultDatetime.month, 7)
        self.assertEqual(resultDatetime.day, 23)
        self.assertEqual(resultDatetime.hour, 1)
        self.assertEqual(resultDatetime.minute, 1)
        
        #Test time with hours and minutes
        resultDatetime = getDateTimeFromString("2018-07-23T12:01:00-04:00")
        self.assertEqual(resultDatetime.year, 2018)
        self.assertEqual(resultDatetime.month, 7)
        self.assertEqual(resultDatetime.day, 23)
        self.assertEqual(resultDatetime.hour, 12)
        self.assertEqual(resultDatetime.minute, 1)
        
        #Test time with hours and minutes
        resultDatetime = getDateTimeFromString("2018-07-23T01:12:00-04:00")
        self.assertEqual(resultDatetime.year, 2018)
        self.assertEqual(resultDatetime.month, 7)
        self.assertEqual(resultDatetime.day, 23)
        self.assertEqual(resultDatetime.hour, 1)
        self.assertEqual(resultDatetime.minute, 12)
        
    def test_getPrettyDateTimeString(self):
        resultStr = getPrettyDateTimeString("2018-07-23T18:30:00-04:00")
        self.assertEqual(resultStr, "Mon 7/23, 6:30PM")

        resultStr = getPrettyDateTimeString("2018-07-01")
        self.assertEqual(resultStr, "Sun 7/1")

        resultStr = getPrettyDateTimeString("2018-07-24")
        self.assertEqual(resultStr, "Tue 7/24")

        resultStr = getPrettyDateTimeString("2018-12-24")
        self.assertEqual(resultStr, "Mon 12/24")

        resultStr = getPrettyDateTimeString("2018-12-05")
        self.assertEqual(resultStr, "Wed 12/5")

        resultStr = getPrettyDateTimeString("2018-07-24T11:30:00-04:00")
        self.assertEqual(resultStr, "Tue 7/24, 11:30AM")

        resultStr = getPrettyDateTimeString("2018-07-25T19:00:00-04:00")
        self.assertEqual(resultStr, "Wed 7/25, 7:00PM")

        resultStr = getPrettyDateTimeString("2018-07-24T08:00:00-04:00")
        self.assertEqual(resultStr, "Tue 7/24, 8:00AM")

        resultStr = getPrettyDateTimeString("2018-07-26T08:00:00-04:00")
        self.assertEqual(resultStr, "Thu 7/26, 8:00AM")
    
if (__name__) == "__main__":
    unittest.main()
    