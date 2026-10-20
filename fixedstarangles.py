"""Fixed stars on the angles: the stars rising, culminating, setting or
anticulminating near the moment of birth (angle at birth), and the
paranatellonta of the birth day: a planet and a star on angles at the same
time. The stars are those chosen in Options > Fixed stars; the times are the
Swiss Ephemeris's (swe_rise_trans), with refraction.

Times are Julian days (UT)."""

import astrology
import planets
import util
import starnames

ANGLES = ((astrology.SE_CALC_RISE, 'Asc', 'rising'), (astrology.SE_CALC_MTRANSIT, 'MC', 'culminating'),
	(astrology.SE_CALC_SET, 'Dsc', 'setting'), (astrology.SE_CALC_ITRANSIT, 'IC', 'anticulminating'))
AT_BIRTH_MINUTES = 30.0
PARAN_MINUTES = 4.0


def events(jd0, jd1, place, ipl=0, star=''):
	"""(angle index, UT Julian day) of every crossing of an angle in [jd0, jd1)."""
	out = []
	for ai, (rsmi, short, name) in enumerate(ANGLES):
		t = jd0
		for i in range(4):
			ret, tret, serr = astrology.swe_rise_trans(t, ipl, star, astrology.SEFLG_SWIEPH, rsmi, place.lon, place.lat, float(place.altitude), 0.0, 10.0)
			if ret < 0 or tret <= 0.0 or tret >= jd1:
				break	# -2: circumpolar, never rises or sets
			out.append((ai, tret))
			t = tret + 0.01
	return out


def starname(nom, jd):
	star = starnames.lookup(nom, jd, astrology.SEFLG_SWIEPH)
	return star[0] if star else nom


def localday(chrt):
	"""UT Julian days of the local midnights before and after the birth."""
	off = chrt.time.localoffset()
	start = int(chrt.time.jd + off + 0.5) - 0.5 - off
	return start, start + 1.0


def at_birth(chrt):
	"""(star name, angle index, UT Julian day) within AT_BIRTH_MINUTES of the birth, nearest first."""
	jd = chrt.time.jd
	window = AT_BIRTH_MINUTES / 1440.0
	out = []
	for nom in chrt.options.fixedstars:
		for ai, t in events(jd - 0.5, jd + 0.5, chrt.place, star=',' + starnames.ALIASES.get(nom, nom)):
			if abs(t - jd) <= window:
				out.append((starname(nom, jd), ai, t))
	return sorted(out, key=lambda e: abs(e[2] - jd))


def parans(chrt):
	"""(planet, planet's angle, star name, star's angle, planet's time, star's time) on the birth day."""
	jd0, jd1 = localday(chrt)
	orb = PARAN_MINUTES / 1440.0
	plevents = [(pl, ai, t) for pl in range(planets.Planets.PLANETS_NUM)
		for ai, t in events(jd0, jd1, chrt.place, ipl=util.mapChaldeanToModern(pl))]
	out = []
	for nom in chrt.options.fixedstars:
		name = None
		for sai, st in events(jd0 - orb, jd1 + orb, chrt.place, star=',' + starnames.ALIASES.get(nom, nom)):
			for pl, pai, pt in plevents:
				if abs(pt - st) <= orb:
					name = name or starname(nom, chrt.time.jd)
					out.append((pl, pai, name, sai, pt, st))
	return sorted(out, key=lambda e: e[4])
