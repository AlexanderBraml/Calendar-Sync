# Generic-Calendar-Sync

Lets you sync events from one or multiple source calendars to one target calendar very easily.

The original goal of this project was to sync events from a caldav calendar to Google Calendar. Once an early prototype was made, I wanted to make the design more flexible to use other calendars so I designed a generic Calendar Provider which is used to sync events. You can implement your own provider by implementing a concrete subclass of `CalProvider.py`. Already implemented are `CaldavProvider.py`, which can sync events from any caldav url, and `GCalProvider.py`, which syncs from and to Google Calendar, given credentials and a token.

## How To Sync
Syncing from one calendar to the other is very easy. You just have to create one or multiple Sync Jobs and then just sync.
Here is an example which syncs all events in the next 10 days from a caldav source to the primary Google Calendar:
```python3
import datetime

from src.Sync import SyncJob, Syncer
from src.CaldavProvider import CaldavProvider
from src.GCalProvider import GCalProvider

if __name__ == '__main__':
    dav_provider = CaldavProvider('https://user:password@cal.domain.com/dav/calendars/')
    g_provider = GCalProvider()

    syncer = Syncer()
    syncer.register(
        SyncJob(dav_provider, g_provider, ['Private', 'Appointments', 'Work'], 'id12453@group.calendar.google.com',
                datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=10)))
    syncer.sync()
```
In the case of Google Calendar, you first have to get a token and credentials. Please refer to the official [Google Calendar API Documentation](https://developers.google.com/calendar/api/quickstart/python) for further reference.

## How This Works
The sync mechanism is very simple. For each day which should be synced, the program retrieves the events of this day in the source calendar.
It then gets all events of this day in the target calendar, if the two are equal, then there is no further action.
Otherwise all events in this day in the target calendar are deleted and are replaced by the events from the source calendar.
There are surely other more efficient ways to do this, but this is very simple and works reliably.

## What This Does Not Do
This program does not sync two ways. You cannot keep two calendar in sync as of today. You can take this code as a starting point and implement it yourself if you need it. It was not a priority for me.

Currently full day events are not supported. Maybe I'll work on them in the future and integrate them.
