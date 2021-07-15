"""
"""

import pytz
import datetime


def utcnow() -> datetime.datetime:
    """
    Returns current UTC datetime.
    """
    utc_now = datetime.datetime.now(tz=pytz.utc)
    return utc_now

def nznow() -> datetime.datetime:
    """
    Returns current NZT datetime.
    """
    nz_now = datetime.datetime.now(tz=pytz.timezone('NZ'))
    return nz_now 

def naive_dt_to_aware(
    naive_datetime: datetime.datetime, 
    timezone: str
    ) -> datetime.datetime:
    """
    Makes a naive datetime timezone aware.

    Args:
        - naive_datetime, the datetime to make timezone aware
        - timezone, the timezone to assign to the datetime

    Returns:
        - aware_dt, timezone aware datetime
    """
    local_timezone = pytz.timezone(timezone)
    aware_dt = local_timezone.localize(naive_datetime)
    return aware_dt

def localize_tz_to_utc(dt: datetime.datetime) -> datetime.datetime:
    """
    Should work for naive and aware datetimes.

    #TODO is this a good thing to work for both?
    """
    dt = dt.replace(tzinfo=pytz.utc)
    return dt