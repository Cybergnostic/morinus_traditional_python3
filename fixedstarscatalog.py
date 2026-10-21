"""Fixed Stars workspace navigation; each method retains its own orb rule."""
TABS = ('Star positions', 'Conjunctions and aspects', 'Angles and paranatellonta')
DESCRIPTIONS = (
    'Selected fixed-star positions: longitude, latitude, right ascension and declination.',
    'Original fixed-star aspect matrix and its configured astrological orbs.',
    'Birth-time angle contacts and birth-day paranatellonta; distinct minute-based tolerances.',
)
ALIASES = {'onFixedStars': 0, 'onFixedStarsAsps': 1, 'onStarAngles': 2}


def is_selected(selected):
    return bool(selected)
