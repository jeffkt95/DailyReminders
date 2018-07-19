import sys
from TwilioSms import TwilioSms
from iCloudReminders import iCloudReminders
from GoogleCalendarConnection import GoogleCalendarConnection

def main():
    twilioClient = TwilioSms()
    
    username = sys.argv[1]
    password = sys.argv[2]

    textJeff = False
    textKatie = False
    if ("textJeff" in sys.argv):
        textJeff = True
    if ("textKatie" in sys.argv):
        textKatie = True
        
    if ("icloudReminders" in sys.argv):        
        icReminders = iCloudReminders(username, password, 'Katie List', 'Jeff List')
        icRemindersTextMessage = icReminders.formatMessage()
        print(icRemindersTextMessage)
        
        if (textJeff or textKatie):
            print("Texting iCloud reminders message....")
            if (textJeff):
                twilioClient.sendMessage("-\n" + icRemindersTextMessage, "+14073739626")
            if (textKatie):
                twilioClient.sendMessage("-\n" + icRemindersTextMessage, "+14435387234")
     
    if ("googleCalendar" in sys.argv):
        googleCalendar = GoogleCalendarConnection()
        googleCalendar.setEvents(4)
        calendarTextMessage = googleCalendar.formatEvents()
        print(calendarTextMessage)
        
        if (textJeff or textKatie):
            print("Texting Google calendar events message....")
            if (textJeff):
                twilioClient.sendMessage("-\n" + calendarTextMessage, "+14073739626")
            if (textKatie):
                twilioClient.sendMessage("-\n" + calendarTextMessage, "+14435387234")
    

if __name__ == "__main__":
    main()