"""Zodiacal releasing as native Morinus tables: levels 1 and 2 for a lifetime;
a click on a level 2 period shows its levels 3 and 4."""

import wx
import tablewnd
import zodiacalreleasing as zr

HEADERS = ('Level', 'Sign', 'From the lot', 'Starts', 'Ends', 'Length', '')
NOTE = 'Places from the lot: 1, 4 and 7 are angles, 10 the peak. Dates in the time of the chart; years of 360 days.'


def place(sign, lotsign):
	n = (sign - lotsign) % 12 + 1
	return '%d%s' % (n, {1: ', angle', 4: ', angle', 7: ', angle', 10: ', peak'}.get(n, ''))


class ReleasingWnd(tablewnd.TableWnd):

	def __init__(self, parent, chrt, options, mainfr, lot, periods=None, title=''):
		"""periods: the level 3/4 periods to show (from a level 2 period), else levels 1/2."""
		tablewnd.TableWnd.__init__(self, parent, chrt, options, mainfr)
		self.lot = lot
		self.lotsign = int(zr.lot_longitude(chrt, lot) // 30.0) % 12
		self.drillable = periods is None
		if periods is None:
			self.lotsign, periods = zr.releasing(chrt, lot)
		self.periods = periods
		now = zr.now()
		rows, colours = [], []
		for p in periods:
			notes = []
			if p.loosing:
				notes.append('loosing of the bond')
			if p.start <= now < p.end:
				notes.append('now')
			hours = p.level >= 3
			rows.append(['L%d' % p.level,
				(tablewnd.SIGN, p.sign), place(p.sign, self.lotsign),
				zr.datestr(chrt, p.start, hours), zr.datestr(chrt, p.end, hours), zr.lengthstr(p), ', '.join(notes)])
			colours.append(self.options.clrLoF if p.level in (1, 3) else None)
		self.sections = [tablewnd.Section(rows, HEADERS, colours)]
		self.notes = [title or 'Zodiacal releasing from the Lot of %s' % zr.LOTNAMES[lot], NOTE]
		if self.drillable:
			self.notes.append('Click a level 2 period for its levels 3 and 4.')
			self.Bind(wx.EVT_LEFT_UP, self.onClick)
		self.layout()

	def getExt(self):
		return '_ZR'

	def onClick(self, event):
		hit = self.rowAt(event.GetPosition())
		if hit is None:
			return
		p = self.periods[hit[1]]
		if p.level != 2:
			return
		title = 'Level 2: %s, %s - %s' % (zr.LOTNAMES[self.lot], zr.datestr(self.chart, p.start), zr.datestr(self.chart, p.end))
		frame = tablewnd.TableFrame(self.GetTopLevelParent(), self.GetTopLevelParent().GetTitle() + ' - ' + title,
			lambda f: ReleasingWnd(f, self.chart, self.options, self.mainfr, self.lot, zr.drill(p), title))
		frame.Show(True)


class ReleasingFrame(tablewnd.TableFrame):

	def __init__(self, parent, title, chrt, options, lot):
		tablewnd.TableFrame.__init__(self, parent, title + ' - Zodiacal releasing from ' + zr.LOTNAMES[lot], lambda f: ReleasingWnd(f, chrt, options, parent, lot))
