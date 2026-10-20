"""Circumambulation of the Ascendant through the bounds as a native Morinus table."""

import wx
import common
import tablewnd
import circumambulation as ca
import zodiacalreleasing as zr

HEADERS = ('Age', 'Date', 'Point', 'Distributor', 'Participant', '')
NOTE = "%s, %s; bounds from Options > Terms (Options > Circumambulation)."


class CircumambulationWnd(tablewnd.TableWnd):

	def __init__(self, parent, chrt, options, mainfr):
		tablewnd.TableWnd.__init__(self, parent, chrt, options, mainfr)
		try:
			events = ca.circumambulation(chrt)
		except ca.NotAvailable as e:
			self.sections = [tablewnd.Section([('Not available for this chart', str(e))])]
			self.layout()
			return
		now = zr.now()
		rows, colours = [], []
		distributor = None
		for i, ev in enumerate(events):
			start = ca.date(chrt, ev.years)
			end = ca.date(chrt, events[i + 1].years) if i + 1 < len(events) else None
			if ev.distributor is not None:
				distributor = ev.distributor
				participant = ''
				colour = self.options.clrplanets[distributor]
			else:
				participant = (tablewnd.GLYPH, common.common.planets[ev.participant] + ca.ASPECTS[ev.aspect][1])
				colour = self.options.clrplanets[ev.participant]
			current = 'now' if start <= now and (end is None or now < end) else ''
			rows.append(['%.1f' % ev.years, zr.datestr(chrt, start), (tablewnd.POSITION, ev.lon),
				(tablewnd.GLYPH, common.common.planets[distributor]), participant, current])
			colours.append(colour)
		self.sections = [tablewnd.Section(rows, HEADERS, colours)]
		point = ca.tradoptions.get('ca_point')
		self.notes = ['Circumambulation of the %s through the bounds' % ('Midheaven' if point == 'mc' else 'Ascendant'),
			NOTE % ('The Midheaven under the right ascensions' if point == 'mc' else 'The Ascendant under the oblique ascensions of the birth latitude',
			'a year for each 0\xb059\'08" (Naibod)' if ca.tradoptions.get('ca_key') == 'naibod' else 'a year for each degree (Ptolemy)')]
		self.layout()

	def getExt(self):
		return '_Circumambulation'


class CircumambulationFrame(tablewnd.TableFrame):

	def __init__(self, parent, title, chrt, options):
		tablewnd.TableFrame.__init__(self, parent, title + ' - Circumambulation', lambda f: CircumambulationWnd(f, chrt, options, parent))
