import sys

from src.sync import sync_next_days_to_nc, sync_next_days_to_go

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        days = int(sys.argv[1])
        sync_next_days_to_nc(days)
        sync_next_days_to_go(days)
