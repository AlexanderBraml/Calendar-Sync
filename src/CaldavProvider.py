import datetime
import logging
from typing import Any, List
from urllib.parse import urlsplit

import caldav

from src.CalProvider import CalProvider
from src.Event import Reminder, Event

log = logging.getLogger('calendar_sync')


class CaldavProvider(CalProvider):

    def __init__(self, base_url: str):
        log.info(f'Setup caldav provider with server {urlsplit(base_url).hostname}')
        self.base_url = base_url

    def get_day(self, day: datetime.datetime, cal: List[str]) -> List[Event]:
        log.debug(f'Getting all events from Caldav Calendar ({cal}) for {day.date()}')
        start_of_day = day.replace(hour=0, minute=0, second=0).astimezone(tz=None)
        end_of_day = day.replace(hour=23, minute=59, second=59).astimezone(tz=None)

        calendars = caldav.DAVClient(self.base_url).principal().calendars()

        raw_events = []
        for calendar in calendars:
            if calendar.name in cal:
                raw_events += calendar.search(start=start_of_day, end=end_of_day, event=True, expand=True)
        log.debug(f'Raw events received from Caldav Calendar: {raw_events}')

        return [event for event in self.parse_events(raw_events)
                if (event.is_all_day and event.start_time.date() == day.date())
                or (not event.is_all_day and event.start_time >= start_of_day)]

    def create_event(self, cal: str, event: Event) -> None:
        log.debug(f'Creating event {event} in Caldav Calendar ({cal})')
        calendars = caldav.DAVClient(self.base_url).principal().calendars()
        for calendar in calendars:
            if calendar.name == cal:
                calendar.save_event(summary=event.summary, description=event.description, dtstart=event.start_time,
                                    dtend=event.end_time)
        log.info(f'Successfully created event {event} in Caldav Calendar')

    def delete_event(self, cal: str, event: Event) -> None:
        log.debug(f'Deleting event {event} in Caldav Calendar ({cal})')
        if type(event.raw) != caldav.objects.Event:
            raise ValueError('Cannot delete event which is not from this calendar.')

        event.raw.delete()
        log.info(f'Successfully deleted event {event} in Caldav Calendar')

    def parse_event(self, raw_event: caldav.objects.Event) -> Event | None:
        log.debug(f'Parsing event {raw_event} from Caldav Calendar')

        descr = str(raw_event.icalendar_component.get("description"))
        summary = str(raw_event.icalendar_component.get("summary"))
        start = raw_event.icalendar_component.get("dtstart").dt
        end = raw_event.icalendar_component.get("dtend").dt
        is_all_day = type(start) == datetime.date

        if is_all_day:
            start = datetime.datetime.combine(start, datetime.time(0))
            end = datetime.datetime.combine(end, datetime.time(0))

        return Event(summary, descr, is_all_day, start.astimezone(tz=None), end.astimezone(tz=None), [], raw_event)

    def parse_reminder(self, raw_reminder: Any) -> List[Reminder]:
        log.warning(f'NOT SUPPORTED: Parsing reminder {raw_reminder} from Caldav Calendar')
        return []

    def __str__(self) -> str:
        return f'CaldavProvider[{urlsplit(self.base_url).hostname}]'
