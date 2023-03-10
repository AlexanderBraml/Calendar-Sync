import datetime
from dataclasses import dataclass
from typing import List, Set

from src.CalProvider import CalProvider
from src.Event import Event


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
        amount_of_days: int = (self.end_date - self.start_date).days
        for delta in range(amount_of_days + 1):
            day = self.start_date + datetime.timedelta(delta)

            if day == datetime.datetime(2023, 3, 11):
                pass

            source_day: List[Event] = self.source_cal_provider.get_day(day, self.source_cal)
            target_day: List[Event] = self.target_cal_provider.get_day(day, [self.target_cal])
            if not days_equal(set(source_day), set(target_day)):
                self.target_cal_provider.delete_events(self.target_cal, target_day)
                self.target_cal_provider.create_events(self.target_cal, source_day)


class Syncer:

    def __init__(self) -> None:
        self.sync_jobs: List[SyncJob] = []

    def register(self, sync_job: SyncJob) -> None:
        self.sync_jobs.append(sync_job)

    def sync(self) -> None:
        for job in self.sync_jobs:
            job.sync()
