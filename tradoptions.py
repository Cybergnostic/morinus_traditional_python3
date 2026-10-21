"""Options of the techniques added to this version, kept in Opts/traditional.json
(beside Morinus's own .opt files, which the Windows Morinus still reads)."""

import os
import json
import copy

FILENAME = os.path.join('Opts', 'traditional.json')

DEFAULTS = {
	# zodiacal releasing
	'zr_yeardays': 360.0,		# 360 (Valens) or 365.25
	'zr_years': 110,
	# decennials
	'dec_start': 'sect',		# sect, sun, moon, asc (first planet after it), fortune (first planet after it)
	'dec_monthdays': 30.0,		# 30 or 30.4375 (a twelfth of a year of 365.25 days)
	'dec_years': 110,
	# circumambulation
	'ca_point': 'asc',		# asc (oblique ascension), mc (right ascension)
	'ca_key': 'ptolemy',		# ptolemy (1 degree = 1 year), naibod (0.98565 degrees = 1 year)
	'ca_rays': [True, True, True, True, True],	# conjunction, sextile, square, trine, opposition
	'ca_years': 100,
	# heliacal phenomena
	'hel_phasisdays': 7,
	'hel_stationdays': 30,
	'hel_pressure': 0.0,		# hPa, 0: standard (1013.25)
	'hel_temperature': 15.0,	# degrees C
	'hel_humidity': 40.0,		# percent
	'hel_age': 36,			# years of the observer
	# fixed stars on the angles
	'fsa_minutes': 30,
	'fsa_paranminutes': 4,
	# antiscia table
	'ant_rule': 'degrees',		# degrees (whole degrees adding up to 29), orb (conjunction orbs)
	# places and time zones
	'place_atlas': True,
	'place_online': True,
	'place_username': 'morinastro',
	'place_timezone': True,		# offer the birth date's time zone after choosing a place
	# chart drawing
	'chart_smooth': True,		# antialiased lines and circles
	'chart_lines': 'fine',		# fine, or morinus (the weights of Morinus 6)
	'show_toolbar': True,
	'table_zoom': 1.0,
	'show_sidebar': True,
	# windows and errors
	'win_remember': True,
	'err_show': True,
}

_values = None


def load():
	global _values
	_values = copy.deepcopy(DEFAULTS)
	try:
		with open(FILENAME, encoding='utf-8') as f:
			saved = json.load(f)
		_values.update({k: v for k, v in saved.items() if k in DEFAULTS})
	except (OSError, ValueError):
		pass
	return _values


def get(key):
	if _values is None:
		load()
	return _values[key]


def values():
	if _values is None:
		load()
	return dict(_values)


def set(changes):
	if _values is None:
		load()
	_values.update(changes)


def save():
	try:
		with open(FILENAME, 'w', encoding='utf-8') as f:
			json.dump(_values, f, indent=1, sort_keys=True)
		return True
	except OSError:
		return False
