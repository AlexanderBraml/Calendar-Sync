import datetime
from dataclasses import dataclass
from typing import List, Any


@dataclass
class Reminder:
    minutes: str = 0


@dataclass
class Event:
    summary: str
    description: str
    is_all_day: bool
    start_time: datetime.datetime
    end_time: datetime.datetime
    reminder: List[Reminder]
    raw: Any
