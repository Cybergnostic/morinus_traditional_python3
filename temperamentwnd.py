"""Temperament worksheet as a native Morinus table (the analysis comes from traditional.py)."""

import wx
import common
import commonwnd
from PIL import Image
from PIL import ImageDraw
import traditional
import util

QUALITIES = ('K', 'S', 'M', 'F')
KEY = 'K choleric   S sanguine   M melancholic   F phlegmatic'


class TemperamentWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE // 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)

        self.rows = []
        self.totals = None
        self.dominant = ''
        try:
            t = traditional.analyse(chrt).technical.temperament
            self.rows = [(row.factor, '; '.join(row.evidence) or '-', [row.scores[q] for q in QUALITIES]) for row in t.rows]
            self.totals = [t.totals[q] for q in QUALITIES]
            self.dominant = ', '.join(t.dominant)
        except traditional.NotAvailable as e:
            self.dominant = 'Not available for this chart (%s)' % e

        # column widths from the longest texts
        measure = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        width = lambda txt: measure.textbbox((0, 0), txt, self.fntText)[2]
        self.FACTOR_WIDTH = max([width(r[0]) for r in self.rows] + [width('Highest'), width('Factor')]) + 2 * self.SPACE
        self.EVIDENCE_WIDTH = max([width(r[1]) for r in self.rows] + [width(self.dominant), width(KEY), 10 * self.FONT_SIZE]) + 2 * self.SPACE
        self.SCORE_WIDTH = 2 * self.FONT_SIZE
        self.COLS = (self.FACTOR_WIDTH, self.EVIDENCE_WIDTH) + (self.SCORE_WIDTH,) * len(QUALITIES)
        self.TABLE_WIDTH = sum(self.COLS)
        self.LINE_NUM = 1 + len(self.rows) + 2	# header, factors, totals, highest
        self.TABLE_HEIGHT = self.LINE_NUM * self.LINE_HEIGHT
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + self.LINE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.drawBkg()

    def getExt(self):
        return '_Temperament'

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
        BOR = commonwnd.CommonWnd.BORDER

        lines = [(('Factor', 'Evidence') + QUALITIES)]
        lines += [(f, e) + tuple(str(v) for v in scores) for f, e, scores in self.rows]
        if self.totals is not None:
            lines.append(('Totals', '') + tuple(str(v) for v in self.totals))
        else:
            lines.append(('Totals', '', '', '', '', ''))
        lines.append(('Highest', self.dominant, '', '', '', ''))

        y = BOR
        for n, cells in enumerate(lines):
            draw.line((BOR, y, BOR + self.TABLE_WIDTH, y), fill=tableclr)
            x = BOR
            for i, txt in enumerate(cells):
                draw.line((x, y, x, y + self.LINE_HEIGHT), fill=tableclr)
                if txt:
                    w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                    if i == 1 and n > 0:
                        tx = x + self.SPACE	# evidence is left-aligned
                    else:
                        tx = x + (self.COLS[i] - w) // 2
                    draw.text((tx, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
                x += self.COLS[i]
            draw.line((x, y, x, y + self.LINE_HEIGHT), fill=tableclr)
            y += self.LINE_HEIGHT
            # a double line under the header and above the totals
            if n == 0 or n == len(lines) - 3:
                draw.line((BOR, y - 2, BOR + self.TABLE_WIDTH, y - 2), fill=tableclr)
        draw.line((BOR, y, BOR + self.TABLE_WIDTH, y), fill=tableclr)
        w, h = draw.textbbox((0, 0), KEY, self.fntText)[2:]
        draw.text((BOR, y + (self.LINE_HEIGHT - h) // 2), KEY, fill=txtclr, font=self.fntText)

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)


class TemperamentFrame(wx.Frame):

    def __init__(self, parent, title, chrt, options):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(640, 400))
        self.w = TemperamentWnd(self, chrt, options, parent)
        self.SetSize((min(self.w.WIDTH + 30, 1200), min(self.w.HEIGHT + 50, 900)))
        self.SetMinSize((200, 200))
