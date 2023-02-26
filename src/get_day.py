from typing import List
import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from representation import Event

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

        for event in events:
            print(event)
    except HttpError as error:
        print('An error occurred: %s' % error)
