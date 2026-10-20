"""Circumambulation of the Ascendant through the bounds (Ptolemy, Tetrabiblos III;
Valens): the Ascendant is directed under the oblique ascensions of the birth
latitude, one year for each degree (Ptolemy's key). The lord of each bound it
enters is the distributor; the planets whose bodies or rays (sextile, square,
trine, opposition) it meets are the participants.

The bounds are those chosen in Options > Terms. Oblique ascensions are
calculated directly (OA = RA - ascensional difference) for points on the
ecliptic."""

import math
import planets
import houses
import util
import tradoptions

ASPECTS = ((0, 'L'), (60, 'M'), (90, 'N'), (120, 'O'), (180, 'P'))	# with their Morinus.ttf letters
YEAR = 365.2421897
NAIBOD = 0.98564733	# degrees of right ascension of the Sun's mean daily motion: a year


class NotAvailable(Exception):
	pass


class Event:
	def __init__(self, years, lon, distributor=None, participant=None, aspect=None):
		self.years = years
		self.lon = lon			# tropical longitude reached
		self.distributor = distributor	# planet: the Ascendant enters its bound
		self.participant = participant	# planet whose body/ray the Ascendant meets
		self.aspect = aspect		# index into ASPECTS


def right_ascension(lon, obl):
	l, e = math.radians(lon), math.radians(obl)
	return math.degrees(math.atan2(math.sin(l) * math.cos(e), math.cos(l))) % 360.0


def oblique_ascension(lon, obl, lat):
	"""OA of a point on the ecliptic (degrees) under geographic latitude lat."""
	l, e, phi = math.radians(lon), math.radians(obl), math.radians(lat)
	ra = math.degrees(math.atan2(math.sin(l) * math.cos(e), math.cos(l))) % 360.0
	decl = math.asin(math.sin(e) * math.sin(l))
	x = math.tan(phi) * math.tan(decl)
	if abs(x) >= 1.0:
		raise NotAvailable('the ecliptic does not rise and set at this latitude')
	return (ra - math.degrees(math.asin(x))) % 360.0


def bounds(options, ayanamsha):
	"""(tropical start longitude, lord) of every bound of the zodiac."""
	table = options.terms[options.selterm]
	out = []
	for sign in range(12):
		start = sign * 30.0
		for lord, length in table[sign]:
			lon = start + (ayanamsha if options.ayanamsha != 0 else 0.0)
			out.append((util.normalize(lon), lord))
			start += length
	return out


def circumambulation(chrt, years=None):
	"""Events in order of time: bounds entered and rays met, for the point,
	key and rays of the options (Options > Circumambulation)."""
	years = years or tradoptions.get('ca_years')
	key = NAIBOD if tradoptions.get('ca_key') == 'naibod' else 1.0
	rays = tradoptions.get('ca_rays')
	obl = chrt.obl[0]
	lat = chrt.place.lat
	if tradoptions.get('ca_point') == 'mc':
		asc = chrt.houses.ascmc[houses.Houses.MC]
		ra0 = chrt.houses.ascmc[houses.Houses.ARMC]

		def arc(lon):
			return (right_ascension(lon, obl) - ra0) % 360.0 / key
	else:
		if abs(lat) >= 90.0 - obl:
			raise NotAvailable('the ecliptic does not rise and set at this latitude')
		asc = chrt.houses.ascmc[houses.Houses.ASC]
		oa0 = (chrt.houses.ascmc[houses.Houses.ARMC] + 90.0) % 360.0

		def arc(lon):
			return (oblique_ascension(lon, obl, lat) - oa0) % 360.0 / key

	events = []
	bnds = bounds(chrt.options, chrt.ayanamsha)
	# the bound the Ascendant is in at birth: the nearest bound start before it
	current = min(bnds, key=lambda b: util.normalize(asc - b[0]))
	events.append(Event(0.0, asc, distributor=current[1]))
	for lon, lord in bnds:
		if lon != current[0]:
			events.append(Event(arc(lon), lon, distributor=lord))
	for pl in range(planets.Planets.PLANETS_NUM):
		plon = chrt.planets.planets[pl].data[planets.Planet.LON]
		for i, (angle, letter) in enumerate(ASPECTS):
			if not rays[i]:
				continue
			for sign in ((1,) if angle in (0, 180) else (1, -1)):
				point = util.normalize(plon + sign * angle)
				events.append(Event(arc(point), point, participant=pl, aspect=i))
	return sorted((e for e in events if e.years <= years), key=lambda e: e.years)


def date(chrt, years):
	return chrt.time.jd + years * YEAR
