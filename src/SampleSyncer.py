import datetime

from src.CaldavProvider import CaldavProvider
from src.GCalProvider import GCalProvider
from src.Sync import SyncJob, Syncer

if __name__ == '__main__':
    from env import nc_url, nc_to_g_source, nc_to_g_target, g_to_nc_source, g_to_nc_target

    nc_provider = CaldavProvider(nc_url)
    g_provider = GCalProvider()

    syncer = Syncer()
    syncer.register(
        SyncJob(nc_provider, g_provider, nc_to_g_source, nc_to_g_target, datetime.datetime.today(),
                datetime.datetime.today() + datetime.timedelta(days=10)))
    syncer.register(SyncJob(g_provider, nc_provider, g_to_nc_source, g_to_nc_target, datetime.datetime.today(),
                            datetime.datetime.today() + datetime.timedelta(days=10)))
    syncer.sync()
