"""Some basic utility functions that help out with the Skytap API."""

from datetime import datetime
from datetime import timedelta
from datetime import tzinfo
import json


def error(err):
    """Convert an error message into JSON."""
    return json.dumps({"error": err})


def convert_date(date_str):
    """Convert a Skytap date string to a datetime object.

    Sample from Skytap: 2015/09/08 00:26:48 -0800
    """
    naive_date_str, _, offset_str = date_str.rpartition(' ')
    naive_dt = datetime.strptime(naive_date_str, '%Y/%m/%d %H:%M:%S')
    offset = int(offset_str[-4:-2]) * 60 + int(offset_str[-2:])
    if offset_str[0] == "-":
        offset = -offset
    dt = naive_dt.replace(tzinfo=FixedOffset(offset))
    return dt


class FixedOffset(tzinfo):

    """Fixed offset in minutes: `time = utc_time + utc_offset`."""

    def __init__(self, offset):
        """Given offset, built timezone info."""
        self.__offset = timedelta(minutes=offset)
        hours, minutes = divmod(offset, 60)
        # NOTE: the last part is to remind about deprecated POSIX GMT+h
        #  timezones that have the opposite sign in the name;
        #  the corresponding numeric value is not used e.g., no minutes
        self.__name = '<%+03d%02d>%+d' % (hours, minutes, -hours)

    def utcoffset(self, dt=None):
        """Return UTC offset."""
        return self.__offset

    def tzname(self, dt=None):
        """Return timezone name."""
        return self.__name

    def dst(self, dt=None):
        """Ignore daylight savings time."""
        return timedelta(0)

    def __repr__(self):
        """String representation of the offset."""
        return 'FixedOffset(%d)' % (self.utcoffset().total_seconds() / 60)
