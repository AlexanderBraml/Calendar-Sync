from datetime import datetime, time
import caldav
from src.env import webdav_credentials

url = webdav_credentials
today = datetime.combine(datetime.today(), time(0, 0))

client = caldav.DAVClient(url)
principal = client.principal()
calendars = principal.calendars()

if len(calendars) > 0:
    calendar = calendars[0]
    events = calendar.date_search(today, datetime.combine(today, time(23, 59, 59, 59)))

    if len(events) == 0:
        print("No events today!")
    else:
        print("Total {num_events} events:".format(num_events=len(events)))

        for event in events:
            event.load()
            e = event.instance.vevent
            print(e)
