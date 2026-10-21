"""The sidebar of the main window, beside the chart: the Planet tab (position,
motion, conditions, dignities and aspects of the planet chosen, or clicked in
the chart), the Chart tab (sect, angles, lots, rulers of the day and hour) and
the Time lords tab (profection, firdaria, zodiacal releasing and decennials of
today)."""

import json
import wx
import wx.html
import chart
import planets
import houses
import fortune
import firdaria
import lotswnd
import mtexts
import tradoptions
import traditional
import zodiacalreleasing
import decennials

WIDTH = 310
P = planets.Planets
NAMES = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon', 'North Node', 'South Node')
SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
ASPECTS = {chart.Chart.CONIUNCTIO: 'Conjunction', chart.Chart.SEXTIL: 'Sextile', chart.Chart.QUADRAT: 'Square', chart.Chart.TRIGON: 'Trine', chart.Chart.OPPOSITIO: 'Opposition'}
TRIPLS = (0, 3, 1, 2, 0, 3, 1, 2, 0, 3, 1, 2)	# fire, earth, air, water (as almutens.py)


def signname(i):
	return mtexts.txtscommon.get(SIGNS[i], SIGNS[i])


def planetname(i):
	return mtexts.txtscommon.get(NAMES[i], NAMES[i]) if i < 7 else NAMES[i]


def pos(lon):
	"""12°22′ Pisces"""
	d = lon % 30.0
	deg, minute = int(d), int(round((d - int(d)) * 60.0))
	if minute == 60:
		deg, minute = deg + 1, 0
	return '%d°%02d′ %s' % (deg, minute, signname(int(lon // 30.0) % 12))


def rulers(opts, lon, night):
	"""The rulers of a degree: (domicile, exaltation, triplicity (by sect), participating, term, face); -1 for none."""
	sign, deg = int(lon // 30.0) % 12, lon % 30.0
	dom = next((p for p in range(7) if opts.dignities[p][0][sign]), -1)
	exa = next((p for p in range(7) if opts.dignities[p][1][sign]), -1)
	trip = [p if 0 <= p < 7 else -1 for p in opts.trips[opts.seltrip][TRIPLS[sign]]]	# 7: none
	total, term = 0.0, -1
	for pl, width in opts.terms[opts.selterm][sign]:
		total += width
		if total > deg:
			term = pl
			break
	face = opts.decans[opts.seldecan][sign][min(int(deg // 10), 2)]
	return dom, exa, trip[1] if night else trip[0], trip[2], term, face


def jdstr(chrt, jd):
	return zodiacalreleasing.datestr(chrt, jd)


class Sidebar(wx.Panel):

	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1, size=(WIDTH, -1))
		self.chart = None
		self.key = None
		self.planet = P.SUN
		self.book = wx.Notebook(self, -1)
		self.pages = []
		for title in ('Planet', 'Chart', 'Time lords'):
			page = wx.Panel(self.book)
			vs = wx.BoxSizer(wx.VERTICAL)
			if title == 'Planet':
				self.choice = wx.Choice(page, -1, choices=[planetname(i) for i in range(len(NAMES))])
				self.choice.SetToolTip('The planet shown; clicking a planet in the chart chooses it too')
				self.choice.Bind(wx.EVT_CHOICE, lambda e: self.select(self.choice.GetSelection()))
				vs.Add(self.choice, 0, wx.EXPAND | wx.ALL, 4)
			html = wx.html.HtmlWindow(page, -1, style=wx.html.HW_SCROLLBAR_AUTO)
			html.SetStandardFonts(10)
			vs.Add(html, 1, wx.EXPAND)
			page.SetSizer(vs)
			self.book.AddPage(page, title)
			self.pages.append(html)
		s = wx.BoxSizer(wx.VERTICAL)
		s.Add(self.book, 1, wx.EXPAND)
		self.SetSizer(s)

	def setChart(self, chrt, radix=None):
		"""Shows a chart; recalculates only when it or its settings changed. With
		radix (a return, transit... of it) the time lords are the radix's at the
		time of chrt, otherwise the chart's of today."""
		o = chrt.options
		self.radix = radix
		key = (id(chrt), id(radix), chrt.time.jd, chrt.houses.ascmc[houses.Houses.ASC], o.meannode, o.ayanamsha, o.seltrip, o.selterm, o.seldecan,
			o.isfirbonatti, json.dumps(tradoptions.values(), sort_keys=True))
		if key == self.key:
			return
		self.key, self.chart = key, chrt
		try:
			self.analysis = traditional.analyse(chrt)
		except Exception:	# traditional.NotAvailable, or an unusual chart
			self.analysis = None
		self.night = lotswnd.LotsWnd.isNightChart(chrt)
		self.showPlanet()
		self.pages[1].SetPage(self.page(self.chartHtml()))
		self.pages[2].SetPage(self.page(self.lordsHtml()))

	def select(self, planet):
		"""Shows a planet (an index of planets.Planets) in the Planet tab."""
		if planet is None or not 0 <= planet < len(NAMES):
			return
		self.planet = planet
		if self.chart is not None:
			self.showPlanet()
			self.book.SetSelection(0)

	def showPlanet(self):
		self.choice.SetSelection(self.planet)
		self.pages[0].SetPage(self.page(self.planetHtml(self.planet)))

	# html

	def page(self, body):
		c = lambda i: wx.SystemSettings.GetColour(i).GetAsString(wx.C2S_HTML_SYNTAX)
		self.grey = c(wx.SYS_COLOUR_GRAYTEXT)
		return '<html><body bgcolor="%s" text="%s">%s</body></html>' % (c(wx.SYS_COLOUR_WINDOW), c(wx.SYS_COLOUR_WINDOWTEXT), body.replace('$GREY', self.grey))

	@staticmethod
	def rows(pairs):
		return '<table cellspacing="0" cellpadding="2" width="100%">' + ''.join(
			'<tr><td valign="top" width="42%%"><font color="$GREY">%s</font></td><td valign="top">%s</td></tr>' % (k, v) for k, v in pairs if v) + '</table>'

	@staticmethod
	def head(text):
		return '<p><b>%s</b></p>' % text

	def planetHtml(self, i):
		h = self.chart
		pl = h.planets.planets[i]
		lon, speed = pl.data[planets.Planet.LON], pl.data[planets.Planet.SPLON]
		ascsign = int(h.houses.ascmc[houses.Houses.ASC] // 30.0)
		house = (int(lon // 30.0) - ascsign) % 12 + 1
		out = ['<font size="+2"><b>%s</b></font><br>%s, house %d (whole sign)' % (planetname(i), pos(lon), house)]
		pairs = [('Motion', '%s, %.2f° a day' % ('retrograde' if speed < 0 else 'direct', abs(speed)))]
		rep = None
		if self.analysis is not None and i < 7:
			rep = next((r for r in self.analysis.reports if r.planet.name == NAMES[i]), None)
		if rep is not None:
			p = rep.planet
			pairs = [('Motion', '%s, %s, %.2f° a day' % ('retrograde' if p.retrograde else 'direct', rep.speed_class, abs(p.speed_long))),
				('Station', {'first': 'first (turning retrograde)', 'second': 'second (turning direct)'}.get(p.station or '')),
				('Sect', '%s planet, %s' % (rep.sect_planet, 'in sect' if rep.in_sect else 'out of sect')),
				('Hayz', ', '.join(t for t, on in (('hayz', rep.hayz), ('halb', rep.halb)) if on) or '-'),
				('Orientation', None if p.name == 'Sun' else ('oriental' if rep.oriental else 'occidental')),
				('Phase', traditional_phase(rep)),
				('Latitude', {'north_strengthening': 'north, strengthening', 'south_weakening': 'south, weakening'}.get(rep.latitude_condition, 'on the ecliptic')),
				('Joy', 'in its joy' if rep.is_in_planetary_joy else None),
				('Via Combusta', 'yes' if rep.is_in_via_combusta else None)]
		out.append(self.rows(pairs))
		if i < 7:
			o = h.options
			sign = int(lon // 30.0) % 12
			r = rulers(o, lon, self.night)
			mark = lambda p: ('<b>%s</b> ✓' % planetname(p)) if p == i else (planetname(p) if p >= 0 else '-')
			out.append(self.head('Essential dignities'))
			own = [n for n, p in zip(('domicile', 'exaltation', 'triplicity', 'participating triplicity', 'term', 'face'), r) if p == i]
			debil = [n for n, on in (('detriment', o.dignities[i][0][(sign + 6) % 12]), ('fall', o.dignities[i][1][(sign + 6) % 12])) if on]
			out.append(self.rows([('Domicile', mark(r[0])), ('Exaltation', mark(r[1])), ('Triplicity (%s)' % ('night' if self.night else 'day'), mark(r[2])),
				('Participating', mark(r[3]) if r[3] >= 0 else None), ('Term', mark(r[4])), ('Face', mark(r[5])),
				('', 'In its ' + ', '.join(own + debil) if own or debil else 'Peregrine')]))
		asps = []
		for j in range(len(NAMES)):
			if j == i:
				continue
			a = h.aspmatrix[max(i, j)][min(i, j)]
			if a.typ in ASPECTS:
				asps.append((a.aspdif, '%s %s' % (ASPECTS[a.typ], planetname(j)), '%.2f°%s' % (a.aspdif, ', applying' if a.appl else '')))
		if asps:
			out.append(self.head('Aspects'))
			out.append(self.rows([(t, d) for orb, t, d in sorted(asps)]))
		return ''.join(out)

	def chartHtml(self):
		h = self.chart
		asc, mc = h.houses.ascmc[houses.Houses.ASC], h.houses.ascmc[houses.Houses.MC]
		lof = h.fortune.fortune[fortune.Fortune.LON]
		spirit = zodiacalreleasing.lot_longitude(h, zodiacalreleasing.SPIRIT)
		r = rulers(h.options, asc, self.night)
		pairs = [('Sect', 'Night chart' if self.night else 'Day chart'), ('Ascendant', pos(asc)), ('Lord of the Ascendant', planetname(r[0])),
			('Midheaven', pos(mc)), ('Lot of Fortune', pos(lof)), ('Lot of Spirit', pos(spirit))]
		if self.analysis is not None:
			t = self.analysis.technical
			pairs += [('Ruler of the day', t.day_ruler), ('Ruler of the hour', t.hour_ruler or '- (no sunrise or sunset)'),
				('Sunrise / sunset', '%s / %s' % tuple(x.strftime('%H:%M') if x else 'none' for x in (t.solar.sunrise_local, t.solar.sunset_local)))]
			moon = next((x for x in self.analysis.reports if x.planet.name == 'Moon'), None)
			if moon is not None:
				pairs.append(('Moon void of course', 'yes' if moon.is_void_of_course else 'no'))
		return self.rows(pairs)

	def lordsHtml(self):
		h = self.radix or self.chart
		now = self.chart.time.jd if self.radix else zodiacalreleasing.now()
		if now < h.time.jd:
			return '<p>Before the birth: no time lords.</p>'
		age = (now - h.time.jd) / 365.2425
		out = ['<p>%s %s: age %d</p>' % ('Of the radix at this chart,' if self.radix else 'Today,', jdstr(h, now), int(age))]
		ascsign = int(h.houses.ascmc[houses.Houses.ASC] // 30.0)
		prof = (ascsign + int(age)) % 12
		night = lotswnd.LotsWnd.isNightChart(h)
		lord = rulers(h.options, prof * 30.0, night)[0]
		out.append(self.head('Annual profection'))
		out.append(self.rows([('Ascendant profected to', signname(prof)), ('Lord of the year', planetname(lord))]))
		fir = self.firdariaNow(h, night, age)
		if fir:
			out.append(self.head('Firdaria'))
			out.append(self.rows(fir))
		for lot in (zodiacalreleasing.FORTUNE, zodiacalreleasing.SPIRIT):
			first, periods = zodiacalreleasing.releasing(h, lot, max(int(age) + 2, 1))
			cur = [p for p in periods if p.start <= now < p.end]
			if cur:
				out.append(self.head('Zodiacal releasing from ' + zodiacalreleasing.LOTNAMES[lot]))
				out.append(self.rows([('Level %d' % p.level, '%s (%s, until %s)%s' % (signname(p.sign), planetname(rulers(h.options, p.sign * 30.0, night)[0]),
					jdstr(h, p.end), ', loosing of the bond' if p.loosing else '')) for p in cur]))
		seq, periods = decennials.decennials(h, max(int(age) + 2, 1))
		cur = [p for p in periods if p.start <= now < p.end]
		if cur:
			out.append(self.head('Decennials'))
			out.append(self.rows([('Level %d' % p.level, '%s (until %s)' % (planetname(p.planet), jdstr(h, p.end))) for p in cur]))
		out.append('<p><font color="$GREY" size="-1">Profection by whole signs from the Ascendant; the tables (Tables menu) give the full periods.</font></p>')
		return ''.join(out)

	def firdariaNow(self, h, night, age):
		"""The firdaria period and sub-period of chart h at an age, with Morinus's sequences."""
		try:
			f = firdaria.Firdaria(h.time.origyear, h.time.origmonth, h.time.origday, h.options, not night)
		except (ValueError, OverflowError):
			return None
		seq = f.dailyplanetaryyears if f.isdaily else f.nightlyplanetaryyearsbonatti if h.options.isfirbonatti else f.nightlyplanetaryyearsalbiruni
		total = sum(y for p, y in seq)
		t = age % total
		for index, (planet, years) in enumerate(seq):
			if t < years:
				pairs = [('Period', '%s (%d years)' % (planetname(planet), years))]
				if not f.isNode(index):
					sub = int(t / (years / 7.0))
					k = index
					for _ in range(sub):
						k = f.nextIndex(k)
					pairs.append(('Sub-period', planetname(seq[k][0])))
				return pairs
			t -= years
		return None


def traditional_phase(rep):
	from hor_tools import output as hout
	return hout._format_synodic(rep) or None
