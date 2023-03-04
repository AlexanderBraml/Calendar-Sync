import datetime
from typing import Any, List

import caldav
from dateutil import parser

from src.CalProvider import CalProvider
from src.Event import Reminder, Event


class CaldavProvider(CalProvider):

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_day(self, day: datetime.datetime, cal: List[str]) -> List[Event]:
        start_of_day = day.replace(hour=0, minute=0, second=0).astimezone(tz=None)
        end_of_day = day.replace(hour=23, minute=59, second=59).astimezone(tz=None)

        calendars = caldav.DAVClient(self.base_url).principal().calendars()

        raw_events = []
        for calendar in calendars:
            if calendar.name in cal:
                raw_events += calendar.date_search(start_of_day, end_of_day)

        parsed = []
        for raw_event in raw_events:
            event = self.parse_event(raw_event)
            if event is not None and event.start_time >= start_of_day:
                parsed.append(event)

        return parsed

    def create_event(self, cal: str, event: Event) -> None:
        calendars = caldav.DAVClient(self.base_url).principal().calendars()
        for calendar in calendars:
            if calendar.name == cal:
                calendar.save_event(summary=event.summary, description=event.description, dtstart=event.start_time,
                                    dtend=event.end_time)

    def delete_event(self, event: Event) -> None:
        if type(event.raw) != caldav.objects.Event:
            raise ValueError('Cannot delete event which is not from this calendar.')

        event.raw.delete()

    def parse_event(self, raw_event: caldav.objects.Event) -> Event | None:
        split = raw_event.data.split('\n')
        start: str = ''
        end: str = ''
        summary: str = ''
        for item in split:
            if item.startswith('DTSTART;VALUE=DATE:') or item.startswith('DTEND;VALUE=DATE:'):
                return None  # Full day event, currently not supported
            elif item.startswith('DTSTART'):
                start = item.replace('DTSTART:', '')
            elif item.startswith('DTEND'):
                end = item.replace('DTEND:', '')
            elif item.startswith('SUMMARY'):
                summary = item.replace('SUMMARY:', '')

        return Event(summary, '', False, self.__parse_datetime(start), self.__parse_datetime(end), [], raw_event)

    @staticmethod
    def __parse_datetime(date: str) -> datetime.datetime:
        return parser.parse(date).replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

    def parse_reminder(self, raw_reminder: Any) -> Reminder:
        return Reminder()


if __name__ == '__main__':
    from src.env import caldav_credentials

    pro = CaldavProvider(caldav_credentials)
    print(pro.get_day(datetime.datetime.today() + datetime.timedelta(days=1), ['Reclaim']))
