import datetime
from dataclasses import dataclass
from typing import List

from src.CalProvider import CalProvider
from src.Event import Event


def days_equal(day1: List[Event], day2: List[Event]) -> bool:
    if len(day1) != len(day2):
        return False
    for ev1, ev2 in zip(day1, day2):
        if ev1 != ev2:
            return False
    return True


@dataclass
class SyncJob:

    source_cal_provider: CalProvider
    target_cal_provider: CalProvider
    source_cal: str
    target_cal: str
    start_date: datetime.datetime
    end_date: datetime.datetime

    def sync(self) -> None:
        amount_of_days: int = (self.end_date - self.start_date).days
        for delta in range(amount_of_days):
            day = self.start_date + datetime.timedelta(delta)
            source_day: List[Event] = self.source_cal_provider.get_day(self.source_cal, day)
            target_day: List[Event] = self.target_cal_provider.get_day(self.target_cal, day)
            if not days_equal(source_day, target_day):
                self.target_cal_provider.delete_events(self.target_cal, source_day)
                self.target_cal_provider.create_events(self.target_cal, target_day)


class Syncer:

    def __init__(self) -> None:
        self.sync_jobs: List[SyncJob] = []

    def register(self, sync_job: SyncJob) -> None:
        self.sync_jobs.append(sync_job)

    def sync(self) -> None:
        for job in self.sync_jobs:
            job.sync()
