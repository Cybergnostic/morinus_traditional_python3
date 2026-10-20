"""Heliacal phenomena and phasis as a native Morinus table."""

import wx
import common
import tablewnd
import heliacal
import zodiacalreleasing as zr

HEADERS = ('', 'Phenomenon', 'Before the birth', 'After the birth', '')
NOTE = 'Visibility from the Swiss Ephemeris (standard atmosphere); phasis: within %d days of the birth.' % heliacal.PHASIS_DAYS


class HeliacalWnd(tablewnd.TableWnd):

	def __init__(self, parent, chrt, options, mainfr):
		tablewnd.TableWnd.__init__(self, parent, chrt, options, mainfr)
		jd = chrt.time.jd

		def when(t):
			if t is None:
				return '-'
			return '%s (%+.0f days)' % (zr.datestr(chrt, t), t - jd)

		rows, colours = [], []
		for planet, name, before, after in heliacal.phenomena(chrt):
			near = [abs(t - jd) for t in (before, after) if t is not None]
			phasis = 'phasis' if near and min(near) <= heliacal.PHASIS_DAYS else ''
			rows.append([(tablewnd.GLYPH, common.common.planets[planet]), name, when(before), when(after), phasis])
			colours.append(self.options.clrplanets[planet])
		self.sections = [tablewnd.Section(rows, HEADERS, colours)]
		self.notes = ['Heliacal phenomena and phasis', NOTE]
		self.layout()

	def getExt(self):
		return '_Heliacal'


class HeliacalFrame(tablewnd.TableFrame):

	def __init__(self, parent, title, chrt, options):
		tablewnd.TableFrame.__init__(self, parent, title + ' - Heliacal phenomena', lambda f: HeliacalWnd(f, chrt, options, parent))
