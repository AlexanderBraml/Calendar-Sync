import datetime
from typing import Any, List

import caldav

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

        return [event for event in self.parse_events(raw_events) if event.start_time >= start_of_day]

    def create_event(self, cal: str, event: Event) -> None:
        calendars = caldav.DAVClient(self.base_url).principal().calendars()
        for calendar in calendars:
            if calendar.name == cal:
                calendar.save_event(summary=event.summary, description=event.description, dtstart=event.start_time,
                                    dtend=event.end_time)

    def delete_event(self, cal: str, event: Event) -> None:
        if type(event.raw) != caldav.objects.Event:
            raise ValueError('Cannot delete event which is not from this calendar.')

        event.raw.delete()

    def parse_event(self, raw_event: caldav.objects.Event) -> Event | None:
        return Event(str(raw_event.icalendar_component.get("summary")),
                     str(raw_event.icalendar_component.get("description")),
                     False,
                     raw_event.icalendar_component.get("dtstart").dt.astimezone(tz=None),
                     raw_event.icalendar_component.get("dtend").dt.astimezone(tz=None),
                     [], raw_event)

    def parse_reminder(self, raw_reminder: Any) -> Reminder:
        return Reminder()
