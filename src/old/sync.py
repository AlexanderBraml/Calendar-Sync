import datetime
from typing import List

from create_event import create_google, create_nc
from delete_event import delete_event_nc, delete_event_go
from get_day import get_day_nc, get_day_google, Calendar
from representation import compare_day, Event


def sync_to_google(events: List[Event]) -> None:
    for ev in events:
        create_google(ev)


def sync_to_nc(events: List[Event]) -> None:
    for ev in events:
        create_nc(ev)


def sync_to(amount: int, target: str) -> None:
    today = datetime.datetime.today()

    for i in range(amount + 1):
        day = today + datetime.timedelta(days=i)
        day_nc = get_day_nc(day, Calendar.FOR_GO_SYNC if target == 'go' else Calendar.FOR_NC_SYNC)
        day_go = get_day_google(day, Calendar.FOR_GO_SYNC if target == 'go' else Calendar.FOR_NC_SYNC)
        equal = compare_day(day_nc, day_go)

        if not equal:
            print(f'Day {day} not equal.\nNC: {day_nc}\nGO:{day_go}')
            for ev in (day_go if target == 'go' else day_nc):
                delete_event_go(ev) if target == 'go' else delete_event_nc(ev)
            sync_to_google(day_nc) if target == 'go' else sync_to_nc(day_go)
