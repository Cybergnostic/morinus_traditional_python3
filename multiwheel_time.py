"""Calendar-safe date steps for the multiwheel transit controller.

The controller uses the source chart's civil date and timezone settings;
the caller creates a new Morinus Chart without modifying the source window.
"""

import calendar
from datetime import datetime, timedelta


UNITS = ('Year', 'Month', 'Day', 'Hour', 'Min', 'Sec')


def validate(parts, julian=False):
    """Check a manually entered civil time, including Julian leap days.

    Morinus also supports Julian and BC charts, so Gregorian datetime alone
    cannot validate the dates accepted by its chart.Time constructor.
    """
    year, month, day, hour, minute, second = parts
    if not all(isinstance(value, int) for value in parts):
        raise ValueError('Date and time values must be integers')
    if not 1 <= year <= 9999 or not 1 <= month <= 12:
        raise ValueError('Year or month is out of range')
    leap = (year % 4 == 0 if julian else
            year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
    month_days = (31, 29 if leap else 28, 31, 30, 31, 30,
                  31, 31, 30, 31, 30, 31)
    if not 1 <= day <= month_days[month - 1]:
        raise ValueError('Day is out of range for the selected month')
    if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
        raise ValueError('Hour, minute or second is out of range')
    return parts


def shift(parts, unit, forward):
    """Move a (year, month, day, hour, minute, second) tuple one step.

    Changing a month/year clamps the day (31 January -> 28 February),
    matching the behavior of Morinus's existing transit arrow shortcuts.
    """
    year, month, day, hour, minute, second = parts
    delta = 1 if forward else -1
    if unit == 'Year':
        year += delta
        if not 1 <= year <= 9999:
            return None
        day = min(day, calendar.monthrange(year, month)[1])
        return year, month, day, hour, minute, second
    if unit == 'Month':
        index = year * 12 + month - 1 + delta
        year, offset = divmod(index, 12)
        month = offset + 1
        if not 1 <= year <= 9999:
            return None
        day = min(day, calendar.monthrange(year, month)[1])
        return year, month, day, hour, minute, second
    if unit not in ('Day', 'Hour', 'Min', 'Sec'):
        raise ValueError('Unknown transit step: %s' % unit)
    try:
        keyword = {
            'Day': 'days', 'Hour': 'hours', 'Min': 'minutes', 'Sec': 'seconds'
        }[unit]
        value = datetime(*parts) + timedelta(**{keyword: delta})
    except (OverflowError, ValueError):
        return None
    return (value.year, value.month, value.day,
            value.hour, value.minute, value.second)
