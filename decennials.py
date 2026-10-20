"""Decennials (Vettius Valens, Anthology IV): each of the seven planets rules
129 months (10 years 9 months) in turn, from the sect light (Sun by day, Moon by
night) and then in the zodiacal order of the planets in the chart. Within each
period the planets, from its ruler on, rule their minor years in months; at
levels 3 and 4 the period above is shared out in proportion to the minor years.
Months have 30 days. Method as in Morinus by shin10567
(https://github.com/shin10567/Morinus-Source-Codes, GPL).

Times are Julian days (UT), as in zodiacalreleasing."""

import planets
import lotswnd

P = planets.Planets
MINOR = {P.SATURN: 30, P.JUPITER: 12, P.MARS: 15, P.SUN: 19, P.VENUS: 8, P.MERCURY: 20, P.MOON: 25}
TOTAL = 129
MONTH = 30.0


class Period:
	def __init__(self, level, planet, start, end):
		self.level = level
		self.planet = planet
		self.start = start
		self.end = end


def order(chrt):
	"""The seven planets in zodiacal order, from the sect light (Morinus's sect,
	as used for the lots)."""
	pls = sorted(MINOR, key=lambda p: chrt.planets.planets[p].data[planets.Planet.LON])
	first = P.MOON if lotswnd.LotsWnd.isNightChart(chrt) else P.SUN
	i = pls.index(first)
	return pls[i:] + pls[:i]


def rotated(seq, first):
	i = seq.index(first)
	return seq[i:] + seq[:i]


def decennials(chrt, years=110):
	"""Level 1 periods and the level 2 periods within them, for years after birth."""
	seq = order(chrt)
	out = []
	t = chrt.time.jd
	end = t + years * 365.25
	while t < end:
		for p in seq:
			e = t + TOTAL * MONTH
			out.append(Period(1, p, t, e))
			tt = t
			for q in rotated(seq, p):
				out.append(Period(2, q, tt, tt + MINOR[q] * MONTH))
				tt += MINOR[q] * MONTH
			t = e
			if t >= end:
				break
	return seq, out


def share(seq, period, level):
	"""Periods of a level within a period, in proportion to the minor years."""
	out = []
	t = period.start
	length = period.end - period.start
	for q in rotated(seq, period.planet):
		e = t + length * MINOR[q] / float(TOTAL)
		out.append(Period(level, q, t, e))
		t = e
	out[-1].end = period.end
	return out


def drill(seq, period):
	"""Level 3 periods within a level 2 period, each followed by its level 4 periods."""
	out = []
	for p3 in share(seq, period, 3):
		out.append(p3)
		out.extend(share(seq, p3, 4))
	return out
