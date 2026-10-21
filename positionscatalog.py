"""The Positions workspace's public tab and method model.

Pure Python so menu aliases, displayed categories, and independent speculum
selection can be tested without opening wxPython windows.
"""

TABS = ('Zodiacal / speculum', 'Mundane', 'Motion', 'Chart data')
DESCRIPTIONS = (
    'Zodiacal positions and the full Placidus or Regiomontanus speculum. '
    'The chosen columns are controlled by Appearance II.',
    'Mundane house positions and the mundane Lot of Fortune.',
    'Longitude and latitude speeds of the planets.',
    'Sidereal time, obliquity of the ecliptic, and Julian day.',
)
MENU_TABS = {'onPositions': 0, 'onMunPos': 1, 'onSpeeds': 2, 'onMisc': 3}


def initial_speculum(primarydir, regiomontan):
    """Return the same default method as the original Positions window."""
    return int(primarydir == regiomontan)


def has_columns(speculums, method):
    """A valid speculum must have at least one enabled column."""
    return method in (0, 1) and any(speculums[method])
