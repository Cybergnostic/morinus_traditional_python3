"""Heliacal phenomena and phasis: for each planet the visibility events nearest
the birth (morning first and evening last, and for Venus, Mercury and the Moon
evening first and morning last) and the stations, from the Swiss Ephemeris
(swe_heliacal_ut: arcus visionis, with the atmosphere and observer of the options).
A planet makes its phasis when such an event falls within some days of the
birth (Options > Heliacal phenomena: 7 in the Hellenistic texts).

Times are Julian days (UT)."""

import astrology
import planets
import tradoptions

P = planets.Planets
NAMES = {P.SATURN: 'saturn', P.JUPITER: 'jupiter', P.MARS: 'mars', P.VENUS: 'venus', P.MERCURY: 'mercury', P.MOON: 'moon'}
SWE = {P.SATURN: astrology.SE_SATURN, P.JUPITER: astrology.SE_JUPITER, P.MARS: astrology.SE_MARS, P.VENUS: astrology.SE_VENUS, P.MERCURY: astrology.SE_MERCURY, P.MOON: astrology.SE_MOON}
MORNING_FIRST, EVENING_LAST, EVENING_FIRST, MORNING_LAST = 1, 2, 3, 4
EVENTNAMES = {MORNING_FIRST: 'morning first (heliacal rising)', EVENING_LAST: 'evening last (heliacal setting)',
	EVENING_FIRST: 'evening first', MORNING_LAST: 'morning last'}
EVENTS = {P.SATURN: (1, 2), P.JUPITER: (1, 2), P.MARS: (1, 2), P.VENUS: (1, 2, 3, 4), P.MERCURY: (1, 2, 3, 4), P.MOON: (3, 4)}


def event(planet, eventtype, start, place):
	"""The first such event after start (UT Julian day), or None."""
	o = tradoptions.get
	# atmosphere: pressure, temperature, humidity, extinction (0: from the others); observer: age, Snellen ratio
	ret, dret, serr = astrology.swe_heliacal_ut(start, place.lon, place.lat, float(place.altitude),
		float(o('hel_pressure')), float(o('hel_temperature')), float(o('hel_humidity')), 0.0,
		float(o('hel_age')), 1.0, 0.0, 0.0, 0.0, 0.0, NAMES[planet], eventtype, astrology.SEFLG_SWIEPH)
	if ret[0] < 0 or dret[0] <= 0.0:
		return None
	return dret[0]


def around(planet, eventtype, jd, place):
	"""The last such event before jd and the first after it (either may be None)."""
	before = after = None
	t = jd - (40.0 if planet == P.MOON else 800.0)
	for i in range(30):
		e = event(planet, eventtype, t, place)
		if e is None:
			break
		if e < jd:
			before, t = e, e + 1.0
		else:
			after = e
			break
	return before, after


def stations(planet, jd):
	"""Stations within the days of the options of jd: (UT Julian day, turning retrograde?)."""
	if planet == P.MOON:
		return []
	STATION_DAYS = int(tradoptions.get('hel_stationdays'))
	out = []
	speed = lambda t: astrology.swe_calc_ut(t, SWE[planet], astrology.SEFLG_SWIEPH | astrology.SEFLG_SPEED)[1][3]
	prev = speed(jd - STATION_DAYS)
	for day in range(-STATION_DAYS + 1, STATION_DAYS + 1):
		v = speed(jd + day)
		if (prev > 0.0) != (v > 0.0):
			# halve the day to the hour
			lo, hi = jd + day - 1, jd + day
			for k in range(5):
				mid = (lo + hi) / 2.0
				if (speed(mid) > 0.0) == (prev > 0.0):
					lo = mid
				else:
					hi = mid
			out.append(((lo + hi) / 2.0, prev > 0.0))
		prev = v
	return out


def phenomena(chrt):
	"""Rows: (planet, description, before, after); before/after are Julian days or None."""
	rows = []
	for planet in (P.SATURN, P.JUPITER, P.MARS, P.VENUS, P.MERCURY, P.MOON):
		for ev in EVENTS[planet]:
			before, after = around(planet, ev, chrt.time.jd, chrt.place)
			rows.append((planet, EVENTNAMES[ev], before, after))
		for jd, retro in stations(planet, chrt.time.jd):
			name = 'station, turning retrograde' if retro else 'station, turning direct'
			rows.append((planet, name, jd if jd < chrt.time.jd else None, jd if jd >= chrt.time.jd else None))
	return rows
