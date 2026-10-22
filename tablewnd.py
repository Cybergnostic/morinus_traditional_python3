"""Native Morinus tables made of sections of rows (the look of Morinus's own
tables: lines in the table colour, FreeSans text, Morinus symbols), used by the
tables added to this version."""

import i18n
import wx
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
import chart
import util

# special cells: (GLYPH, Morinus.ttf letters), (POSITION, longitude), (SIGN, sign index)
GLYPH, POSITION, SIGN = 'glyph', 'position', 'sign'


class Section:
	"""Rows of cells under optional headers; colours: per row, None for the text colour."""

	def __init__(self, rows, headers=None, colours=None):
		self.rows = rows
		self.headers = headers
		self.colours = colours or [None] * len(rows)


class TableWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		self.mainfr = mainfr
		self.FONT_SIZE = int(21 * self.options.tablesize)
		self.SPACE = self.FONT_SIZE // 2
		self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
		self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
		self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
		self.signs = common.common.signs
		self.sections = []
		self.notes = []

	def layout(self):
		"""Sizes the table to self.sections and self.notes and draws it."""
		measure = ImageDraw.Draw(Image.new('RGB', i18n.tr((1, 1))))
		self.cols = []
		width = max([measure.textbbox((0, 0), i18n.tr(n), self.fntText)[2] for n in self.notes] + [0])
		height = commonwnd.CommonWnd.BORDER
		for sec in self.sections:
			lines = ([sec.headers] if sec.headers else []) + sec.rows
			ncols = max([len(l) for l in lines] + [0])
			cols = [max([self.cellWidth(measure, l[i]) for l in lines if i < len(l)] + [0]) for i in range(ncols)]
			self.cols.append(cols)
			width = max(width, sum(cols))
			height += len(lines) * self.LINE_HEIGHT + self.LINE_HEIGHT
		height += len(self.notes) * self.LINE_HEIGHT
		self.TABLE_WIDTH = width
		self.WIDTH = commonwnd.CommonWnd.BORDER + width + commonwnd.CommonWnd.BORDER
		self.HEIGHT = height + commonwnd.CommonWnd.BORDER
		self.SetVirtualSize((self.WIDTH, self.HEIGHT))
		self.drawBkg()

	def position(self, lon):
		if self.options.ayanamsha != 0:
			lon = util.normalize(lon - self.chart.ayanamsha)
		d, m, s = util.decToDeg(lon)
		return str(d % chart.Chart.SIGN_DEG).rjust(2) + '\xb0' + str(m).zfill(2) + "'" + str(s).zfill(2) + '"', self.signs[d // chart.Chart.SIGN_DEG]

	def cellWidth(self, draw, cell):
		if isinstance(cell, tuple) and cell[0] in (GLYPH, SIGN):
			txt = cell[1] if cell[0] == GLYPH else self.signs[cell[1]]
			w = max(draw.textbbox((0, 0), txt, self.fntMorinus)[2], self.FONT_SIZE)
		elif isinstance(cell, tuple):
			txt, sign = self.position(cell[1])
			w = draw.textbbox((0, 0), txt + ' ', self.fntText)[2] + draw.textbbox((0, 0), sign, self.fntMorinus)[2]
		else:
			w = draw.textbbox((0, 0), i18n.tr(cell), self.fntText)[2]
		return w + 2 * self.SPACE

	def drawCell(self, draw, x, y, width, cell, clr):
		if isinstance(cell, tuple) and cell[0] in (GLYPH, SIGN):
			txt = cell[1] if cell[0] == GLYPH else self.signs[cell[1]]
			w, h = draw.textbbox((0, 0), txt, self.fntMorinus)[2:]
			draw.text((x + (width - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clr, font=self.fntMorinus)
		elif isinstance(cell, tuple):
			txt, sign = self.position(cell[1])
			w, h = draw.textbbox((0, 0), txt + ' ', self.fntText)[2:]
			wsg, hsg = draw.textbbox((0, 0), sign, self.fntMorinus)[2:]
			x += (width - w - wsg) // 2
			draw.text((x, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clr, font=self.fntText)
			draw.text((x + w, y + (self.LINE_HEIGHT - hsg) // 2), sign, fill=clr, font=self.fntMorinus)
		elif cell:
			cell = i18n.tr(cell)	# the texts of the added tables are English in the code
			w, h = draw.textbbox((0, 0), cell, self.fntText)[2:]
			draw.text((x + (width - w) // 2, y + (self.LINE_HEIGHT - h) // 2), cell, fill=clr, font=self.fntText)

	def drawBkg(self):
		if self.bw:
			self.bkgclr = (255, 255, 255)
		else:
			self.bkgclr = self.options.clrbackground
		self.SetBackgroundColour(self.bkgclr)
		tableclr = (0, 0, 0) if self.bw else self.options.clrtable
		txtclr = (0, 0, 0) if self.bw else self.options.clrtexts
		img = Image.new('RGB', i18n.tr((self.WIDTH, self.HEIGHT)), i18n.tr(self.bkgclr))
		draw = ImageDraw.Draw(img)
		x0 = commonwnd.CommonWnd.BORDER
		y = commonwnd.CommonWnd.BORDER
		self.rowspans = []	# (section, row, top, bottom) for rowAt
		for si, sec in enumerate(self.sections):
			cols = self.cols[si]
			width = sum(cols)
			lines = [(sec.headers, None, True)] if sec.headers else []
			lines += [(row, sec.colours[i], False) for i, row in enumerate(sec.rows)]
			ri = 0
			for cells, clr, header in lines:
				clr = txtclr if self.bw or clr is None else clr
				draw.line((x0, y, x0 + width, y), fill=tableclr)
				x = x0
				for i, cell in enumerate(cells):
					draw.line((x, y, x, y + self.LINE_HEIGHT), fill=tableclr)
					self.drawCell(draw, x, y, cols[i], cell, clr)
					x += cols[i]
				draw.line((x0 + width, y, x0 + width, y + self.LINE_HEIGHT), fill=tableclr)
				if not header:
					self.rowspans.append((si, ri, y, y + self.LINE_HEIGHT))
					ri += 1
				y += self.LINE_HEIGHT
				if header:
					draw.line((x0, y - 2, x0 + width, y - 2), fill=tableclr)
			draw.line((x0, y, x0 + width, y), fill=tableclr)
			y += self.LINE_HEIGHT
		for note in self.notes:
			note = i18n.tr(note)
			w, h = draw.textbbox((0, 0), note, self.fntText)[2:]
			draw.text((x0, y - self.LINE_HEIGHT + (self.LINE_HEIGHT - h) // 2), note, fill=txtclr, font=self.fntText)
			y += self.LINE_HEIGHT

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)

	def rowAt(self, pos):
		"""(section, row) under a mouse position in the window, or None."""
		x, y = self.CalcUnscrolledPosition(pos)
		for si, ri, top, bottom in self.rowspans:
			if top <= y < bottom:
				return si, ri
		return None


class TableFrame(wx.Frame):
	"""A frame sized to its table."""

	def __init__(self, parent, title, make):
		wx.Frame.__init__(self, parent, -1, i18n.tr(title), wx.DefaultPosition, wx.Size(640, 400))
		self.w = make(self)
		self.SetSize((min(self.w.WIDTH + 30, 1600), min(self.w.HEIGHT + 50, 900)))
		self.SetMinSize((200, 200))
