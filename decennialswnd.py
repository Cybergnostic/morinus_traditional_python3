"""Decennials as native Morinus tables: levels 1 and 2 for a lifetime; a click on a
level 2 period shows its levels 3 and 4."""

import wx
import common
import tablewnd
import decennials
import zodiacalreleasing as zr

HEADERS = ('Level', 'Planet', 'Starts', 'Ends', 'Length', '')
NOTE = 'From the sect light, then in zodiacal order; dates in the time of the chart, months of 30 days.'


class DecennialsWnd(tablewnd.TableWnd):

	def __init__(self, parent, chrt, options, mainfr, periods=None, title=''):
		"""periods: the level 3/4 periods to show (from a level 2 period), else levels 1/2."""
		tablewnd.TableWnd.__init__(self, parent, chrt, options, mainfr)
		self.drillable = periods is None
		if periods is None:
			self.seq, periods = decennials.decennials(chrt)
		else:
			self.seq = decennials.order(chrt)
		self.periods = periods
		now = zr.now()
		rows, colours = [], []
		for p in periods:
			hours = p.level >= 3
			rows.append(['L%d' % p.level, (tablewnd.GLYPH, common.common.planets[p.planet]),
				zr.datestr(chrt, p.start, hours), zr.datestr(chrt, p.end, hours), zr.lengthstr(p),
				'now' if p.start <= now < p.end else ''])
			colours.append(self.options.clrplanets[p.planet])
		self.sections = [tablewnd.Section(rows, HEADERS, colours)]
		self.notes = [title or 'Decennials', NOTE]
		if self.drillable:
			self.notes.append('Click a level 2 period for its levels 3 and 4.')
			self.Bind(wx.EVT_LEFT_UP, self.onClick)
		self.layout()

	def getExt(self):
		return '_Decennials'

	def onClick(self, event):
		hit = self.rowAt(event.GetPosition())
		if hit is None or self.periods[hit[1]].level != 2:
			return
		p = self.periods[hit[1]]
		title = 'Decennials, level 2: %s - %s' % (zr.datestr(self.chart, p.start), zr.datestr(self.chart, p.end))
		top = self.GetTopLevelParent()
		frame = tablewnd.TableFrame(top, top.GetTitle() + ' - ' + title,
			lambda f: DecennialsWnd(f, self.chart, self.options, self.mainfr, decennials.drill(self.seq, p), title))
		frame.Show(True)


class DecennialsFrame(tablewnd.TableFrame):

	def __init__(self, parent, title, chrt, options):
		tablewnd.TableFrame.__init__(self, parent, title + ' - Decennials', lambda f: DecennialsWnd(f, chrt, options, parent))
