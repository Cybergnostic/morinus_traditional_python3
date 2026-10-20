"""Zodiacal releasing (Vettius Valens, Anthology IV) from the Lot of Fortune or the
Lot of Spirit.

Each sign gives a period of the minor years of its ruler; level 1 counts them in
years of 360 days, level 2 in months of 30 days, level 3 in units of 2.5 days and
level 4 in units of 5 hours. Levels 2-4 start from the sign of the period above
them; when they would come back to it, they leap to the opposite sign once
(the loosing of the bond). Method as in Morinus by shin10567
(https://github.com/shin10567/Morinus-Source-Codes, GPL).

Times are Julian days (UT), so the calendar and BC dates of the chart are kept."""

import datetime
import astrology
import chart
import fortune
import houses

YEARS = (15, 8, 20, 25, 19, 20, 8, 15, 12, 27, 30, 12)	# Aries..Pisces
UNIT_DAYS = {1: 360.0, 2: 30.0, 3: 2.5, 4: 5.0 / 24.0}
FORTUNE, SPIRIT = 0, 1
LOTNAMES = ('Fortune', 'Spirit')


class Period:
	def __init__(self, level, sign, start, end, loosing=False):
		self.level = level
		self.sign = sign
		self.start = start
		self.end = end
		self.loosing = loosing	# this period begins with the loosing of the bond


def lot_longitude(chrt, lot):
	"""Fortune as Morinus calculates it (Options > Lot of Fortune); Spirit is its
	mirror in the Ascendant (Asc + Sun - Moon by day, reversed by night)."""
	lof = chrt.fortune.fortune[fortune.Fortune.LON]
	if lot == FORTUNE:
		return lof
	return (2.0 * chrt.houses.ascmc[houses.Houses.ASC] - lof) % 360.0


def sublevel(level, start, end, first):
	"""Periods of a level within [start, end), from the sign first."""
	out = []
	t, sign, loosed = start, first, False
	leap = False
	while t < end:
		e = min(t + YEARS[sign] * UNIT_DAYS[level], end)
		out.append(Period(level, sign, t, e, leap))
		t, leap = e, False
		nxt = (sign + 1) % 12
		if not loosed and nxt == first:
			sign, loosed, leap = (first + 6) % 12, True, True
		else:
			sign = nxt
	return out


def releasing(chrt, lot, years=110):
	"""Level 1 periods and the level 2 periods within them, for years after birth."""
	start = chrt.time.jd
	end = start + years * 365.25
	first = int(lot_longitude(chrt, lot) // chart.Chart.SIGN_DEG) % 12
	out = []
	t, sign = start, first
	while t < end:
		e = t + YEARS[sign] * UNIT_DAYS[1]
		out.append(Period(1, sign, t, e))
		out.extend(sublevel(2, t, e, sign))
		t, sign = e, (sign + 1) % 12
	return first, out


def drill(period):
	"""Level 3 periods within a level 2 period, each followed by its level 4 periods."""
	out = []
	for p3 in sublevel(3, period.start, period.end, period.sign):
		out.append(p3)
		out.extend(sublevel(4, p3.start, p3.end, p3.sign))
	return out


def datestr(chrt, jd, hours=False):
	t = chrt.time
	calflag = astrology.SE_GREG_CAL if t.cal == chart.Time.GREGORIAN else astrology.SE_JUL_CAL
	y, m, d, h = astrology.swe_revjul(jd + t.localoffset(), calflag)
	txt = '%s%04d.%02d.%02d' % ('-' if y < 0 else '', abs(y), m, d)
	if hours:
		txt += ' %02d:%02d' % divmod(min(int(round(h * 60.0)), 24 * 60 - 1), 60)
	return txt


def lengthstr(p):
	days = p.end - p.start
	if p.level == 1:
		return '%g years' % round(days / 360.0, 2)
	if p.level == 2:
		return '%g months' % round(days / 30.0, 2)
	if days >= 1.0:
		return '%.1f days' % days
	return '%.1f hours' % (days * 24.0)


def now():
	"""The present moment as a UT Julian day."""
	n = datetime.datetime.now(datetime.timezone.utc)
	return astrology.swe_julday(n.year, n.month, n.day, n.hour + n.minute / 60.0 + n.second / 3600.0, astrology.SE_GREG_CAL)
