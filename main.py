import sys
from TwilioSms import TwilioSms
from iCloudReminders import iCloudReminders
from GoogleCalendarConnection import GoogleCalendarConnection

def main():
    twilioClient = TwilioSms()
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    icReminders = iCloudReminders(username, password, 'Family')

    icRemindersTextMessage = icReminders.formatMessage()
    print(icRemindersTextMessage)
    print("Texting iCloud reminders message....")
    twilioClient.sendMessage("-\n" + icRemindersTextMessage, "+14073739626")
    twilioClient.sendMessage("-\n" + icRemindersTextMessage, "+14435387234")

    googleCalendar = GoogleCalendarConnection()
    googleCalendar.setEvents(4)
    calendarTextMessage = googleCalendar.formatEvents()
    print(calendarTextMessage)
    print("Texting Google calendar events message....")
    twilioClient.sendMessage("-\n" + calendarTextMessage, "+14073739626")
    twilioClient.sendMessage("-\n" + calendarTextMessage, "+14435387234")
    

if __name__ == "__main__":
    main()