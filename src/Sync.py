class SyncJob:
    pass


class Syncer:

    def __init__(self):
        self.sync_job: SyncJob | None = None

    def register(self, sync_job: SyncJob) -> None:
        pass

    def sync(self) -> None:
        pass
