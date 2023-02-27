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

    def as_google_dict(self) -> dict:
        return {
            'summary': self.summary,
            'start': datetime_to_google(self.start_time),
            'end': datetime_to_google(self.end_time),
            'reminders': {'useDefault': True, },
        }

    @staticmethod
    def parse_google(ev: dict) -> Event:
        description = ''
        if 'description' in ev:
            description = ev['description']
        return Event(ev['summary'], description, parse_datetime_google(ev['start']), parse_datetime_google(ev['end']),
                     Reminder.parse_reminders_google(ev['reminders']))

    @staticmethod
    def parse_nc(ev: str) -> Event:
        split = ev.split('\n')
        start = parse_datetime_nc(split[6])
        end = parse_datetime_nc(split[7])
        return Event('Event', '', start, end, [])


def parse_datetime_google(date: dict):
    return datetime.datetime.strptime(date['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S')


def parse_datetime_nc(date: str):
    formatted = date.replace('DTSTART:', '').replace('DTEND:', '')[:-1]

    year = int(formatted[:4])
    month = int(formatted[4:6])
    day = int(formatted[6:8])
    hour = (int(formatted[9:11]) + 1) % 24
    min = int(formatted[11:13])
    sec = int(formatted[13:15])

    return datetime.datetime(year, month, day, hour, min, sec)


def datetime_to_google(date: datetime.datetime) -> dict:
    return {
        'dateTime': date.strftime('%Y-%m-%dT%H:%M:%S') + '+01:00',
        'timeZone': 'Europe/Berlin',
    }
