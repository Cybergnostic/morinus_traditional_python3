"""Planetary hours and Rise/Set workspace navigation contracts."""
TABS = ('Planetary hours', 'Rise, set and culmination')
ALIASES = {'onPlanetaryHours': 0, 'onRiseSet': 1}


def has_both_tables():
    return len(TABS) == 2 and set(ALIASES.values()) == {0, 1}
