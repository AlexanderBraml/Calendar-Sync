import datetime
from dataclasses import dataclass
from typing import List, Any


@dataclass
class Reminder:
    minutes: int = 0


@dataclass
class Event:
    summary: str
    description: str
    is_all_day: bool
    start_time: datetime.datetime
    end_time: datetime.datetime
    reminder: List[Reminder]
    raw: Any

    def short_str(self):
        return f'Event[{self.summary}, {self.start_time}, {self.end_time}, {self.is_all_day}]'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Event):
            return False
        return self.summary == other.summary and self.start_time == other.start_time and self.end_time == other.end_time
