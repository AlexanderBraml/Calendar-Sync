import logging
from typing import List

from src.SyncJob import SyncJob

log = logging.getLogger('calendar_sync')


class Syncer:

    def __init__(self) -> None:
        self.sync_jobs: List[SyncJob] = []

    def register(self, sync_job: SyncJob) -> None:
        self.sync_jobs.append(sync_job)
        log.debug(f'Added {sync_job} to list of sync jobs')

    def sync(self) -> None:
        for job in self.sync_jobs:
            log.debug(f'Syncing job {job}')
            job.sync()
            log.info('Successfully executed sync job')
