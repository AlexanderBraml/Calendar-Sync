import datetime
from abc import ABC, abstractmethod
from typing import Any, List

from src.Event import Event, Reminder


class CalProvider(ABC):

    @abstractmethod
    def get_day(self, cal: str, day: datetime.datetime) -> List[Event]:
        pass

    @abstractmethod
    def create_events(self, cal: str, events: List[Event]) -> None:
        for event in events:
            self.create_event(cal, event)

    @abstractmethod
    def create_event(self, cal: str, event: Event) -> None:
        pass

    @abstractmethod
    def delete_events(self, cal: str, events: List[Event]) -> None:
        for event in events:
            self.delete_event(cal, event)

    @abstractmethod
    def delete_event(self, cal: str, event: Event) -> None:
        if type(event.raw) != Any:
            pass

    @abstractmethod
    def parse_event(self, raw_event: Any) -> Event:
        pass

    @abstractmethod
    def parse_reminder(self, raw_reminder: Any) -> Reminder:
        pass
