"""Offline atlas: the GeoNames list of every place with 500 or more inhabitants,
with its coordinates, elevation and time zone, in Res/atlas.db (made by
tools/build_atlas.py). GeoNames data: CC BY 4.0, https://www.geonames.org"""

import os
import math
import sqlite3
import datetime
import unicodedata
from zoneinfo import ZoneInfo

FILENAME = os.path.join('Res', 'atlas.db')

# letters that do not decompose into a base letter and a diacritic
LETTERS = str.maketrans({'đ': 'd', 'ł': 'l', 'ø': 'o', 'ß': 'ss', 'æ': 'ae', 'œ': 'oe', 'ı': 'i', 'þ': 'th', 'ð': 'd', 'ħ': 'h'})

_db = None


def normalize(text):
	"""Search key: lower case, without diacritics, hyphens or apostrophes
	(Niš, NIS and nis give the same key)."""
	text = unicodedata.normalize('NFKD', text.casefold().translate(LETTERS))
	text = ''.join(c for c in text if not unicodedata.combining(c))
	return ' '.join(text.replace('-', ' ').replace("'", '').replace('’', '').split())


def _connect():
	global _db
	if _db is None and os.path.exists(FILENAME):
		_db = sqlite3.connect(FILENAME)
	return _db


def available():
	return _connect() is not None


def standard_offset(zone):
	"""The zone's standard offset from UTC this year, in hours (the smaller of
	its January and July offsets, so summer time is not included)."""
	try:
		z = ZoneInfo(zone)
	except Exception:
		return 0.0
	year = datetime.date.today().year
	return min(datetime.datetime(year, m, 15, 12, tzinfo=z).utcoffset() for m in (1, 7)).total_seconds() / 3600.0


def search(query, limit=100):
	"""Places whose name, in any spelling GeoNames knows, starts with the query:
	exact names first, then by population. 'Name, region or country' narrows the
	search (e.g. 'Springfield, Illinois' or 'Nis, RS').

	Returns tuples in the order of geonames.Geonames: name, longitude, latitude,
	country code, 'region, country', altitude, standard GMT offset (hours)."""
	db = _connect()
	if db is None:
		return []
	name, _, where = query.partition(',')
	key = normalize(name)
	if not key:
		return []
	sql = '''SELECT p.name, p.lon, p.lat, p.cc, p.country, p.admin1, p.alt, p.tz, MAX(n.key = :key) AS exact
		FROM names n JOIN places p ON p.id = n.id
		WHERE n.key >= :key AND n.key < :end'''
	args = {'key': key, 'end': key+'\U0010ffff', 'limit': limit}
	where = normalize(where)
	if where:
		sql += ' AND (p.ckey LIKE :where OR p.akey LIKE :where OR lower(p.cc) = :cc)'
		args['where'] = where+'%'
		args['cc'] = where
	sql += ' GROUP BY p.id ORDER BY exact DESC, p.pop DESC LIMIT :limit'
	places = []
	for name, lon, lat, cc, country, admin1, alt, tz, exact in db.execute(sql, args):
		region = admin1+', '+country if admin1 else country
		places.append((name, lon, lat, cc, region, alt, standard_offset(tz)))
	return places


def zone_at(lat, lon, km=30.0):
	"""The time zone of the nearest place in the atlas, if one is within km."""
	db = _connect()
	if db is None:
		return None
	dlat = km/111.0
	dlon = dlat/max(math.cos(math.radians(lat)), 0.01)
	best = None
	for plat, plon, tz in db.execute('SELECT lat, lon, tz FROM places WHERE lat BETWEEN ? AND ? AND lon BETWEEN ? AND ?', (lat-dlat, lat+dlat, lon-dlon, lon+dlon)):
		x = math.radians(plon-lon)*math.cos(math.radians((plat+lat)/2.0))
		d = 6371.0*math.hypot(x, math.radians(plat-lat))
		if d <= km and (best is None or d < best[0]):
			best = (d, tz)
	return best[1] if best else None
