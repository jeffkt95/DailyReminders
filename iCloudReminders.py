from pyicloud import PyiCloudService
import calendar

class iCloudReminders:
    
    def __init__(self, username, password, reminderListName):
        self.iCloudService = PyiCloudService(username, password)
        self.reminderListName = reminderListName
        self.loginAndGetReminders()

    def loginAndGetReminders(self):
        ics = self.iCloudService
        if ics.requires_2fa:
            import click
            print("Two-step authentication required. Your trusted devices are:")

            devices = ics.trusted_devices
            for i, device in enumerate(devices):
                print("  %s: %s" % (i, device.get('deviceName',
                    "SMS to %s" % device.get('phoneNumber'))))

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not ics.send_verification_code(device):
                print("Failed to send verification code")
                sys.exit(1)

            code = click.prompt('Please enter validation code')
            if not ics.validate_verification_code(device, code):
                print("Failed to verify verification code")
                sys.exit(1)
        
        ics.reminders.refresh()
        self.reminders = ics.reminders.lists[self.reminderListName]
        
    def printReminders(self):
        for listItem in self.reminders:
            print("Reminder item: " + str(listItem))
            print("  Item name: " + listItem['title'])
            print("  Item due date: " + str(listItem['due']))

    def formatMessage(self):
        msg = "\n" + "Here are your daily reminders!"
        for listItem in self.reminders:
            msg = msg + "\n" + "  * " + listItem['title'] 
            if (listItem['due'] is not None):
                dueDate = listItem['due']
                dateStr = calendar.day_name[dueDate.weekday()] + ", " + calendar.month_name[dueDate.month] + " " + str(int(dueDate.day))

                msg = msg + ", due " + dateStr
            
        msg = msg + "\n\n" + "Add/remove/mark items done using your iPhone Reminders app."
        
        return msg