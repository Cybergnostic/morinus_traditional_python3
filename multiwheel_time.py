"""Calendar-safe date steps for the multiwheel transit controller.

The controller uses the source chart's civil date and timezone settings;
the caller creates a new Morinus Chart without modifying the source window.
"""

import calendar
from datetime import datetime, timedelta


UNITS = ('Year', 'Month', 'Day', 'Hour', 'Min', 'Sec')


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
