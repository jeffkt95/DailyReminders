import sys
from TwilioSms import TwilioSms
from iCloudReminders import iCloudReminders
from GoogleCalendarConnection import GoogleCalendarConnection

def main():
    username = sys.argv[1]
    password = sys.argv[2]
    
    icReminders = iCloudReminders(username, password, 'Family')

    messageToText = icReminders.formatMessage()
    print("Texting message....")
    print(messageToText)
    #twilioClient = TwilioSms()
    #twilioClient.sendMessage("-\n" + messageToText, "+14073739626")
    #twilioClient.sendMessage("-\n" + messageToText, "+14435387234")

    print("....Now google calendar stuff....")
    googleCalendar = GoogleCalendarConnection()
    googleCalendar.setEvents(4)
    googleCalendar.formatEvents()
    

if __name__ == "__main__":
    main()