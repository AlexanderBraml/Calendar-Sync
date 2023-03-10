import datetime
import logging
from dataclasses import dataclass
from typing import List, Set

from src.CalProvider import CalProvider
from src.Event import Event

log = logging.getLogger('calendar_sync')


def days_equal(day1: Set[Event], day2: Set[Event]) -> bool:
    if len(day1) != len(day2):
        return False
    return day1 == day2


@dataclass
class SyncJob:
    source_cal_provider: CalProvider
    target_cal_provider: CalProvider
    source_cal: List[str]
    target_cal: str
    start_date: datetime.datetime
    end_date: datetime.datetime

    def sync(self) -> None:
        log.info(f'Syncing {self.source_cal_provider} ({self.source_cal}) '
                 f'-> {self.target_cal_provider} ({self.target_cal})')
        amount_of_days: int = (self.end_date - self.start_date).days
        for delta in range(amount_of_days + 1):
            day = self.start_date + datetime.timedelta(delta)
            log.info(f'Syncing day {day.date()}')

            source_day: List[Event] = self.source_cal_provider.get_day(day, self.source_cal)
            target_day: List[Event] = self.target_cal_provider.get_day(day, [self.target_cal])
            log.debug(f'Source day: {source_day}\nTarget day: {target_day}')
            if not days_equal(set(source_day), set(target_day)):
                log.info('Source day and target day are not equal, syncing them')
                self.target_cal_provider.delete_events(self.target_cal, target_day)
                log.debug('Successfully deleted all events from target day in target calendar')
                self.target_cal_provider.create_events(self.target_cal, source_day)
                log.debug('Successfully created all events from source day in target calendar')
