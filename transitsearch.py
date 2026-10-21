"""Transit search: the exact transits of Saturn ... Mercury over a span of
months (instead of Morinus's month at a time and its separate Sun transits),
chosen by transiting planet, aspect and the natal points they reach. The
transits are those of Morinus's own calculation (transits.Transits); a
double-click opens the transit chart around the radix."""

import csv
import os
import wx
import astrology
import chart
import transits
import transitframe
import zodiacalreleasing

PLANETS = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury')	# the Moon moves too fast for this search
ASPECTS = ('Conjunction', 'Sextile', 'Square', 'Trine', 'Opposition')
ASPECTVERBS = ('conjunct', 'sextile', 'square', 'trine', 'opposite')
BODIES = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon', 'North Node')
SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
ORDINALS = ('1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th')
T = transits.Transit
TARGETS = ((T.PLANET, 'Natal planets'), (T.ASCMC, 'Ascendant and Midheaven'), (T.LOF, 'Lot of Fortune'),
	(T.ANTISCION, 'Antiscia'), (T.CONTRAANTISCION, 'Contra-antiscia'), (T.SIGN, 'Sign ingresses'))
MAXMONTHS = 12 * 30


def months(start, end):
	"""(year, month) from start to end, both included."""
	y, m = start
	while (y, m) <= end:
		yield y, m
		y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def jd_of(radix, year, month, tr):
	calflag = astrology.SE_GREG_CAL if radix.time.cal == chart.Time.GREGORIAN else astrology.SE_JUL_CAL
	return astrology.swe_julday(year, month, tr.day, tr.time, calflag)


def wanted(tr, planets_, aspects, targets):
	if tr.plt not in planets_ or tr.objtype not in targets:
		return False
	return tr.objtype == T.SIGN or tr.aspect in aspects


def search(radix, start, end, planets_, aspects, targets, progress=None):
	"""[(jd, transit)] in time order; progress(done, total) may return False to stop."""
	spans = list(months(start, end))
	found = []
	for n, (y, m) in enumerate(spans):
		if progress is not None and progress(n, len(spans)) is False:
			break
		trs = transits.Transits()
		trs.month(y, m, radix)
		found += [(jd_of(radix, y, m, tr), tr) for tr in trs.transits if wanted(tr, planets_, aspects, targets)]
	found.sort(key=lambda x: x[0])
	return found


def describe(tr):
	"""'Saturn (R) square Sun', 'Mars enters Leo', 'Jupiter conjunct the antiscion of Venus'..."""
	who = PLANETS[tr.plt] + (' (R)' if tr.pltretr == T.RETR else ' (S)' if tr.pltretr == T.STAT else '')
	if tr.objtype == T.SIGN:
		return '%s enters %s' % (who, SIGNS[tr.obj])
	verb = ASPECTVERBS[tr.aspect] if 0 <= tr.aspect < len(ASPECTVERBS) else 'conjunct'
	target = {T.PLANET: lambda: 'natal ' + BODIES[tr.obj], T.ASCMC: lambda: ('the Ascendant', 'the Midheaven')[tr.obj],
		T.LOF: lambda: 'the Lot of Fortune', T.ANTISCION: lambda: 'the antiscion of ' + BODIES[tr.obj],
		T.CONTRAANTISCION: lambda: 'the contra-antiscion of ' + BODIES[tr.obj]}[tr.objtype]()
	return '%s %s %s' % (who, verb, target)


class TransitSearch(wx.Frame):

	def __init__(self, mainfr, sun=False):
		self.mainfr = mainfr
		self.radix = radix = mainfr.horoscope
		wx.Frame.__init__(self, mainfr, -1, 'Transit search — ' + radix.name, size=(980, 680))
		self.SetMinSize((760, 480))
		panel = wx.Panel(self)
		year = zodiacalreleasing.datestr(radix, zodiacalreleasing.now())[:4]
		year = int(year) if year.lstrip('-').isdigit() else radix.time.origyear
		self.fromyear = wx.SpinCtrl(panel, -1, min=1, max=5000, initial=year, size=(130, -1))
		self.toyear = wx.SpinCtrl(panel, -1, min=1, max=5000, initial=year, size=(130, -1))
		names = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
		self.frommonth = wx.Choice(panel, -1, choices=names)
		self.tomonth = wx.Choice(panel, -1, choices=names)
		self.frommonth.SetSelection(0)
		self.tomonth.SetSelection(11)
		self.planets = [wx.CheckBox(panel, -1, p) for p in PLANETS]
		self.aspects = [wx.CheckBox(panel, -1, a) for a in ASPECTS]
		self.targets = [(typ, wx.CheckBox(panel, -1, label)) for typ, label in TARGETS]
		self.preset(sun)
		go = wx.Button(panel, -1, 'Search')
		go.SetDefault()
		go.Bind(wx.EVT_BUTTON, self.onSearch)
		self.status = wx.StaticText(panel, -1, 'Choose the months and the transits, then Search.')
		self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		for i, (name, width) in enumerate((('Date and time (chart\'s zone)', 190), ('Transit', 430), ('In natal house', 120))):
			self.list.InsertColumn(i, name, width=width)
		self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onOpen)
		self.openbtn = wx.Button(panel, -1, 'Open transit chart')
		self.openbtn.Bind(wx.EVT_BUTTON, self.onOpen)
		csvbtn = wx.Button(panel, -1, 'Export as CSV...')
		csvbtn.Bind(wx.EVT_BUTTON, self.onCSV)
		close = wx.Button(panel, wx.ID_CLOSE)
		close.Bind(wx.EVT_BUTTON, lambda e: self.Close())

		grid = wx.FlexGridSizer(0, 2, 8, 12)
		span = wx.BoxSizer(wx.HORIZONTAL)
		for w, gap in ((wx.StaticText(panel, -1, 'From'), 6), (self.frommonth, 4), (self.fromyear, 18),
		               (wx.StaticText(panel, -1, 'to'), 6), (self.tomonth, 4), (self.toyear, 0)):
			span.Add(w, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, gap)
		presets = wx.Choice(panel, -1, choices=['All transits', 'Sun to the angles and natal planets', 'Slow planets: hard aspects'])
		presets.SetSelection(1 if sun else 0)
		presets.Bind(wx.EVT_CHOICE, lambda e: self.preset(*{0: (False,), 1: (True,), 2: (False, True)}[presets.GetSelection()]))
		for label, items in (('Months', [span]), ('Preset', [presets]), ('Transiting', self.planets), ('Aspects', self.aspects),
		                     ('To', [c for t, c in self.targets])):
			row = wx.BoxSizer(wx.HORIZONTAL)
			for w in items:
				row.Add(w, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
			t = wx.StaticText(panel, -1, label + ':')
			grid.Add(t, 0, wx.ALIGN_CENTER_VERTICAL)
			grid.Add(row, 0)
		top = wx.BoxSizer(wx.HORIZONTAL)
		top.Add(grid, 1)
		top.Add(go, 0, wx.ALIGN_BOTTOM)
		buttons = wx.BoxSizer(wx.HORIZONTAL)
		buttons.Add(self.status, 1, wx.ALIGN_CENTER_VERTICAL)
		for b in (self.openbtn, csvbtn, close):
			buttons.Add(b, 0, wx.LEFT, 8)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(top, 0, wx.EXPAND | wx.ALL, 12)
		sizer.Add(self.list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 12)
		sizer.Add(buttons, 0, wx.EXPAND | wx.ALL, 12)
		panel.SetSizer(sizer)
		self.results = []
		self.openbtn.Enable(False)
		self.Bind(wx.EVT_CLOSE, self.onClose)

	def preset(self, sun=False, slow=False):
		"""All transits; the Sun to the angles and natal planets (Morinus's Sun
		transits); or Saturn, Jupiter and Mars in hard aspects."""
		for i, c in enumerate(self.planets):
			c.SetValue(i == 3 if sun else i < 3 if slow else True)
		for i, c in enumerate(self.aspects):
			c.SetValue(i == 0 if sun else i in (0, 2, 4) if slow else True)
		for typ, c in self.targets:
			c.SetValue(typ in ((T.PLANET, T.ASCMC) if sun or slow else (T.PLANET, T.ASCMC, T.LOF)))

	def choices(self):
		planets_ = {i for i, c in enumerate(self.planets) if c.GetValue()}
		aspects = {i for i, c in enumerate(self.aspects) if c.GetValue()}
		targets = {t for t, c in self.targets if c.GetValue()}
		return planets_, aspects, targets

	def onSearch(self, event):
		start = (self.fromyear.GetValue(), self.frommonth.GetSelection() + 1)
		end = (self.toyear.GetValue(), self.tomonth.GetSelection() + 1)
		if end < start:
			start, end = end, start
		span = len(list(months(start, end)))
		if span > MAXMONTHS:
			wx.MessageBox('Search at most %d years at a time.' % (MAXMONTHS // 12), 'Transit search', wx.OK | wx.ICON_INFORMATION, self)
			return
		planets_, aspects, targets = self.choices()
		dlg = wx.ProgressDialog('Transit search', 'Searching %d months...' % span, maximum=span, parent=self,
		                        style=wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE)
		try:
			self.results = search(self.radix, start, end, planets_, aspects, targets,
			                      lambda done, total: dlg.Update(done)[0])
		finally:
			dlg.Destroy()
		self.fill()

	def fill(self):
		self.list.DeleteAllItems()
		for n, (jd, tr) in enumerate(self.results):
			self.list.InsertItem(n, zodiacalreleasing.datestr(self.radix, jd, hours=True))
			self.list.SetItem(n, 1, describe(tr))
			self.list.SetItem(n, 2, ORDINALS[tr.house] if 0 <= tr.house < 12 else '')
		self.status.SetLabel('%d transits' % len(self.results))
		self.openbtn.Enable(bool(self.results))
		if self.results:
			self.list.Select(0)

	def onOpen(self, event):
		sel = self.list.GetFirstSelected()
		if not 0 <= sel < len(self.results):
			return
		jd, tr = self.results[sel]
		r = self.radix
		calflag = astrology.SE_GREG_CAL if r.time.cal == chart.Time.GREGORIAN else astrology.SE_JUL_CAL
		y, m, d, hours = astrology.swe_revjul(jd + 0.5 / 86400.0, calflag)
		h, rest = divmod(int(hours * 3600), 3600)
		mi, s = divmod(rest, 60)
		tim = chart.Time(y, m, d, h, mi, s, False, r.time.cal, chart.Time.GREENWICH, True, 0, 0, False, r.place)
		trchart = chart.Chart(r.name, r.male, tim, r.place, chart.Chart.TRANSIT, describe(tr), self.mainfr.options, False)
		frame = transitframe.TransitFrame(self.mainfr, self.mainfr.title + ' — ' + describe(tr), trchart, r,
		                                  self.mainfr.options, transitframe.TransitFrame.COMPOUND)
		frame.Show(True)

	def onCSV(self, event):
		dlg = wx.FileDialog(self, 'Export as CSV', '', self.radix.name + '_Transits.csv', 'CSV files (*.csv)|*.csv', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			if not path.lower().endswith('.csv'):
				path += '.csv'
			with open(path, 'w', newline='', encoding='utf-8-sig') as f:
				w = csv.writer(f)
				w.writerow(['Date and time (chart\'s zone)', 'Transit', 'In natal house'])
				for jd, tr in self.results:
					w.writerow([zodiacalreleasing.datestr(self.radix, jd, hours=True), describe(tr), ORDINALS[tr.house] if 0 <= tr.house < 12 else ''])
		dlg.Destroy()

	def onClose(self, event):
		if getattr(self.mainfr, 'transit_search', None) is self:
			self.mainfr.transit_search = None
		event.Skip()


def show(mainfr, sun=False):
	if mainfr.splash:
		return None
	if mainfr.horoscope.time.bc:
		wx.MessageBox('The transit search is not available for BC charts.', 'Transit search', wx.OK | wx.ICON_INFORMATION, mainfr)
		return None
	wnd = getattr(mainfr, 'transit_search', None)
	if not wnd:
		wnd = mainfr.transit_search = TransitSearch(mainfr, sun)
	elif sun:
		wnd.preset(True)
	wnd.Show()
	wnd.Raise()
	return wnd
