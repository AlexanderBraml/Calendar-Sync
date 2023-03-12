import datetime
import logging
from os.path import abspath
from typing import Any, List

import pytz
from dateutil import parser
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.CalProvider import CalProvider
from src.Event import Reminder, Event

log = logging.getLogger('calendar_sync')

g_scopes = ['https://www.googleapis.com/auth/calendar']
g_creds = Credentials.from_authorized_user_file(abspath('token.json'), g_scopes)
g_service = build('calendar', 'v3', credentials=g_creds)


class GCalProvider(CalProvider):

    def get_day(self, day: datetime.datetime, cal: List[str]) -> List[Event]:
        log.debug(f'Getting all events from Google Calendar ({cal}) for {day.date()}')
        start_of_day = day.replace(hour=0, minute=0, second=0).astimezone(tz=None)
        end_of_day = day.replace(hour=23, minute=59, second=59, microsecond=0).astimezone(tz=None).isoformat()

        raw_events = []
        for calendar in cal:
            events_result = g_service.events().list(calendarId=calendar, timeMin=start_of_day.isoformat(),
                                                    timeMax=end_of_day, singleEvents=True,
                                                    orderBy='startTime').execute()
            raw_events += events_result.get('items', [])
        log.debug(f'Raw events received from Google Calendar: {raw_events}')

        return [event for event in self.parse_events(raw_events) if event.start_time >= start_of_day]

    def create_event(self, cal: str, event: Event) -> None:
        log.debug(f'Creating event {event} in Google Calendar ({cal})')
        g_service.events().insert(calendarId=cal, body=self.__event_as_dict(event)).execute()
        log.info(f'Successfully created event {event} in Google Calendar')

    @staticmethod
    def __event_as_dict(event: Event) -> dict:
        return {
            'summary': event.summary,
            'start': GCalProvider.__datetime_as_dict(event.start_time),
            'end': GCalProvider.__datetime_as_dict(event.end_time),
            'description': event.description,
            'reminders': GCalProvider.__reminder_as_dict(event.reminder),
        }

    @staticmethod
    def __datetime_as_dict(date: datetime.datetime) -> dict:
        normal_timezone = pytz.timezone('UTC')
        normalized = normal_timezone.normalize(date)
        log.debug(f'Transforming datetime into dict (dateTime: {normalized.isoformat()}, timeZone: {str(normalized)})')
        return {
            'dateTime': normalized.isoformat(),
            'timeZone': str(normal_timezone),
        }

    @staticmethod
    def __reminder_as_dict(reminders: List[Reminder]):
        if len(reminders) == 0:
            return {'useDefault': True, }
        else:
            return {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': reminder.minutes}
                                                       for reminder in reminders]}

    def delete_event(self, cal: str, event: Event) -> None:
        log.debug(f'Deleting event {event} in Google Calendar ({cal})')
        if type(event.raw) != dict:
            raise ValueError('Cannot delete event which is not from this calendar.')

        g_service.events().delete(calendarId=cal, eventId=event.raw['id']).execute()
        log.info(f'Successfully deleted event {event} in Google Calendar')

    def parse_event(self, raw_event: dict) -> Event | None:
        log.debug(f'Parsing event {raw_event} from Google Calendar')
        description = ''
        if 'description' in raw_event:
            description = raw_event['description']

        return Event(raw_event['summary'], description, False,
                     parser.parse(raw_event['start']['dateTime']),
                     parser.parse(raw_event['end']['dateTime']),
                     self.parse_reminder(raw_event['reminders']), raw_event)

    def parse_reminder(self, raw_reminder: Any) -> List[Reminder]:
        log.debug(f'Parsing reminder {raw_reminder} from Google Calendar')
        if raw_reminder['useDefault']:
            return []
        else:
            return [Reminder(reminder['minutes']) for reminder in raw_reminder['overrides']]

    def __str__(self) -> str:
        return 'GCalProvider'
