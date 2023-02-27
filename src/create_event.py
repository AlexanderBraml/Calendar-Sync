import datetime

import caldav

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.env import nc_cal_id, webdav_credentials
from src.representation import Event

SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_google(ev: Event) -> None:
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    service.events().insert(calendarId=nc_cal_id, body=ev.as_google_dict()).execute()


def create_nc(ev: Event) -> None:
    calendars = caldav.DAVClient(webdav_credentials).principal().calendars()
    calendar = calendars[2]
    calendar.save_event(
        dtstart=ev.start_time,
        dtend=ev.end_time,
        summary=ev.summary
    )
