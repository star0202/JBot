import time
import datetime


def datetime_to_unix(n: datetime.datetime) -> int:
    return int(time.mktime(n.timetuple()))
