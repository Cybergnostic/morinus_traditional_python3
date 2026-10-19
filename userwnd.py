# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, chart, userpd, placspec, regiospec, commonwnd, primdirs, common, Image, ImageDraw, ImageFont, util, mtexts

class UserWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, options, mainfr, usr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
        self.parent = parent
        self.chart = chrt
        self.options = options
        self.mainfr = mainfr
        self.usr = usr
        self.bw = self.options.bw
        self.speculum = 0
        if self.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
            self.speculum = 1
        line_num = 0
        for i in range(len(self.options.speculums[self.speculum])):
            if self.options.speculums[self.speculum][i] == True:
                line_num += 1

        BOR = UserWnd.BORDER
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.COLUMN_NUM = 1
        self.SPACE = self.FONT_SIZE / 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.CELL_WIDTH = 8 * self.FONT_SIZE
        self.LINE_NUM = line_num
        self.TABLE_HEIGHT = self.LINE_NUM * self.LINE_HEIGHT
        self.TABLE_WIDTH = (self.COLUMN_NUM + 1) * self.CELL_WIDTH
        self.WIDTH = BOR + self.TABLE_WIDTH + BOR
        self.HEIGHT = BOR + self.TABLE_HEIGHT + BOR
        self.SetBackgroundColour(self.options.clrbackground)
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntSymbol = ImageFont.truetype(common.common.symbols, 3 * self.FONT_SIZE / 2)
        self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
        self.signs = common.common.signs
        self.deg_symbol = '\xb0'
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Usr']

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
        BOR = UserWnd.BORDER
        x = BOR
        y = BOR
        if self.speculum == 0:
            self.drawplacidian(draw, x, y, tableclr)
        else:
            self.drawregiomontan(draw, x, y, tableclr)
        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)

    def drawplacidian(self, draw, x, y, clr):
        clrtxt = (0, 0, 0)
        if not self.bw:
            clrtxt = self.options.clrtexts
        txts = (mtexts.txtspositions['Longitude'], mtexts.txtspositions['Latitude'], mtexts.txtspositions['Rectascension'], mtexts.txtspositions['Declination'], mtexts.txtspositions['AscDiffLat'], mtexts.txtspositions['Semiarcus'], mtexts.txtspositions['Meridiandist'], mtexts.txtspositions['Horizondist'], mtexts.txtspositions['TemporalHour'], mtexts.txtspositions['HourlyDist'], mtexts.txtspositions['PMP'], mtexts.txtspositions['AscDiffPole'], mtexts.txtspositions['PoleHeight'], mtexts.txtspositions['AODO'])
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=clr)
        j = 0
        for i in range(len(self.options.speculums[self.speculum])):
            if not self.options.speculums[self.speculum][i]:
                continue
            wsp, hsp = draw.textsize(' ', self.fntText)
            w, h = draw.textsize(txts[i], self.fntText)
            draw.text((x + 2 * wsp, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - h) / 2), txts[i], fill=clrtxt, font=self.fntText)
            data = self.usr.speculums[self.speculum].speculum[i]
            d, m, s = util.decToDeg(data)
            if i == placspec.PlacidianSpeculum.LON:
                lon = self.usr.speculums[self.speculum].speculum[placspec.PlacidianSpeculum.LON]
                if self.options.ayanamsha != 0:
                    lon -= self.chart.ayanamsha
                    lon = util.normalize(lon)
                d, m, s = util.decToDeg(lon)
                sign = d / chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textsize(' ', self.fntText)
                wsg, hsg = draw.textsize(self.signs[sign], self.fntMorinus)
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offs = (self.CELL_WIDTH - w - wsp - wsg) / 2
                draw.text((x + self.CELL_WIDTH + offs, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - h) / 2), txt, fill=clrtxt, font=self.fntText)
                draw.text((x + self.CELL_WIDTH + offs + w + wsp, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - hsg) / 2), self.signs[sign], fill=clrtxt, font=self.fntMorinus)
            elif i == placspec.PlacidianSpeculum.LAT or i == placspec.PlacidianSpeculum.DECL or i == placspec.PlacidianSpeculum.ADLAT:
                sign = ''
                if data < 0.0:
                    sign = '-'
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offs = (self.CELL_WIDTH - w) / 2
                draw.text((x + self.CELL_WIDTH + offs, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - h) / 2), txt, fill=clrtxt, font=self.fntText)
            elif i == placspec.PlacidianSpeculum.RA or i == placspec.PlacidianSpeculum.PMP or i == placspec.PlacidianSpeculum.ADPH or i == placspec.PlacidianSpeculum.POH:
                txt = str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                if i == placspec.PlacidianSpeculum.RA:
                    if self.options.intime:
                        d, m, s = util.decToDeg(data / 15.0)
                        txt = str(d).rjust(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                    else:
                        txt = str(d).rjust(3) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offs = (self.CELL_WIDTH - w) / 2
                draw.text((x + self.CELL_WIDTH + offs, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - h) / 2), txt, fill=clrtxt, font=self.fntText)
            elif i == placspec.PlacidianSpeculum.SA or i == placspec.PlacidianSpeculum.MD or i == placspec.PlacidianSpeculum.HD or i == placspec.PlacidianSpeculum.TH or i == placspec.PlacidianSpeculum.HOD or i == placspec.PlacidianSpeculum.AODO:
                sign = ''
                if i == placspec.PlacidianSpeculum.SA or i == placspec.PlacidianSpeculum.TH or i == placspec.PlacidianSpeculum.HOD:
                    sign = 'D'
                    if data < 0.0:
                        sign = 'N'
                elif i == placspec.PlacidianSpeculum.MD:
                    sign = 'M'
                    if data < 0.0:
                        sign = 'I'
                elif i == placspec.PlacidianSpeculum.HD:
                    sign = 'A'
                    if data < 0.0:
                        sign = 'D'
                elif i == placspec.PlacidianSpeculum.AODO:
                    sign = 'A'
                    if data < 0.0:
                        sign = 'D'
                txt = sign + str(d).rjust(3) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offs = (self.CELL_WIDTH - w) / 2
                draw.text((x + self.CELL_WIDTH + offs, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - h) / 2), txt, fill=clrtxt, font=self.fntText)
            draw.line((x, y + (j + 1) * self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + (j + 1) * self.LINE_HEIGHT), fill=clr)
            j += 1

        draw.line((x, y, x, y + self.TABLE_HEIGHT), fill=clr)
        draw.line((x + self.CELL_WIDTH, y, x + self.CELL_WIDTH, y + self.TABLE_HEIGHT), fill=clr)
        draw.line((x + 2 * self.CELL_WIDTH, y, x + 2 * self.CELL_WIDTH, y + self.TABLE_HEIGHT), fill=clr)

    def drawregiomontan(self, draw, x, y, clr):
        clrtxt = (0, 0, 0)
        if not self.bw:
            clrtxt = self.options.clrtexts
        txts = (mtexts.txtspositions['Longitude'], mtexts.txtspositions['Latitude'], mtexts.txtspositions['Rectascension'], mtexts.txtspositions['Declination'], mtexts.txtspositions['Meridiandist'], mtexts.txtspositions['Horizondist'], mtexts.txtspositions['ZD'], mtexts.txtspositions['Pole'], mtexts.txtspositions['Q'], mtexts.txtspositions['WReg'], mtexts.txtspositions['CMP'])
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=clr)
        j = 0
        for i in range(len(self.options.speculums[self.speculum])):
            if not self.options.speculums[self.speculum][i]:
                continue
            wsp, hsp = draw.textsize(' ', self.fntText)
            w, h = draw.textsize(txts[i], self.fntText)
            draw.text((x + 2 * wsp, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - h) / 2), txts[i], fill=clrtxt, font=self.fntText)
            data = self.usr.speculums[self.speculum].speculum[i]
            d, m, s = util.decToDeg(data)
            if i == regiospec.RegiomontanianSpeculum.LON:
                lon = self.usr.speculums[self.speculum].speculum[regiospec.RegiomontanianSpeculum.LON]
                if self.options.ayanamsha != 0:
                    lon -= self.chart.ayanamsha
                    lon = util.normalize(lon)
                d, m, s = util.decToDeg(lon)
                sign = d / chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textsize(' ', self.fntText)
                wsg, hsg = draw.textsize(self.signs[sign], self.fntMorinus)
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offs = (self.CELL_WIDTH - w - wsp - wsg) / 2
                draw.text((x + self.CELL_WIDTH + offs, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - h) / 2), txt, fill=clrtxt, font=self.fntText)
                draw.text((x + self.CELL_WIDTH + offs + w + wsp, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - hsg) / 2), self.signs[sign], fill=clrtxt, font=self.fntMorinus)
            elif i == regiospec.RegiomontanianSpeculum.LAT or i == regiospec.RegiomontanianSpeculum.DECL or i == regiospec.RegiomontanianSpeculum.Q:
                sign = ''
                if data < 0.0:
                    sign = '-'
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offs = (self.CELL_WIDTH - w) / 2
                draw.text((x + self.CELL_WIDTH + offs, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - h) / 2), txt, fill=clrtxt, font=self.fntText)
            elif i == regiospec.RegiomontanianSpeculum.RA or i == regiospec.RegiomontanianSpeculum.ZD or i == regiospec.RegiomontanianSpeculum.POLE or i == regiospec.RegiomontanianSpeculum.W or i == regiospec.RegiomontanianSpeculum.CMP:
                sign = ''
                if i == regiospec.RegiomontanianSpeculum.ZD:
                    sign = 'Z'
                    if data < 0.0:
                        sign = 'N'
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                if i == regiospec.RegiomontanianSpeculum.RA:
                    if self.options.intime:
                        d, m, s = util.decToDeg(data / 15.0)
                        txt = str(d).rjust(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                    else:
                        txt = str(d).rjust(3) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offs = (self.CELL_WIDTH - w) / 2
                draw.text((x + self.CELL_WIDTH + offs, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - h) / 2), txt, fill=clrtxt, font=self.fntText)
            elif i == regiospec.RegiomontanianSpeculum.RMD or i == regiospec.RegiomontanianSpeculum.RHD:
                sign = ''
                if i == regiospec.RegiomontanianSpeculum.RMD:
                    sign = 'M'
                    if data < 0.0:
                        sign = 'I'
                else:
                    sign = 'A'
                    if data < 0.0:
                        sign = 'D'
                txt = sign + str(d).rjust(3) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offs = (self.CELL_WIDTH - w) / 2
                draw.text((x + self.CELL_WIDTH + offs, y + self.LINE_HEIGHT * j + (self.LINE_HEIGHT - h) / 2), txt, fill=clrtxt, font=self.fntText)
            draw.line((x, y + (j + 1) * self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + (j + 1) * self.LINE_HEIGHT), fill=clr)
            j += 1

        draw.line((x, y, x, y + self.TABLE_HEIGHT), fill=clr)
        draw.line((x + self.CELL_WIDTH, y, x + self.CELL_WIDTH, y + self.TABLE_HEIGHT), fill=clr)
        draw.line((x + 2 * self.CELL_WIDTH, y, x + 2 * self.CELL_WIDTH, y + self.TABLE_HEIGHT), fill=clr)