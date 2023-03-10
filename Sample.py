import datetime
import sys

from src.CaldavProvider import CaldavProvider
from src.GCalProvider import GCalProvider
from src.SyncJob import SyncJob
from src.Syncer import Syncer
from src.env import nc_url, nc_to_g_source, nc_to_go_target, go_to_nc_source, go_to_nc_target

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise TypeError('You have to provide the number of days to be synced!')
    elif not sys.argv[1].isdigit():
        raise ValueError('You amount of days to be synced is not a number!')

    days = int(sys.argv[1])
    today = datetime.datetime.today()
    last_day = today + datetime.timedelta(days=days)

    nc_provider = CaldavProvider(nc_url)
    go_provider = GCalProvider()

    syncer = Syncer()
    syncer.register(SyncJob(nc_provider, go_provider, nc_to_g_source, nc_to_go_target, today, last_day))
    syncer.register(SyncJob(go_provider, nc_provider, go_to_nc_source, go_to_nc_target, today, last_day))
    syncer.sync()
