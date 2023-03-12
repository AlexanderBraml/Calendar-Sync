from __future__ import annotations

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
        if not isinstance(other, Event) or self.summary != other.summary:
            return False

        if self.is_all_day and other.is_all_day:
            return self.start_time.date() == other.start_time.date() and self.end_time.date() == other.end_time.date()
        else:
            return self.start_time == other.start_time and self.end_time == other.end_time

    def __hash__(self):
        if self.is_all_day:
            return hash((self.summary, self.start_time.date(), self.end_time.date()))
        else:
            return hash((self.summary, self.start_time, self.end_time))

    def __str__(self) -> str:
        return f'Event[{self.summary}, {self.start_time}, {self.end_time}]'
