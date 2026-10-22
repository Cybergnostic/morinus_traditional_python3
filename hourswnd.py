# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
import wx
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import astrology
import chart
import common
import commonwnd
import hours
import util
import mtexts

class HoursWnd(commonwnd.CommonWnd):
    HOURSPERHALFDAY = 12

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE // 2
        self.COLUMN_NUM = 2
        self.LINE_NUM = HoursWnd.HOURSPERHALFDAY
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.SMALL_CELL_WIDTH = 2 * self.FONT_SIZE
        self.CELL_WIDTH = 8 * self.FONT_SIZE
        self.TITLE_HEIGHT = 3 * self.LINE_HEIGHT
        self.TITLE_WIDTH = self.SMALL_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Hrs']

    def drawBkg(self):
        if self.bw:
            self.bkgclr = (255, 255, 255)
        else:
            self.bkgclr = self.options.clrbackground
        self.SetBackgroundColour(self.bkgclr)
        tableclr = self.options.clrtable
        if self.bw:
            tableclr = (0, 0, 0)
        img = Image.new('RGB', i18n.tr((self.WIDTH, self.HEIGHT)), i18n.tr(self.bkgclr))
        draw = ImageDraw.Draw(img)
        BOR = commonwnd.CommonWnd.BORDER
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        draw.rectangle(((BOR, BOR), (BOR + self.TITLE_WIDTH, BOR + self.TITLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
        # times in the chart's own time (they were UT, beside a local mean birth time)
        self.offs = self.chart.time.localoffset()
        jdlocal = self.chart.time.jd + self.offs
        jy, jm, jd, jh = astrology.swe_revjul(jdlocal, 1)
        hh, mm, ss = util.decToDeg(jh)
        txt = mtexts.txtshours['LocalBirthTime'] + ': ' + str(hh) + ':' + str(mm).zfill(2) + ':' + str(ss).zfill(2)
        w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
        draw.text((BOR + (self.TITLE_WIDTH - w) // 2, BOR + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
        if self.chart.time.ph != None:
            rh, rm, rs = self.chart.time.ph.revTime(self.chart.time.ph.risetime + self.offs, self.chart.time.cal)
            sh, sm, ss = self.chart.time.ph.revTime(self.chart.time.ph.settime + self.offs, self.chart.time.cal)
            if self.chart.time.ph.daytime:
                txt1 = mtexts.txtshours['RiseTime'] + ': ' + str(rh) + ':' + str(rm).zfill(2) + ':' + str(rs).zfill(2)
                txt2 = mtexts.txtshours['SetTime'] + ': ' + str(sh) + ':' + str(sm).zfill(2) + ':' + str(ss).zfill(2)
            else:
                txt2 = mtexts.txtshours['RiseTime'] + ': ' + str(rh) + ':' + str(rm).zfill(2) + ':' + str(rs).zfill(2)
                txt1 = mtexts.txtshours['SetTime'] + ': ' + str(sh) + ':' + str(sm).zfill(2) + ':' + str(ss).zfill(2)
            w, h = draw.textbbox((0, 0), txt1, self.fntText)[2:]
            draw.text((BOR + (self.TITLE_WIDTH - w) // 2, BOR + self.LINE_HEIGHT + (self.LINE_HEIGHT - h) // 2), txt1, fill=txtclr, font=self.fntText)
            w, h = draw.textbbox((0, 0), txt2, self.fntText)[2:]
            draw.text((BOR + (self.TITLE_WIDTH - w) // 2, BOR + 2 * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) // 2), txt2, fill=txtclr, font=self.fntText)
            x = BOR
            y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY
            draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
            self.begtime = 0.0
            if self.chart.time.ph.daytime:
                self.begtime = self.chart.time.ph.risetime
            else:
                self.begtime = self.chart.time.ph.settime
            for i in range(int(HoursWnd.HOURSPERHALFDAY)):
                self.drawline(draw, x, y + i * self.LINE_HEIGHT, tableclr, i)

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)
        return

    def drawline(self, draw, x, y, clr, idx):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        BOR = commonwnd.CommonWnd.BORDER
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        hr = 0
        endtime = 0.0
        if self.chart.time.ph.daytime:
            endtime = self.chart.time.ph.risetime + self.chart.time.ph.hrlen * (idx + 1)
            hr = idx
        else:
            endtime = self.chart.time.ph.settime + self.chart.time.ph.hrlen * (idx + 1)
            hr = idx + int(HoursWnd.HOURSPERHALFDAY)
        planetaryhour = hours.PlanetaryHours.PHs[self.chart.time.ph.weekday][hr]
        summa = 0
        for i in range(self.COLUMN_NUM + 1 + 1):
            draw.line((x + summa + offs[i], y, x + summa + offs[i], y + self.LINE_HEIGHT), fill=clr)
            if i == 1:
                tclr = (0, 0, 0)
                if not self.bw:
                    tclr = self.options.clrplanets[planetaryhour]
                txtpl = common.common.planets[planetaryhour]
                w, h = draw.textbbox((0, 0), txtpl, self.fntMorinus)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txtpl, fill=tclr, font=self.fntMorinus)
            elif i > 1:
                h, m, s = (0, 0, 0)
                if i == 2:
                    h, m, s = self.chart.time.ph.revTime(self.begtime + self.offs, self.chart.time.cal)
                else:
                    h, m, s = self.chart.time.ph.revTime(endtime + self.offs, self.chart.time.cal)
                txt = str(h) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                draw.text((x + summa + (offs[i] - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
                self.begtime = endtime
            summa += offs[i]