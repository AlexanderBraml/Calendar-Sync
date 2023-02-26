from __future__ import annotations
from typing import List
from dataclasses import dataclass
from enum import Enum
import datetime


class ReclaimType(Enum):
    NONE = 1
    PERSONAL = 2
    WORK = 3


@dataclass
class Reminder:
    minutes: str

    @staticmethod
    def parse_google(rem: dict) -> Reminder:
        return Reminder(rem['minutes'])

    @staticmethod
    def parse_reminders_google(rems: dict) -> List[Reminder]:
        reminders = []
        if 'overrides' in rems:
            for override in rems['overrides']:
                reminders.append(Reminder.parse_google(override))
        return reminders


@dataclass
class Event:
    summary: str
    description: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    reminders: List[Reminder]
    reclaim_type: ReclaimType = ReclaimType.NONE

    @staticmethod
    def parse_google(ev: dict) -> Event:
        description = ''
        if 'description' in ev:
            description = ev['description']
        return Event(ev['summary'], description, parse_datetime(ev['start']), parse_datetime(ev['end']),
                     Reminder.parse_reminders_google(ev['reminders']))

    @staticmethod
    def parse_nc(encoded: str) -> Event:
        pass


def parse_datetime(date: dict):
    return datetime.datetime.strptime(date['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S')
