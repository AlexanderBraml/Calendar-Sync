import sys

from sync import sync_to

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        days = int(sys.argv[1])
        sync_to(days, "go")
        sync_to(days, "nc")
