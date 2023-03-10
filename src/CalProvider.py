import datetime
from abc import ABC, abstractmethod
from typing import Any, List

from src.Event import Event, Reminder


class CalProvider(ABC):

    @abstractmethod
    def get_day(self, day: datetime.datetime, cal: List[str]) -> List[Event]:
        pass

    def create_events(self, cal: str, events: List[Event]) -> None:
        for event in events:
            self.create_event(cal, event)

    @abstractmethod
    def create_event(self, cal: str, event: Event) -> None:
        pass

    def delete_events(self, cal: str, events: List[Event]) -> None:
        for event in events:
            self.delete_event(cal, event)

    @abstractmethod
    def delete_event(self, cal: str, event: Event) -> None:
        pass

    def parse_events(self, events: List[Any]) -> List[Event]:
        return [self.parse_event(event) for event in events if event is not None]

    @abstractmethod
    def parse_event(self, raw_event: Any) -> Event | None:
        pass

    @abstractmethod
    def parse_reminder(self, raw_reminder: Any) -> List[Reminder]:
        pass
