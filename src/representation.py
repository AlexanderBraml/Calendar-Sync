from __future__ import annotations
from typing import List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class ReclaimType(Enum):
    NONE = 1
    PERSONAL = 2
    WORK = 3


@dataclass
class Reminder:
    
    method: str
    minutes: str

    def parse_google(self, encoded: str) -> Reminder:
        pass


@dataclass
class Event:

    summary: str
    description: str
    start_time: datetime
    end_time: datetime
    reminders: List[Reminder]
    reclaim_type: ReclaimType = ReclaimType.NONE

    def parse_google(encoded: str) -> Event:
        pass
    
    def parse_nc(encoded: str) -> Event:
        pass

ev = Event.parse_google("")

print(ev)
