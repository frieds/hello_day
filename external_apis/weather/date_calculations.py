from datetime import timedelta


def round_datetime_to_next_hour(datetime_obj):
    """
    Round a datetime object to the next hour.
    If the minute is greater than or equal to 40, the hour is rounded up.
    Otherwise, the hour is rounded down.
    """
    if datetime_obj.minute >= 40:
        # this handles edge condition of hour 23 utc + 1 hour = hour 0 (not hour 24)
        datetime_obj += timedelta(hours=1)
    datetime_obj = datetime_obj.replace(minute=0, second=0, microsecond=0)
    return datetime_obj
