"""Hyleg and alcocoden by the traditional method, without wx so it can be
tested headless.

Hyleg, by day: (1) the Sun in I, XI or X, or in VII or IX in a masculine sign;
(2) the Moon in I, II, III or VII, or in X, XI, IV or V in a feminine sign;
(3) after a new Moon the Ascendant (seen by one of its rulers or by the Moon),
otherwise Fortune if angular or succedent; after a full Moon Fortune first,
then the Ascendant; (4) the degree of the prenatal syzygy.
By night: (1) the Moon in I, XI or X, or in VII or IX in a feminine sign;
(2) the Sun in I or II in a masculine sign, or in IV, V or VII; (3) and (4) as
by day. A candidate is the hyleg only if one of its rulers sees it by a
classical aspect of the signs; the Moon under the beams and an eclipsed Sun
cannot be the hyleg. The places are whole-sign houses from the Ascendant
(checked on the charts of Elizabeth II, Steve Jobs and Princess Diana), or
Porphyry houses (Options); the strength of the alcocoden (angular, succedent,
cadent) is by Porphyry, the trisection of the quadrants.

Alcocoden: a planet with dignity in the place of the hyleg (domicile,
exaltation, triplicity, term; not the face) that aspects it; with several, the
one with the highest dignity there (domicile, exaltation, triplicity, term:
Steve Jobs's Jupiter by domicile before Venus by exaltation, triplicity and
term), then more dignity, then the closer aspect, then the stronger house.

No length of life is computed here: only the planetary years
of the alcocoden and the conditions the astrologer weighs.
"""

import astrology
import planets
import tradoptions

SATURN, JUPITER, MARS, SUN, VENUS, MERCURY, MOON = range(7)
NAMES = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')
# greater, middle, lesser years
YEARS = {SATURN: (57, 43.5, 30), JUPITER: (79, 45.5, 12), MARS: (66, 40.5, 15), SUN: (120, 69.5, 19),
	VENUS: (82, 45, 8), MERCURY: (76, 48, 20), MOON: (108, 66.5, 25)}
TRIPLS = (0, 3, 1, 2, 0, 3, 1, 2, 0, 3, 1, 2)	# fire, air, water, earth as options.trips
ASPECT_SIGNS = {0: 0, 2: 60, 10: 60, 3: 90, 9: 90, 4: 120, 8: 120, 6: 180}
ANGULAR, SUCCEDENT, CADENT = 'angular', 'succedent', 'cadent'
UNDER_BEAMS = 15.0
PORPHYRY = ord('O')


class Candidate:
	def __init__(self, key, name, lon):
		self.key = key		# 'sun', 'moon', 'asc', 'fortune', 'syzygy'
		self.name = name
		self.lon = lon
		self.house = None
		self.accepted = False
		self.reasons = []	# English texts (translated by the window)
		self.seenby = []	# (planet, aspect angle)


class Result:
	def __init__(self):
		self.day = True
		self.newmoon = True
		self.candidates = []	# in the order examined
		self.hyleg = None		# the accepted Candidate
		self.alcocoden = None	# planet index
		self.alcocodens = []	# (planet, dignity points, dignities, aspect, orb, house, strength) sorted best first
		self.years = None		# (greater, middle, lesser)
		self.strength = None
		self.conditions = []	# texts about the alcocoden


def sign(chrt, lon):
	if chrt.options.ayanamsha != 0:
		lon -= chrt.ayanamsha
	return int(lon % 360.0 // 30.0)


def porphyry_cusps(chrt):
	res, cusps, ascmc = astrology.swe_houses_ex(chrt.time.jd, 0, chrt.place.lat, chrt.place.lon, PORPHYRY)
	return cusps[1:13]


def house_of(cusps, lon):
	for i in range(12):
		a, b = cusps[i], cusps[(i + 1) % 12]
		if (lon - a) % 360.0 < (b - a) % 360.0:
			return i + 1
	return 1


def strength(house):
	if house in (1, 4, 7, 10):
		return ANGULAR
	if house in (2, 5, 8, 11):
		return SUCCEDENT
	return CADENT


def dignities(opts, s, deg):
	"""{planet: [(kind, points)]} of the rulers of a degree: domicile 5,
	exaltation 4, triplicity 3 (all three rulers), term 2; no face."""
	scores = opts.dignityscores
	out = {}
	def add(pl, kind, pts):
		if 0 <= pl < 7:
			out.setdefault(pl, []).append((kind, pts))
	for pl in range(7):
		if opts.dignities[pl][0][s]:
			add(pl, 'domicile', scores[0])
		if opts.dignities[pl][1][s]:
			add(pl, 'exaltation', scores[1])
	for pl in opts.trips[opts.seltrip][TRIPLS[s]]:
		if pl not in [p for p, kinds in out.items() if any(k == 'triplicity' for k, x in kinds)]:
			add(pl, 'triplicity', scores[2])
	total = 0.0
	for pl, width in opts.terms[opts.selterm][s]:
		total += width
		if total > deg:
			add(pl, 'term', scores[3])
			break
	return out


def sign_aspect(s1, s2):
	return ASPECT_SIGNS.get((s1 - s2) % 12)


def orb(lon1, lon2, angle):
	sep = abs((lon1 - lon2 + 180.0) % 360.0 - 180.0)
	return abs(sep - angle)


def masculine(s):
	return s % 2 == 0


def sun_eclipsed(chrt):
	try:
		ret, attr, serr = astrology.swe_sol_eclipse_how(chrt.time.jd, astrology.SEFLG_SWIEPH, chrt.place.lon, chrt.place.lat, float(chrt.place.altitude))
		return ret[0] > 0 and attr[0] > 0.0
	except Exception:
		return False


def calculate(chrt):
	opts = chrt.options
	pls = chrt.planets.planets
	lon = [pls[i].data[planets.Planet.LON] for i in range(7)]
	cusps = porphyry_cusps(chrt)
	wholesign = tradoptions.get('hyleg_places') == 'wholesign'
	ascsign = sign(chrt, chrt.houses.ascmc[0])
	res = Result()
	res.day = chrt.isDaySect()
	res.newmoon = bool(chrt.syzygy.newmoon) if chrt.syzygy is not None else True
	asc = chrt.houses.ascmc[0]
	fortune = chrt.lots.lots[0][4]	# Lot of Fortune (lots.Lots.LON)

	def seen(c, moon_too=False):
		"""Rulers (or the Moon) seeing the candidate by a classical aspect of the signs."""
		s = sign(chrt, c.lon)
		rulers = dignities(opts, s, (c.lon - (chrt.ayanamsha if opts.ayanamsha else 0.0)) % 30.0)
		seers = []
		for pl in sorted(rulers):
			asp = sign_aspect(sign(chrt, lon[pl]), s)
			if asp is not None and not (c.key == NAMES[pl].lower()):
				seers.append((pl, asp))
		if moon_too and MOON not in [p for p, a in seers]:
			asp = sign_aspect(sign(chrt, lon[MOON]), s)
			if asp is not None:
				seers.append((MOON, asp))
		c.seenby = seers
		return bool(seers)

	def place(c):
		if wholesign:
			c.house = (sign(chrt, c.lon) - ascsign) % 12 + 1
		else:
			c.house = house_of(cusps, c.lon)
		return c.house

	def luminary(key, pl):
		c = Candidate(key, NAMES[pl], lon[pl])
		h = place(c)
		s = sign(chrt, c.lon)
		gender_ok = masculine(s) if pl == SUN else not masculine(s)
		gender = 'masculine' if masculine(s) else 'feminine'
		if pl == SUN:
			free, needgender = ((1, 11, 10), (7, 9)) if res.day else ((4, 5, 7), (1, 2))
		else:
			free, needgender = ((1, 2, 3, 7), (10, 11, 4, 5)) if res.day else ((1, 11, 10), (7, 9))
		if h in free:
			ok = True
			c.reasons.append(('in house %d', h))
		elif h in needgender:
			ok = gender_ok
			c.reasons.append(('in house %d, in a %s sign', h, gender))
		else:
			ok = False
			c.reasons.append(('in house %d: not a hylegical place', h))
		if ok and pl == MOON and abs((lon[MOON] - lon[SUN] + 180.0) % 360.0 - 180.0) < UNDER_BEAMS:
			ok = False
			c.reasons.append(('under the beams',))
		if ok and pl == SUN and sun_eclipsed(chrt):
			ok = False
			c.reasons.append(('eclipsed',))
		return c, ok

	def check(c, ok, moon_too=False):
		if ok:
			if seen(c, moon_too):
				c.reasons.append(('seen by %s', ', '.join(NAMES[p] for p, a in c.seenby)))
			else:
				ok = False
				c.reasons.append(('none of its rulers sees it',))
		c.accepted = ok
		res.candidates.append(c)
		if ok and res.hyleg is None:
			res.hyleg = c
		return ok

	order = (SUN, MOON) if res.day else (MOON, SUN)
	for pl in order:
		c, ok = luminary(NAMES[pl].lower(), pl)
		if check(c, ok):
			break
	if res.hyleg is None:
		ca = Candidate('asc', 'Ascendant', asc)
		place(ca)
		cf = Candidate('fortune', 'Lot of Fortune', fortune)
		hf = place(cf)
		fok = strength(hf) != CADENT
		if not fok:
			cf.reasons.append(('in house %d: cadent', hf))
		else:
			cf.reasons.append(('in house %d', hf))
		ca.reasons.append(('the prenatal syzygy was a %s', 'new Moon' if res.newmoon else 'full Moon'))
		pair = ((ca, True, True), (cf, fok, False)) if res.newmoon else ((cf, fok, False), (ca, True, True))
		for c, ok, moon_too in pair:
			if check(c, ok, moon_too):
				break
	if res.hyleg is None and chrt.syzygy is not None:
		cs = Candidate('syzygy', 'Prenatal syzygy', chrt.syzygy.lon)
		place(cs)
		check(cs, True)

	if res.hyleg is not None:
		alcocoden(chrt, res, lon, cusps)
	return res


def alcocoden(chrt, res, lon, cusps):
	opts = chrt.options
	h = res.hyleg
	s = sign(chrt, h.lon)
	rulers = dignities(opts, s, (h.lon - (chrt.ayanamsha if opts.ayanamsha else 0.0)) % 30.0)
	rows = []
	order = {ANGULAR: 0, SUCCEDENT: 1, CADENT: 2}
	for pl, kinds in rulers.items():
		if h.key == NAMES[pl].lower():
			continue	# a luminary hyleg is not its own alcocoden here
		asp = sign_aspect(sign(chrt, lon[pl]), s)
		if asp is None:
			continue
		house = house_of(cusps, lon[pl])
		rows.append((pl, sum(p for k, p in kinds), [k for k, p in kinds], asp, orb(lon[pl], h.lon, asp), house, strength(house)))
	rank = ('domicile', 'exaltation', 'triplicity', 'term')
	rows.sort(key=lambda r: (min(rank.index(k) for k in r[2]), -r[1], r[4], order[r[6]]))
	res.alcocodens = rows
	if not rows:
		return
	pl = rows[0][0]
	res.alcocoden = pl
	res.years = YEARS[pl]
	res.strength = rows[0][6]
	p = chrt.planets.planets[pl]
	cond = res.conditions
	cond.append(('%s in house %d (Porphyry): %s; its years: greater %s, middle %s, lesser %s', NAMES[pl], rows[0][5], res.strength) + tuple(_fmt(y) for y in YEARS[pl]))
	if p.data[planets.Planet.SPLON] < 0.0:
		cond.append(('retrograde: the years are diminished by a fifth',))
	dig = chrt.dignity(pl)
	import chart as chartmod
	if dig == chartmod.Chart.CASUS:
		cond.append(('in its fall: the years are diminished by a fifth',))
	elif dig == chartmod.Chart.EXIL:
		cond.append(('in its detriment',))
	elif dig in (chartmod.Chart.DOMICIL, chartmod.Chart.EXAL):
		cond.append(('in its domicile' if dig == chartmod.Chart.DOMICIL else 'in its exaltation',))
	if pl != SUN:
		elong = abs((lon[pl] - lon[SUN] + 180.0) % 360.0 - 180.0)
		if elong < UNDER_BEAMS:
			cond.append(('under the beams of the Sun: gives no years unless the Sun receives it',))


def _fmt(y):
	return ('%g' % y)
