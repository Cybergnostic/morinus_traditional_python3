# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, chart, planets, common, commonwnd, Image, ImageDraw, ImageFont, transits, mtexts, util

class TransitMonthWnd(commonwnd.CommonWnd):

    def __init__(self, parent, trans, year, month, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.trans = trans
        self.year = year
        self.month = month
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE / 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        length = len(self.trans)
        self.LINE_NUM = length
        self.COLUMN_NUM = 4
        self.CELL_WIDTH = 8 * self.FONT_SIZE
        self.SMALL_CELL_WIDTH = 4 * self.FONT_SIZE
        self.TITLE_HEIGHT = 2 * self.LINE_HEIGHT
        self.TITLE_WIDTH = self.SMALL_CELL_WIDTH + (self.COLUMN_NUM - 1) * self.CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT
        self.TABLE_WIDTH = self.TITLE_WIDTH
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.RETRYOFFS = 2 * self.FONT_SIZE / 5
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntAspects = ImageFont.truetype(common.common.symbols, 3 * self.FONT_SIZE / 4)
        self.fntSigns = ImageFont.truetype(common.common.symbols, 3 * self.FONT_SIZE / 4)
        self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
        self.fntRText = ImageFont.truetype(common.common.abc, self.FONT_SIZE * 3 / 4)
        self.signs = common.common.signs
        self.txtsp = ' '
        self.txtrs = ('R', 'S')
        self.txtant = ('A', 'CA')
        self.txtascmc = (mtexts.txtstransits['Asc'], mtexts.txtstransits['MC'])
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Tra']

    def drawBkg(self):
        if self.bw:
            self.bkgclr = (255, 255, 255)
        else:
            self.bkgclr = self.options.clrbackground
        self.SetBackgroundColour(self.bkgclr)
        tableclr = self.options.clrtable
        if self.bw:
            tableclr = (0, 0, 0)
        img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
        draw = ImageDraw.Draw(img)
        BOR = commonwnd.CommonWnd.BORDER
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        draw.rectangle(((BOR, BOR), (BOR + self.TITLE_WIDTH, BOR + self.TITLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
        mtxt = mtexts.txtstransits['Transits'] + ' ' + str(self.year) + '.' + mtexts.months[(self.month - 1)]
        w, h = draw.textsize(mtxt, self.fntText)
        draw.text((BOR + (self.TITLE_WIDTH - w) / 2, BOR + (self.LINE_HEIGHT - h) / 2), mtxt, fill=txtclr, font=self.fntText)
        txt = (
         mtexts.txtstransits['Day'], mtexts.txtstransits['Time'] + ' (' + mtexts.txtstransits['GMT'] + ')', mtexts.txtstransits['Transit'].capitalize(), mtexts.txtstransits['House'])
        offs = (self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        summa = 0
        for i in range(len(txt)):
            w, h = draw.textsize(txt[i], self.fntText)
            draw.text((BOR + summa + (offs[i] - w) / 2, BOR + self.TITLE_HEIGHT / 2 + (self.TITLE_HEIGHT / 2 - h) / 2), txt[i], fill=txtclr, font=self.fntText)
            summa += offs[i]

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        for i in range(len(self.trans)):
            self.drawline(draw, x, y + i * self.LINE_HEIGHT, tableclr, i)

        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)

    def drawline(self, draw, x, y, clr, idx):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        BOR = commonwnd.CommonWnd.BORDER
        summa = 0
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        for i in range(self.COLUMN_NUM + 1):
            draw.line((x + summa + offs[i], y, x + summa + offs[i], y + self.LINE_HEIGHT), fill=clr)
            if i == 1:
                txt = str(self.trans[idx].day)
                w, h = draw.textsize(txt, self.fntText)
                draw.text((x + summa + (offs[i] - w) / 2, y + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
            elif i == 2:
                d, m, s = util.decToDeg(self.trans[idx].time)
                txt = str(d).rjust(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                w, h = draw.textsize(txt, self.fntText)
                draw.text((x + summa + (offs[i] - w) / 2, y + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
            elif i == 3:
                txtpt = common.common.planets[self.trans[idx].plt]
                clrp1 = (0, 0, 0)
                if not self.bw:
                    clrp1 = self.options.clraux
                wpt, hpt = draw.textsize(txtpt, self.fntMorinus)
                wsp, hsp = draw.textsize(self.txtsp, self.fntText)
                if self.trans[idx].objtype == transits.Transit.ASCMC:
                    txtasp = common.common.aspects[self.trans[idx].aspect]
                    wasp, hasp = draw.textsize(txtasp, self.fntAspects)
                    wascmc, hascmc = draw.textsize(self.txtascmc[self.trans[idx].obj], self.fntText)
                    offset = (offs[i] - (wpt + wsp + wasp + wsp + wascmc)) / 2
                    draw.text((x + summa + offset, y + (self.LINE_HEIGHT - hpt) / 2), txtpt, fill=clrp1, font=self.fntMorinus)
                    clrasp = (0, 0, 0)
                    if not self.bw:
                        clrasp = self.options.clraspect[self.trans[idx].aspect]
                    draw.text((x + summa + offset + wpt + wsp, y + (self.LINE_HEIGHT - hasp) / 2), common.common.aspects[self.trans[idx].aspect], fill=clrasp, font=self.fntAspects)
                    draw.text((x + summa + offset + wpt + wsp + wasp + wsp, y + (self.LINE_HEIGHT - hascmc) / 2), self.txtascmc[self.trans[idx].obj], fill=txtclr, font=self.fntText)
                elif self.trans[idx].objtype == transits.Transit.SIGN:
                    s2 = self.trans[idx].obj
                    s1 = 11
                    if s2 > 0:
                        s1 = s2 - 1
                    txts1 = self.signs[s1]
                    ws1, hs1 = draw.textsize(txts1, self.fntSigns)
                    txtsepa = '|'
                    wse, hse = draw.textsize(txtsepa, self.fntText)
                    txts2 = self.signs[s2]
                    ws2, hs2 = draw.textsize(txts2, self.fntSigns)
                    offset = (offs[i] - (wpt + wsp + ws1 + wse + ws2)) / 2
                    draw.text((x + summa + offset, y + (self.LINE_HEIGHT - hpt) / 2), txtpt, fill=clrp1, font=self.fntMorinus)
                    draw.text((x + summa + offset + wpt + wsp, y + (self.LINE_HEIGHT - hs1) / 2), txts1, fill=txtclr, font=self.fntSigns)
                    draw.text((x + summa + offset + wpt + wsp + ws1, y + (self.LINE_HEIGHT - hse) / 2), txtsepa, fill=txtclr, font=self.fntText)
                    draw.text((x + summa + offset + wpt + wsp + ws1 + wse, y + (self.LINE_HEIGHT - hs2) / 2), txts2, fill=txtclr, font=self.fntSigns)
                elif self.trans[idx].objtype == transits.Transit.PLANET:
                    txtasp = common.common.aspects[self.trans[idx].aspect]
                    wasp, hasp = draw.textsize(txtasp, self.fntSigns)
                    txtpr = common.common.planets[self.trans[idx].obj]
                    wpr, hpr = draw.textsize(txtpr, self.fntMorinus)
                    wrr, hrr = (0, 0)
                    if self.trans[idx].objretr != transits.Transits.NONE:
                        wrr, hrr = draw.textsize(self.txtrs[self.trans[idx].objretr], self.fntRText)
                    offset = (self.CELL_WIDTH - (wpt + wsp + wasp + wsp + wpr + wrr)) / 2
                    draw.text((x + summa + offset, y + (self.LINE_HEIGHT - hpt) / 2), txtpt, fill=clrp1, font=self.fntMorinus)
                    clrasp = (0, 0, 0)
                    if not self.bw:
                        clrasp = self.options.clraspect[self.trans[idx].aspect]
                    draw.text((x + summa + offset + wpt + wsp, y + (self.LINE_HEIGHT - hasp) / 2), common.common.aspects[self.trans[idx].aspect], fill=clrasp, font=self.fntAspects)
                    clrp2 = (0, 0, 0)
                    if not self.bw:
                        objidx = self.trans[idx].obj
                        if objidx >= planets.Planets.BODIES_NUM - 1:
                            objidx -= 1
                        clrp2 = self.options.clrplanets[objidx]
                    draw.text((x + summa + offset + wpt + wsp + wasp + wsp, y + (self.LINE_HEIGHT - hpr) / 2), txtpr, fill=clrp2, font=self.fntMorinus)
                    if self.trans[idx].objretr != transits.Transits.NONE:
                        draw.text((x + summa + offset + wpt + wsp + wasp + wsp + wpr, y + (self.LINE_HEIGHT - hrr) / 2 + self.RETRYOFFS), self.txtrs[self.trans[idx].objretr], fill=clrp2, font=self.fntRText)
                elif self.trans[idx].objtype == transits.Transit.ANTISCION or self.trans[idx].objtype == transits.Transit.CONTRAANTISCION:
                    txtpr = common.common.planets[self.trans[idx].obj]
                    wpr, hpr = draw.textsize(txtpr, self.fntMorinus)
                    wrr, hrr = (0, 0)
                    if self.trans[idx].objretr != transits.Transits.NONE:
                        wrr, hrr = draw.textsize(self.txtrs[self.trans[idx].objretr], self.fntRText)
                    txtasp = common.common.aspects[self.trans[idx].aspect]
                    wasp, hasp = draw.textsize(txtasp, self.fntSigns)
                    ii = 0
                    if self.trans[idx].objtype == transits.Transit.CONTRAANTISCION:
                        ii = 1
                    want, hant = draw.textsize(self.txtant[ii], self.fntText)
                    offset = (self.CELL_WIDTH - (wpt + wsp + wasp + wsp + want + wpr + wrr)) / 2
                    draw.text((x + summa + offset, y + (self.LINE_HEIGHT - hpt) / 2), txtpt, fill=clrp1, font=self.fntMorinus)
                    clrasp = (0, 0, 0)
                    if not self.bw:
                        clrasp = self.options.clraspect[self.trans[idx].aspect]
                    draw.text((x + summa + offset + wpt + wsp, y + (self.LINE_HEIGHT - hasp) / 2), common.common.aspects[self.trans[idx].aspect], fill=clrasp, font=self.fntAspects)
                    draw.text((x + summa + offset + wpt + wsp + wasp + wsp, y + (self.LINE_HEIGHT - hant) / 2), self.txtant[ii], fill=txtclr, font=self.fntText)
                    clrp2 = (0, 0, 0)
                    if not self.bw:
                        objidx = self.trans[idx].obj
                        if objidx >= planets.Planets.BODIES_NUM - 1:
                            objidx -= 1
                        clrp2 = self.options.clrplanets[objidx]
                    draw.text((x + summa + offset + wpt + wsp + wasp + wsp + want, y + (self.LINE_HEIGHT - hpr) / 2), txtpr, fill=clrp2, font=self.fntMorinus)
                    if self.trans[idx].objretr != transits.Transits.NONE:
                        draw.text((x + summa + offset + wpt + wsp + wasp + wsp + want + wpr, y + (self.LINE_HEIGHT - hrr) / 2 + self.RETRYOFFS), self.txtrs[self.trans[idx].objretr], fill=clrp2, font=self.fntRText)
                elif self.trans[idx].objtype == transits.Transit.LOF:
                    txtasp = common.common.aspects[self.trans[idx].aspect]
                    wasp, hasp = draw.textsize(txtasp, self.fntSigns)
                    txtpr = common.common.fortune
                    wpr, hpr = draw.textsize(txtpr, self.fntMorinus)
                    offset = (self.CELL_WIDTH - (wpt + wsp + wasp + wsp + wpr)) / 2
                    draw.text((x + summa + offset, y + (self.LINE_HEIGHT - hpt) / 2), txtpt, fill=clrp1, font=self.fntMorinus)
                    clrasp = (0, 0, 0)
                    if not self.bw:
                        clrasp = self.options.clraspect[self.trans[idx].aspect]
                    draw.text((x + summa + offset + wpt + wsp, y + (self.LINE_HEIGHT - hasp) / 2), common.common.aspects[self.trans[idx].aspect], fill=clrasp, font=self.fntAspects)
                    clrp2 = (0, 0, 0)
                    if not self.bw:
                        clrp2 = self.options.clrLoF
                    draw.text((x + summa + offset + wpt + wsp + wasp + wsp, y + (self.LINE_HEIGHT - hpr) / 2), txtpr, fill=clrp2, font=self.fntMorinus)
            elif i == 4:
                txt = common.common.housenames[self.trans[idx].house]
                w, h = draw.textsize(txt, self.fntText)
                draw.text((x + summa + (offs[i] - w) / 2, y + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
            summa += offs[i]