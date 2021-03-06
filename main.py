import sys
from TwilioSms import TwilioSms
from iCloudReminders import iCloudReminders
from GoogleCalendarConnection import GoogleCalendarConnection

def main():
    usage = "usage: main.py <icloudUsername> <icloudPassword> <optional:icloudReminders> <optional:googleCalendar> <optional:textJeff> <optional:textKatie>"
    usage = usage + "\n\nThe first two arguments must be the icloud username and password, respectively."
    usage = usage + "\nAfter that, in any order, specify if you want 'icloudReminders', 'googleCalendar' reminders, and if you want to 'textKatie' and/or 'textJeff'."
    if (len(sys.argv) < 3):
        print(usage)
        exit(0)
        
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