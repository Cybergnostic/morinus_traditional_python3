"""The Overview of the Positions workspace: one table instead of Positions,
Mundane positions, Speeds and Misc - the zodiacal and equatorial positions of
the planets with their motion and houses, the angles and lots, and the chart's
data. The values are the chart's own (the same as the specialist tables)."""

import wx
import astrology
import common
import houses
import miscwnd
import planets
import tablewnd
import traditional
import util

NAMES = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon', 'North Node')
ORDINALS = ('1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th')


def dms(x, signed=False):
	"""12°03'07", with a sign for signed values."""
	d, m, s = util.decToDeg(x)
	return ('-' if signed and x < 0 else '') + '%d\xb0%02d\'%02d"' % (d, m, s)


def hms(x):
	d, m, s = util.decToDeg(x)
	return '%d:%02d:%02d' % (d, m, s)


def mundane(pos):
	"""A house position (1.0-12.99) as '12th, 22%'."""
	house = int(pos)
	return '%s, %.1f%%' % (ORDINALS[(house - 1) % 12], int((pos - house) * 1000) / 10.0)


class OverviewWnd(tablewnd.TableWnd):

	def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
		tablewnd.TableWnd.__init__(self, parent, chrt, options, mainfr, id, size)
		self.deg_symbol = '\xb0'	# for miscwnd.MiscWnd.tableRows
		h, o = chrt, options
		hsname = houses.Houses.hsystems[h.houses.hsys]
		try:
			reports = {r.planet.name: r for r in traditional.analyse(h).reports}
		except Exception:	# traditional.NotAvailable, or an unusual chart
			reports = {}
		ra = (lambda x: hms(x / 15.0)) if o.intime else dms

		rows, colours = [], []
		for i, name in enumerate(NAMES):
			p = h.planets.planets[i]
			lon, lat, speed, latspeed = (p.data[k] for k in (planets.Planet.LON, planets.Planet.LAT, planets.Planet.SPLON, planets.Planet.SPLAT))
			motion = 'retrograde' if speed < 0 else 'direct'
			rep = reports.get(name)
			if rep is not None:
				motion += ', ' + rep.speed_class
				if rep.planet.station:
					motion = 'stationary (%s station)' % rep.planet.station
			house = h.houses.getHousePos(lon, o, True) + 1
			rows.append([(tablewnd.GLYPH, common.common.planets[i]), (tablewnd.POSITION, lon), dms(lat, True),
				ra(p.dataEqu[planets.Planet.RAEQU]), dms(p.dataEqu[planets.Planet.DECLEQU], True),
				dms(speed, True), dms(latspeed, True), motion if i < 7 else ('mean' if o.meannode else 'true'), str(house),
				mundane(h.houses.mundanePosition(lon, lat, h.place.lat))])
			colours.append(o.clrplanets[i])
		headers = ['', 'Longitude', 'Latitude', 'Right asc.', 'Declination', 'Motion in long.', 'In lat.', 'Motion', 'House', 'Mundane position']

		points = []
		for label, lon in (('Ascendant', h.houses.ascmc[houses.Houses.ASC]), ('Midheaven', h.houses.ascmc[houses.Houses.MC]),
							('Lot of Fortune', h.fortune.fortune[0])):
			r, d, dist = astrology.swe_cotrans(lon, 0.0, 1.0, -h.obl[0])
			points.append([label, (tablewnd.POSITION, lon), ra(r), dms(d, True)])
		if h.munfortune is not None:	# full charts only
			mf = h.munfortune.mfortune
			points.append(['Mundane Lot of Fortune', (tablewnd.POSITION, mf[0]), ra(mf[2]), dms(mf[3], True)])

		data = miscwnd.MiscWnd.tableRows(self)
		data.append(['House system', mundane_name(hsname)])

		self.sections = [tablewnd.Section(rows, headers, colours),
			tablewnd.Section(points, ['', 'Longitude', 'Right asc.', 'Declination']),
			tablewnd.Section(data)]
		self.notes = ['House: by longitude, with the cusp orbs of Settings > Orbs. Mundane position: 1st, 50% is half way through the 1st house.',
			'Speculum (semi-arcs, poles, mundane positions of every method): the Speculum tab.']
		self.layout()

	def getExt(self):
		return '_Overview'


def mundane_name(letter):
	return {'P': 'Placidus', 'K': 'Koch', 'R': 'Regiomontanus', 'C': 'Campanus', 'E': 'Equal', 'W': 'Whole sign', 'X': 'Axial rotation',
		'M': 'Morinus', 'H': 'Horizontal', 'T': 'Page-Polich', 'B': 'Alcabitius', 'O': 'Porphyry'}.get(letter, letter)


class OverviewFrame(tablewnd.TableFrame):

	def __init__(self, parent, title, chrt, options):
		tablewnd.TableFrame.__init__(self, parent, title + ' - Positions', lambda f: OverviewWnd(f, chrt, options, parent))
