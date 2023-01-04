from datetime import datetime
from .objects import Raised


def equallize_datetime(dt: datetime):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=dt.tzinfo)


def equallize(obj):
    if isinstance(obj, Raised):
        return obj

    if isinstance(obj, (str, int, float, bool)):
        return obj
    elif obj is None:
        return obj
    elif isinstance(obj, (list, tuple, set)):
        return [equallize(x) for x in obj]
    elif isinstance(obj, dict):
        return {equallize(k): equallize(v) for k, v in obj.items()}
    elif isinstance(obj, datetime):
        return equallize_datetime(obj)
    else:
        return obj
