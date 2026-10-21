"""Chart themes: presets of the Colors options. Choosing one copies its
colours into the options; they can still be changed one by one in Colors."""

# planets: Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, nodes
# aspects: conjunction, sextile, square, trine, opposition
THEMES = {
	'Ink': {
		'clrframe': (0, 0, 0), 'clrsigns': (0, 0, 0), 'clrAscMC': (0, 128, 192),
		'clrhouses': (0, 0, 0), 'clrhousenumbers': (0, 0, 0), 'clraux': (0, 0, 128),
		'clraspect': [(213, 0, 0), (62, 133, 198), (213, 0, 0), (0, 128, 0), (213, 0, 0)],
		'clrplanets': [(0, 0, 0)] * 8,
		'clrLoF': (0, 128, 192), 'clrbackground': (255, 255, 255),
		'clrtable': (0, 0, 0), 'clrtexts': (0, 0, 0),
	},
	'Instrument': {
		'clrframe': (37, 43, 50), 'clrsigns': (36, 90, 123), 'clrAscMC': (36, 90, 123),
		'clrhouses': (122, 131, 140), 'clrhousenumbers': (122, 131, 140), 'clraux': (36, 90, 123),
		'clraspect': [(169, 77, 70), (36, 90, 123), (169, 77, 70), (63, 125, 90), (169, 77, 70)],
		'clrplanets': [(75, 85, 99), (47, 93, 138), (169, 77, 70), (140, 106, 31), (63, 125, 90), (122, 95, 42), (91, 110, 136), (90, 99, 109)],
		'clrLoF': (161, 138, 97), 'clrbackground': (255, 255, 255),
		'clrtable': (122, 131, 140), 'clrtexts': (37, 43, 50),
	},
	'Classic': {
		'clrframe': (0, 0, 255), 'clrsigns': (0, 0, 255), 'clrAscMC': (0, 0, 0),
		'clrhouses': (0, 0, 255), 'clrhousenumbers': (0, 0, 255), 'clraux': (0, 0, 128),
		'clraspect': [(0, 0, 128), (0, 128, 0), (128, 0, 0), (0, 128, 0), (128, 0, 0)],
		'clrplanets': [(0, 0, 0), (0, 0, 255), (178, 34, 34), (255, 215, 0), (0, 128, 0), (138, 43, 226), (0, 191, 255), (139, 54, 38)],
		'clrLoF': (205, 96, 144), 'clrbackground': (192, 192, 192),
		'clrtable': (0, 0, 0), 'clrtexts': (0, 0, 0),
	},
}
NAMES = ('Ink', 'Instrument', 'Classic')


def apply(options, name):
	for key, value in THEMES[name].items():
		setattr(options, key, value[:] if isinstance(value, list) else value)


def current(options):
	"""The name of the theme the colours match, or None if they were changed."""
	for name in NAMES:
		if all(getattr(options, k) == v for k, v in THEMES[name].items()):
			return name
	return None
