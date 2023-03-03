import datetime
from abc import ABC, abstractmethod
from typing import Any, List

from src.Event import Event, Reminder


class CalProvider(ABC):

    @abstractmethod
    def get_day(self, day: datetime.datetime) -> List[Event]:
        pass

    @abstractmethod
    def create_event(self, ev: Event) -> None:
        pass

    @abstractmethod
    def delete_event(self, ev: Event) -> None:
        pass

    @abstractmethod
    def parse_event(self, raw_event: Any) -> Event:
        pass

    @abstractmethod
    def parse_reminder(self, raw_reminder: Any) -> Reminder:
        pass
