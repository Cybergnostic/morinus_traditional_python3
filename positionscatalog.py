"""The Positions workspace's public tab and method model.

Pure Python so menu aliases, displayed categories, and independent speculum
selection can be tested without opening wxPython windows.
"""

TABS = ('Overview', 'Speculum')
DESCRIPTIONS = (
    'Zodiacal and equatorial positions, motion, houses and mundane positions, '
    'the angles and lots, and the data of the chart.',
    'The full Placidus or Regiomontanus speculum, with your point of the primary directions when defined; '
    'Appearance II chooses its columns.',
)
# Morinus's Positions (F1) is the speculum; Mundane positions (F6), Speeds (F11)
# and Misc (F5) are all in the overview.
MENU_TABS = {'onPositions': 1, 'onMunPos': 0, 'onSpeeds': 0, 'onMisc': 0, 'onUserSpeculum': 1}


def initial_speculum(primarydir, regiomontan):
    """Return the same default method as the original Positions window."""
    return int(primarydir == regiomontan)


def has_columns(speculums, method):
    """A valid speculum must have at least one enabled column."""
    return method in (0, 1) and any(speculums[method])
