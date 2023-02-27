from typing import List
import datetime

import caldav

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from representation import Event
from src.env import webdav_credentials

SCOPES = ['https://www.googleapis.com/auth/calendar']

g_creds = Credentials.from_authorized_user_file('token.json', SCOPES)


def get_day_google(day: datetime.datetime) -> List[Event]:
    try:
        service = build('calendar', 'v3', credentials=g_creds)

        start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + '+01:00'
        end_of_day = day.replace(hour=23, minute=59, second=59, microsecond=0).isoformat() + '+01:00'

        events_result = service.events().list(calendarId='primary', timeMin=start_of_day, timeMax=end_of_day,
                                              singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        return [Event.parse_google(ev) for ev in events]
    except HttpError as error:
        print('An error occurred: %s' % error)


def get_day_nc(day: datetime.datetime) -> List[Event]:
    url = webdav_credentials
    start_of_day = day.replace(hour=0, minute=0, second=0) - datetime.timedelta(hours=1, minutes=0)
    end_of_day = day.replace(hour=23, minute=59, second=59) - datetime.timedelta(hours=1, minutes=0)

    calendars = caldav.DAVClient(url).principal().calendars()

    calendar = calendars[2]
    events = calendar.date_search(start_of_day, end_of_day)

    return [Event.parse_nc(ev.data) for ev in events]
