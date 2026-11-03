"""Hyleg and alcocoden (hyleg.py) as a Morinus table: the candidates examined
in order with the reasons, the alcocoden candidates, and the planetary years
of the alcocoden with the conditions the astrologer weighs."""

import i18n
import wx
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
import hyleg
import util

ASPECTS = {0: 'conjunction', 60: 'sextile', 90: 'square', 120: 'trine', 180: 'opposition'}
CAUTION = 'The course: rules about the length of life are delicate and uncertain; never state them categorically.'


def text(item):
	"""A (format, args...) tuple of hyleg.py, translated."""
	fmt, args = item[0], item[1:]
	args = tuple(i18n.tr(a) if isinstance(a, str) else a for a in args)
	return i18n.tr(fmt) % args if args else i18n.tr(fmt)


class HylegWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		self.mainfr = mainfr
		self.FONT_SIZE = int(21 * self.options.tablesize)
		self.SPACE = self.FONT_SIZE // 2
		self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
		self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
		self.rows = self.makeRows(hyleg.calculate(chrt))

		measure = ImageDraw.Draw(Image.new('RGB', (1, 1)))
		width = lambda txt: measure.textbbox((0, 0), txt, self.fntText)[2]
		self.COL1 = max(width(r[0]) for r in self.rows) + 2 * self.SPACE
		self.COL2 = max([width(r[1]) for r in self.rows] + [width(i18n.tr(CAUTION)), 12 * self.FONT_SIZE]) + 2 * self.SPACE
		self.TABLE_WIDTH = self.COL1 + self.COL2
		self.TABLE_HEIGHT = len(self.rows) * self.LINE_HEIGHT
		self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
		self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + self.LINE_HEIGHT + commonwnd.CommonWnd.BORDER
		self.SetVirtualSize((self.WIDTH, self.HEIGHT))
		self.drawBkg()

	def makeRows(self, res):
		"""(label, text, kind) rows; kind 'head' draws a section line."""
		tr = i18n.tr
		rows = [(tr('Hyleg'), '', 'head'),
			(tr('Chart'), '%s, %s' % (tr('day chart' if res.day else 'night chart'),
				tr('after a new Moon' if res.newmoon else 'after a full Moon')), '')]
		for c in res.candidates:
			status = tr('hyleg') if c.accepted else tr('rejected')
			rows.append((tr(c.name), '%s: %s' % (status, '; '.join(text(r) for r in c.reasons)), ''))
		rows.append((tr('Hyleg'), tr(res.hyleg.name) if res.hyleg else tr('none'), 'bold'))
		rows.append((tr('Alcocoden'), '', 'head'))
		for pl, pts, kinds, asp, orb, house, strength in res.alcocodens:
			rows.append((tr(hyleg.NAMES[pl]), tr('%s (%d points), %s %.1f\xb0, house %d (Porphyry), %s') % (
				', '.join(tr(k) for k in kinds), pts, tr(ASPECTS[asp]), orb, house, tr(strength)), ''))
		if res.hyleg is not None and not res.alcocodens:
			rows.append(('', tr('no ruler of the place of the hyleg aspects it'), ''))
		rows.append((tr('Alcocoden'), tr(hyleg.NAMES[res.alcocoden]) if res.alcocoden is not None else tr('none'), 'bold'))
		for item in res.conditions:
			rows.append(('', text(item), ''))
		return rows

	def getExt(self):
		return '_Hyleg'

	def tableRows(self):
		return [[r[0], r[1]] for r in self.rows]

	def drawBkg(self):
		self.bkgclr = (255, 255, 255) if self.bw else self.options.clrbackground
		self.SetBackgroundColour(self.bkgclr)
		tableclr = (0, 0, 0) if self.bw else self.options.clrtable
		txtclr = (0, 0, 0) if self.bw else self.options.clrtexts
		img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
		draw = ImageDraw.Draw(img)
		BOR = commonwnd.CommonWnd.BORDER
		y = BOR
		for label, txt, kind in self.rows:
			draw.line((BOR, y, BOR + self.TABLE_WIDTH, y), fill=tableclr)
			if kind == 'head':
				draw.line((BOR, y + 2, BOR + self.TABLE_WIDTH, y + 2), fill=tableclr)
			x = BOR
			for i, cell in enumerate((label, txt)):
				draw.line((x, y, x, y + self.LINE_HEIGHT), fill=tableclr)
				if cell:
					w, h = draw.textbbox((0, 0), cell, self.fntText)[2:]
					draw.text((x + self.SPACE, y + (self.LINE_HEIGHT - h) // 2), cell, fill=txtclr, font=self.fntText)
					if kind in ('head', 'bold'):	# a second pass, one pixel right: bold
						draw.text((x + self.SPACE + 1, y + (self.LINE_HEIGHT - h) // 2), cell, fill=txtclr, font=self.fntText)
				x += (self.COL1, self.COL2)[i]
			draw.line((x, y, x, y + self.LINE_HEIGHT), fill=tableclr)
			y += self.LINE_HEIGHT
		draw.line((BOR, y, BOR + self.TABLE_WIDTH, y), fill=tableclr)
		w, h = draw.textbbox((0, 0), i18n.tr(CAUTION), self.fntText)[2:]
		draw.text((BOR, y + (self.LINE_HEIGHT - h) // 2), i18n.tr(CAUTION), fill=txtclr, font=self.fntText)
		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


class HylegFrame(wx.Frame):

	def __init__(self, parent, title, chrt, options):
		wx.Frame.__init__(self, parent, -1, i18n.tr(title), wx.DefaultPosition, wx.Size(640, 400))
		self.w = HylegWnd(self, chrt, options, parent)
		self.SetSize((min(self.w.WIDTH + 30, 1200), min(self.w.HEIGHT + 50, 900)))
		self.SetMinSize((200, 200))
