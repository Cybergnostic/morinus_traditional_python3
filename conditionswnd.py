"""Planetary conditions as a native Morinus table (the analysis comes from traditional.py)."""

import wx
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
import chart
import planets
import traditional
import util
from hor_tools import output as hout

# hor_tools planet names -> Morinus planet index
PLANETIDS = {'Saturn': planets.Planets.SATURN, 'Jupiter': planets.Planets.JUPITER, 'Mars': planets.Planets.MARS, 'Sun': planets.Planets.SUN,
	'Venus': planets.Planets.VENUS, 'Mercury': planets.Planets.MERCURY, 'Moon': planets.Planets.MOON}
HEADERS = ('', 'Position', 'House', 'Sect', 'Hayz / halb', 'Orientation', 'Synodic phase', 'Station', 'Motion', 'Joy', 'Latitude', 'Via Combusta')
NOTE = "Sect from the Sun's true altitude; whole-sign houses; Via Combusta 19\xb0 Libra - 3\xb0 Scorpio"
GLYPH, POSITION = 'glyph', 'position'


class ConditionsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		self.mainfr = mainfr
		self.FONT_SIZE = int(21 * self.options.tablesize)
		self.SPACE = self.FONT_SIZE // 2
		self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
		self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
		self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
		self.signs = common.common.signs

		self.summary = []
		self.rows = []
		try:
			self.analyse(traditional.analyse(chrt))
		except traditional.NotAvailable as e:
			self.summary = [('Not available for this chart', str(e))]

		measure = ImageDraw.Draw(Image.new('RGB', (1, 1)))
		self.SUMMARY_COLS = [max(self.cellWidth(measure, row[i]) for row in self.summary) for i in range(2)]
		self.COLS = [max([self.cellWidth(measure, HEADERS[i])] + [self.cellWidth(measure, row[i]) for _, row in self.rows]) for i in range(len(HEADERS))] if self.rows else []
		self.TABLE_WIDTH = max(sum(self.SUMMARY_COLS), sum(self.COLS), measure.textbbox((0, 0), NOTE, self.fntText)[2])
		self.HEIGHT = commonwnd.CommonWnd.BORDER + len(self.summary) * self.LINE_HEIGHT
		if self.rows:
			self.HEIGHT += self.LINE_HEIGHT + (1 + len(self.rows)) * self.LINE_HEIGHT + self.LINE_HEIGHT
		self.HEIGHT += commonwnd.CommonWnd.BORDER
		self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
		self.SetVirtualSize((self.WIDTH, self.HEIGHT))
		self.drawBkg()

	def analyse(self, a):
		solar = a.technical.solar
		moon = next((r for r in a.reports if r.planet.name == 'Moon'), None)
		self.summary = [
			('Sect', 'Day' if solar.is_day else 'Night'),
			("Sun's true altitude", '%+.4f\xb0' % solar.sun_true_altitude),
			('Apparent sunrise / sunset', '%s / %s' % (solar.sunrise_local.strftime('%H:%M:%S'), solar.sunset_local.strftime('%H:%M:%S'))),
			('Planetary day / hour ruler', '%s / %s' % (a.technical.day_ruler, a.technical.hour_ruler)),
			('Moon void of course', 'yes' if moon is not None and moon.is_void_of_course else 'no')]
		for r in a.reports:
			p = r.planet
			idx = PLANETIDS[p.name]
			hayz = ', '.join(t for t, on in (('hayz', r.hayz), ('halb', r.halb)) if on) or '-'
			station = {'first': 'first (turning retrograde)', 'second': 'second (turning direct)'}.get(p.station or '', '-')
			motion = '%s, %s, %.2f\xb0/day (%.2fx mean)' % ('retrograde' if p.retrograde else 'direct', r.speed_class, abs(p.speed_long), r.speed_ratio)
			lat = {'north_strengthening': 'north: strengthening', 'south_weakening': 'south: weakening'}.get(r.latitude_condition, 'on the ecliptic')
			self.rows.append((idx, [
				(GLYPH, common.common.planets[idx]),
				(POSITION, self.chart.planets.planets[idx].data[planets.Planet.LON]),
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

	def position(self, lon):
		if self.options.ayanamsha != 0:
			lon = util.normalize(lon - self.chart.ayanamsha)
		d, m, s = util.decToDeg(lon)
		return str(d % chart.Chart.SIGN_DEG).rjust(2) + '\xb0' + str(m).zfill(2) + "'" + str(s).zfill(2) + '"', self.signs[d // chart.Chart.SIGN_DEG]

	def cellWidth(self, draw, cell):
		if isinstance(cell, tuple) and cell[0] == GLYPH:
			w = 2 * self.FONT_SIZE
		elif isinstance(cell, tuple):
			txt, sign = self.position(cell[1])
			w = draw.textbbox((0, 0), txt + ' ', self.fntText)[2] + draw.textbbox((0, 0), sign, self.fntMorinus)[2]
		else:
			w = draw.textbbox((0, 0), cell, self.fntText)[2]
		return w + 2 * self.SPACE

	def drawCell(self, draw, x, y, width, cell, clr):
		if isinstance(cell, tuple) and cell[0] == GLYPH:
			w, h = draw.textbbox((0, 0), cell[1], self.fntMorinus)[2:]
			draw.text((x + (width - w) // 2, y + (self.LINE_HEIGHT - h) // 2), cell[1], fill=clr, font=self.fntMorinus)
		elif isinstance(cell, tuple):
			txt, sign = self.position(cell[1])
			w, h = draw.textbbox((0, 0), txt + ' ', self.fntText)[2:]
			wsg, hsg = draw.textbbox((0, 0), sign, self.fntMorinus)[2:]
			x += (width - w - wsg) // 2
			draw.text((x, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clr, font=self.fntText)
			draw.text((x + w, y + (self.LINE_HEIGHT - hsg) // 2), sign, fill=clr, font=self.fntMorinus)
		elif cell:
			w, h = draw.textbbox((0, 0), cell, self.fntText)[2:]
			draw.text((x + (width - w) // 2, y + (self.LINE_HEIGHT - h) // 2), cell, fill=clr, font=self.fntText)

	def drawTable(self, draw, y, cols, lines, tableclr):
		"""lines: (cells, colour, header); a double line under a header line"""
		x0 = commonwnd.CommonWnd.BORDER
		width = sum(cols)
		for cells, clr, header in lines:
			draw.line((x0, y, x0 + width, y), fill=tableclr)
			x = x0
			for i, cell in enumerate(cells):
				draw.line((x, y, x, y + self.LINE_HEIGHT), fill=tableclr)
				self.drawCell(draw, x, y, cols[i], cell, clr)
				x += cols[i]
			draw.line((x, y, x, y + self.LINE_HEIGHT), fill=tableclr)
			y += self.LINE_HEIGHT
			if header:
				draw.line((x0, y - 2, x0 + width, y - 2), fill=tableclr)
		draw.line((x0, y, x0 + width, y), fill=tableclr)
		return y

	def drawBkg(self):
		if self.bw:
			self.bkgclr = (255, 255, 255)
		else:
			self.bkgclr = self.options.clrbackground
		self.SetBackgroundColour(self.bkgclr)
		tableclr = (0, 0, 0) if self.bw else self.options.clrtable
		txtclr = (0, 0, 0) if self.bw else self.options.clrtexts
		img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
		draw = ImageDraw.Draw(img)

		y = self.drawTable(draw, commonwnd.CommonWnd.BORDER, self.SUMMARY_COLS, [(row, txtclr, False) for row in self.summary], tableclr)
		if self.rows:
			y += self.LINE_HEIGHT
			lines = [(HEADERS, txtclr, True)]
			for idx, cells in self.rows:
				lines.append((cells, (0, 0, 0) if self.bw else self.options.clrplanets[idx], False))
			y = self.drawTable(draw, y, self.COLS, lines, tableclr)
			w, h = draw.textbbox((0, 0), NOTE, self.fntText)[2:]
			draw.text((commonwnd.CommonWnd.BORDER, y + (self.LINE_HEIGHT - h) // 2), NOTE, fill=txtclr, font=self.fntText)

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


class ConditionsFrame(wx.Frame):

	def __init__(self, parent, title, chrt, options):
		wx.Frame.__init__(self, parent, -1, title + ' - Planetary conditions', wx.DefaultPosition, wx.Size(640, 400))
		self.w = ConditionsWnd(self, chrt, options, parent)
		self.SetSize((min(self.w.WIDTH + 30, 1600), min(self.w.HEIGHT + 50, 900)))
		self.SetMinSize((200, 200))
