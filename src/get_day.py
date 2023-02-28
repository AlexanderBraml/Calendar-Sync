from typing import List
import datetime
from enum import Enum

import caldav

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from representation import Event
from env import webdav_credentials, nc_cal_id

SCOPES = ['https://www.googleapis.com/auth/calendar']

g_creds = Credentials.from_authorized_user_file('token.json', SCOPES)


class Calendar(Enum):
    FOR_NC_SYNC = 0
    FOR_GO_SYNC = 1


def get_day_google(day: datetime.datetime, cal: Calendar) -> List[Event]:
    try:
        service = build('calendar', 'v3', credentials=g_creds)

        start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + '+01:00'
        end_of_day = day.replace(hour=23, minute=59, second=59, microsecond=0).isoformat() + '+01:00'

        calendarId = 'primary' if cal == Calendar.FOR_NC_SYNC else nc_cal_id
        events_result = service.events().list(calendarId=calendarId, timeMin=start_of_day, timeMax=end_of_day,
                                              singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        return [Event.parse_google(ev) for ev in events]
    except HttpError as error:
        print('An error occurred: %s' % error)


def get_day_nc(day: datetime.datetime, cal: Calendar) -> List[Event]:
    start_of_day = day.replace(hour=0, minute=0, second=0)
    end_of_day = day.replace(hour=23, minute=59, second=59)

    calendars = caldav.DAVClient(webdav_credentials).principal().calendars()

    events = []
    for i in [2] if cal == Calendar.FOR_NC_SYNC else [0, 1, 3]:
        events += calendars[i].date_search(start_of_day, end_of_day)

    parsed = []
    for event in events:
        ev = Event.parse_nc(event)
        if ev.start_time >= start_of_day:
            event.load()
            ev.summary = event.vobject_instance.vevent.summary.value
            parsed.append(ev)

    return parsed
