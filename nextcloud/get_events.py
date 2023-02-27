from datetime import datetime, time
import caldav
from src.env import webdav_credentials
from src.representation import Event


def parse_datetime(date: str):
    formatted = date.replace('DTSTART:', '').replace('DTEND:', '')[:-1]

    year = int(formatted[:4])
    month = int(formatted[4:6])
    day = int(formatted[6:8])
    hour = int(formatted[9:11]) + 1
    min = int(formatted[11:13])
    sec = int(formatted[13:15])

    return datetime(year, month, day, hour, min, sec)


url = webdav_credentials
today = datetime.combine(datetime.today(), time(0, 0))

client = caldav.DAVClient(url)
principal = client.principal()
calendars = principal.calendars()

if len(calendars) > 0:
    calendar = calendars[2]
    events = calendar.date_search(today, datetime.combine(today, time(23, 59, 59, 59)))

    print(events)

    if len(events) == 0:
        print("No events today!")
    else:
        print("Total {num_events} events:".format(num_events=len(events)))

        for event in events:
            split = event.data.split('\n')
            print(split[6])
            print(split[7])

            start = parse_datetime(split[6])
            end = parse_datetime(split[7])

            e = Event('Event', '', start, end, [])

            print(e)
