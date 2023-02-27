import datetime

from src.create_event import create_google, create_nc
from src.get_day import get_day_nc, get_day_google
from src.representation import compare_day


def sync_to_google() -> None:
    events = get_day_nc(datetime.datetime(2023, 2, 28))
    for ev in events:
        create_google(ev)


def sync_to_nc() -> None:
    events = get_day_google(datetime.datetime(2023, 2, 28))
    for ev in events:
        create_nc(ev)


if __name__ == '__main__':
    # sync_to_nc()
    print(compare_day(get_day_nc(datetime.datetime(2023, 2, 28)), get_day_google(datetime.datetime(2023, 2, 28))))
