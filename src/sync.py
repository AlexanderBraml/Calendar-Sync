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


def sync_next_days_to_nc(amount: int) -> None:
    today = datetime.datetime.today()

    for i in range(amount + 1):
        day = today + datetime.timedelta(days=i)
        day_nc = get_day_nc(day, Calendar.FOR_NC_SYNC)
        day_go = get_day_google(day, Calendar.FOR_NC_SYNC)
        equal = compare_day(day_nc, day_go)

        print(equal)
        if not equal:
            for ev in day_nc:
                delete_event_nc(ev)
            sync_to_nc(day_go)


def sync_next_days_to_go(amount: int) -> None:
    today = datetime.datetime.today()

    for i in range(amount + 1):
        day = today + datetime.timedelta(days=i)
        day_nc = get_day_nc(day, Calendar.FOR_GO_SYNC)
        day_go = get_day_google(day, Calendar.FOR_GO_SYNC)
        equal = compare_day(day_nc, day_go)
        print(equal)
        if not equal:
            for ev in day_go:
                delete_event_go(ev)
            sync_to_google(day_nc)


if __name__ == '__main__':
    sync_next_days_to_nc(14)
    sync_next_days_to_go(14)
