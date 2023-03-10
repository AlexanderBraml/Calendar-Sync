import datetime
from os.path import abspath
from typing import Any, List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.CalProvider import CalProvider
from src.Event import Reminder, Event

G_SCOPES = ['https://www.googleapis.com/auth/calendar']

g_creds = Credentials.from_authorized_user_file(abspath('token.json'), G_SCOPES)
g_service = build('calendar', 'v3', credentials=g_creds)


class GCalProvider(CalProvider):

    def get_day(self, day: datetime.datetime, cal: List[str]) -> List[Event]:
        start_of_day = day.replace(hour=0, minute=0, second=0).astimezone(tz=None)
        end_of_day = day.replace(hour=23, minute=59, second=59, microsecond=0).astimezone(tz=None).isoformat()

        raw_events = []
        for calendar in cal:
            events_result = g_service.events().list(calendarId=calendar, timeMin=start_of_day.isoformat(),
                                                    timeMax=end_of_day, singleEvents=True,
                                                    orderBy='startTime').execute()
            raw_events += events_result.get('items', [])

        return [event for event in self.parse_events(raw_events) if event.start_time >= start_of_day]

    def create_event(self, cal: str, event: Event) -> None:
        g_service.events().insert(calendarId=cal, body=self.__event_as_dict(event)).execute()

    @staticmethod
    def __event_as_dict(event: Event) -> dict:
        return {
            'summary': event.summary,
            'start': GCalProvider.__datetime_as_dict(event.start_time),
            'end': GCalProvider.__datetime_as_dict(event.end_time),
            'description': event.description,
            'reminders': {'useDefault': True, },
        }

    @staticmethod
    def __datetime_as_dict(date: datetime.datetime) -> dict:
        return {
            'dateTime': date.isoformat(),
            'timeZone': date.tzname(),
        }

    def delete_event(self, cal: str, event: Event) -> None:
        if type(event.raw) != dict:
            raise ValueError('Cannot delete event which is not from this calendar.')

        g_service.events().delete(calendarId=cal, eventId=event.raw['id']).execute()

    def parse_event(self, raw_event: dict) -> Event | None:
        description = ''
        if 'description' in raw_event:
            description = raw_event['description']

        return Event(raw_event['summary'], description, False,
                     datetime.datetime.fromisoformat(raw_event['start']['dateTime']),
                     datetime.datetime.fromisoformat(raw_event['end']['dateTime']),
                     [self.parse_reminder(raw_event['reminders'])], raw_event)

    def parse_reminder(self, raw_reminder: Any) -> Reminder:
        return Reminder()
