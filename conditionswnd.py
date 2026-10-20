"""Planetary conditions as a native Morinus table (the analysis comes from traditional.py)."""

import wx
import common
import planets
import tablewnd
import traditional
from hor_tools import output as hout

# hor_tools planet names -> Morinus planet index
PLANETIDS = {'Saturn': planets.Planets.SATURN, 'Jupiter': planets.Planets.JUPITER, 'Mars': planets.Planets.MARS, 'Sun': planets.Planets.SUN,
	'Venus': planets.Planets.VENUS, 'Mercury': planets.Planets.MERCURY, 'Moon': planets.Planets.MOON}
HEADERS = ('', 'Position', 'House', 'Sect', 'Hayz / halb', 'Orientation', 'Synodic phase', 'Station', 'Motion', 'Joy', 'Latitude', 'Via Combusta')
NOTE = "Sect from the Sun's true altitude; whole-sign houses; Via Combusta 19\xb0 Libra - 3\xb0 Scorpio"


class ConditionsWnd(tablewnd.TableWnd):

	def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
		tablewnd.TableWnd.__init__(self, parent, chrt, options, mainfr, id, size)
		self.summary = []
		self.rows = []
		try:
			self.analyse(traditional.analyse(chrt))
		except traditional.NotAvailable as e:
			self.summary = [('Not available for this chart', str(e))]
		self.sections = [tablewnd.Section(self.summary)]
		if self.rows:
			self.sections.append(tablewnd.Section([cells for idx, cells in self.rows], HEADERS, [self.options.clrplanets[idx] for idx, cells in self.rows]))
			self.notes = [NOTE]
		self.layout()

	def analyse(self, a):
		solar = a.technical.solar
		moon = next((r for r in a.reports if r.planet.name == 'Moon'), None)
		self.summary = [
			('Sect', 'Day' if solar.is_day else 'Night'),
			("Sun's true altitude", '%+.4f\xb0' % solar.sun_true_altitude),
			('Apparent sunrise / sunset', '%s / %s' % tuple(t.strftime('%H:%M:%S') if t else 'none' for t in (solar.sunrise_local, solar.sunset_local))),
			('Planetary day / hour ruler', '%s / %s' % (a.technical.day_ruler, a.technical.hour_ruler or '- (no sunrise or sunset)')),
			('Moon void of course', 'yes' if moon is not None and moon.is_void_of_course else 'no')]
		for r in a.reports:
			p = r.planet
			idx = PLANETIDS[p.name]
			hayz = ', '.join(t for t, on in (('hayz', r.hayz), ('halb', r.halb)) if on) or '-'
			station = {'first': 'first (turning retrograde)', 'second': 'second (turning direct)'}.get(p.station or '', '-')
			motion = '%s, %s, %.2f\xb0/day (%.2fx mean)' % ('retrograde' if p.retrograde else 'direct', r.speed_class, abs(p.speed_long), r.speed_ratio)
			lat = {'north_strengthening': 'north: strengthening', 'south_weakening': 'south: weakening'}.get(r.latitude_condition, 'on the ecliptic')
			self.rows.append((idx, [
				(tablewnd.GLYPH, common.common.planets[idx]),
				(tablewnd.POSITION, self.chart.planets.planets[idx].data[planets.Planet.LON]),
				str(p.house),
				'%s planet, %s' % (r.sect_planet, 'in sect' if r.in_sect else 'out of sect'),
				hayz,
				'-' if p.name == 'Sun' else ('oriental' if r.oriental else 'occidental'),
				hout._format_synodic(r) or '-',
				station,
				motion,
				'joy' if r.is_in_planetary_joy else '-',
				lat,
				'yes' if r.is_in_via_combusta else '-']))

	def getExt(self):
		return '_Conditions'


class ConditionsFrame(tablewnd.TableFrame):

	def __init__(self, parent, title, chrt, options):
		tablewnd.TableFrame.__init__(self, parent, title + ' - Planetary conditions', lambda f: ConditionsWnd(f, chrt, options, parent))
