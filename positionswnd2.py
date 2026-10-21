# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import os
import chart
import houses
import planets
import primdirs
import placspec
import regiospec
import common
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import util
import mtexts

class PositionsWnd2(wx.Window):
    BORDER = 20

    def __init__(self, parent, chrt, options, mainfr, id=-1, size=wx.DefaultSize):
        wx.Window.__init__(self, parent, id, wx.DefaultPosition, size=size, style=wx.SUNKEN_BORDER)
        self.parent = parent
        self.chart = chrt
        self.options = options
        self.mainfr = mainfr
        self.bw = self.options.bw
        self.parent.mbw.Check(self.bw)
        self.speculum = 0
        if self.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
            self.speculum = 1
        column_num = 0
        for i in range(len(self.options.speculums[self.speculum])):
            if self.options.speculums[self.speculum][i] == True:
                column_num += 1

        BOR = PositionsWnd2.BORDER
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.COLUMN_NUM = column_num
        self.SPACE = self.FONT_SIZE // 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        self.SMALL_CELL_WIDTH = 3 * self.FONT_SIZE
        self.CELL_WIDTH = 8 * self.FONT_SIZE
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TITLE_WIDTH = self.COLUMN_NUM * self.CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.SPACE_ASCPLANETSY = self.LINE_HEIGHT
        self.SPACE_PLANETSHCSY = self.LINE_HEIGHT
        self.LINE_NUM = 16
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.LINE_NUM * self.LINE_HEIGHT + self.SPACE_TITLEY + self.SPACE_ASCPLANETSY + self.SPACE_PLANETSHCSY
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.RETRYOFFS = 3 * self.FONT_SIZE // 5
        self.WIDTH = BOR + self.TABLE_WIDTH + BOR
        self.HEIGHT = BOR + self.TABLE_HEIGHT + BOR
        self.SetBackgroundColour(self.options.clrbackground)
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = util.truetype(common.common.symbols, self.FONT_SIZE)
        self.fntMorinusRetr = util.truetype(common.common.symbols, self.FONT_SIZE * 3 // 4)
        self.fntSymbol = util.truetype(common.common.symbols, 3 * self.FONT_SIZE // 2)
        self.fntText = util.truetype(common.common.abc, self.FONT_SIZE)
        self.fntRText = util.truetype(common.common.abc, self.FONT_SIZE * 3 // 4)
        self.signs = common.common.signs
        self.deg_symbol = '\xb0'
        self.drawBkg()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)

    def onPopupMenu(self, event):
        self.parent.onPopupMenu(event)

    def onSaveAsBitmap(self, event):
        name = self.chart.name + mtexts.txtsabbrevs['Pos']
        dlg = wx.FileDialog(self, mtexts.txtsfiles['SaveAsBmp'], '', name, mtexts.txtsfiles['BMPFiles'], wx.FD_SAVE)
        if os.path.isdir(self.mainfr.fpathimgs):
            dlg.SetDirectory(self.mainfr.fpathimgs)
        else:
            dlg.SetDirectory('.')
        if dlg.ShowModal() == wx.ID_OK:
            dpath = dlg.GetDirectory()
            fpath = dlg.GetPath()
            if not fpath.endswith('.png'):
                fpath += '.png'
            if os.path.isfile(fpath):
                dlgm = wx.MessageDialog(self, mtexts.txtsfiles['FileExists'], mtexts.txtsfiles['Message'], wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                if dlgm.ShowModal() == wx.ID_NO:
                    dlgm.Destroy()
                    dlg.Destroy()
                    return
                dlgm.Destroy()
            self.mainfr.fpathimgs = dpath
            self.buffer.SaveFile(fpath, wx.BITMAP_TYPE_PNG)
        dlg.Destroy()

    def onBlackAndWhite(self, event):
        if self.bw != event.IsChecked():
            self.bw = event.IsChecked()
            self.drawBkg()
            self.Refresh()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

    def drawBkg(self):
        if self.bw:
            self.bkgclr = (
             255, 255, 255)
        else:
            self.bkgclr = self.options.clrbackground
        self.SetBackgroundColour(self.bkgclr)
        tableclr = self.options.clrtable
        if self.bw:
            tableclr = (
             0, 0, 0)
        img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
        draw = ImageDraw.Draw(img)
        BOR = PositionsWnd2.BORDER
        txtclr = (
         0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        draw.rectangle(((BOR + self.SMALL_CELL_WIDTH, BOR), (BOR + self.SMALL_CELL_WIDTH + self.TITLE_WIDTH, BOR + self.TITLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
        txt = ((mtexts.txtspositions['Longitude'], mtexts.txtspositions['Latitude'], mtexts.txtspositions['Rectascension'], mtexts.txtspositions['Declination'], mtexts.txtspositions['AscDiffLat'], mtexts.txtspositions['Semiarcus'], mtexts.txtspositions['Meridiandist'], mtexts.txtspositions['Horizondist'], mtexts.txtspositions['TemporalHour'], mtexts.txtspositions['HourlyDist'], mtexts.txtspositions['PMP'], mtexts.txtspositions['AscDiffPole'], mtexts.txtspositions['PoleHeight'], mtexts.txtspositions['AODO']), (mtexts.txtspositions['Longitude'], mtexts.txtspositions['Latitude'], mtexts.txtspositions['Rectascension'], mtexts.txtspositions['Declination'], mtexts.txtspositions['Meridiandist'], mtexts.txtspositions['Horizondist'], mtexts.txtspositions['ZD'], mtexts.txtspositions['Pole'], mtexts.txtspositions['Q'], mtexts.txtspositions['WReg'], mtexts.txtspositions['CMP']))
        j = 0
        for i in range(len(txt[self.speculum])):
            if self.options.speculums[self.speculum][i]:
                w, h = draw.textbbox((0, 0), txt[self.speculum][i], self.fntText)[2:]
                draw.text((BOR + self.SMALL_CELL_WIDTH + self.CELL_WIDTH * j + (self.CELL_WIDTH - w) // 2, BOR + (self.LINE_HEIGHT - h) // 2), txt[self.speculum][i], fill=txtclr, font=self.fntText)
                j += 1

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        txts = (
         '0', '1')
        lons = [self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON], self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]]
        if self.options.ayanamsha != 0:
            for i in range(len(txts)):
                lons[i] -= self.chart.ayanamsha
                lons[i] = util.normalize(lons[i])

        data = (
         (
          lons[0], self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LAT], self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.RA], self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.DECL]), (lons[1], self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LAT], self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.RA], self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.DECL]))
        for i in range(len(txts)):
            self.drawanglesline(draw, x, y + i * self.LINE_HEIGHT, tableclr, txts[i], data[i], True)

        y = y + len(txts) * self.LINE_HEIGHT + self.SPACE_ASCPLANETSY
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        lons = []
        for i in range(planets.Planets.BODIES_NUM - 1):
            lons.append(self.chart.planets.planets[i].data[planets.Planet.LON])

        if self.options.ayanamsha != 0:
            for i in range(len(lons)):
                lons[i] -= self.chart.ayanamsha
                lons[i] = util.normalize(lons[i])

        j = 0
        for i in range(planets.Planets.BODIES_NUM - 1):
            if self.speculum == 0:
                self.drawplacidianline(draw, x, y + j * self.LINE_HEIGHT, tableclr, common.common.planets[i], self.chart.planets.planets[i].speculums[self.speculum].speculum, lons[j], i, self.chart.planets.planets[i].data[planets.Planet.SPLON])
            else:
                self.drawregiomontanline(draw, x, y + j * self.LINE_HEIGHT, tableclr, common.common.planets[i], self.chart.planets.planets[i].speculums[self.speculum].speculum, lons[j], i, self.chart.planets.planets[i].data[planets.Planet.SPLON])
            j += 1

        hidx = (
         1, 2, 3, 10, 11, 12)
        lons = [self.chart.houses.cusps[hidx[0]], self.chart.houses.cusps[hidx[1]], self.chart.houses.cusps[hidx[2]], self.chart.houses.cusps[hidx[3]], self.chart.houses.cusps[hidx[4]], self.chart.houses.cusps[hidx[5]]]
        if self.options.ayanamsha != 0 and self.options.hsys != 5:
            for i in range(len(hidx)):
                lons[i] -= self.chart.ayanamsha
                lons[i] = util.normalize(lons[i])

        data = (
         (
          lons[0], 0.0, self.chart.houses.cusps2[(hidx[0] - 1)][0], self.chart.houses.cusps2[(hidx[0] - 1)][1]),
         (
          lons[1], 0.0, self.chart.houses.cusps2[(hidx[1] - 1)][0], self.chart.houses.cusps2[(hidx[1] - 1)][1]),
         (
          lons[2], 0.0, self.chart.houses.cusps2[(hidx[2] - 1)][0], self.chart.houses.cusps2[(hidx[2] - 1)][1]),
         (
          lons[3], 0.0, self.chart.houses.cusps2[(hidx[3] - 1)][0], self.chart.houses.cusps2[(hidx[3] - 1)][1]),
         (
          lons[4], 0.0, self.chart.houses.cusps2[(hidx[4] - 1)][0], self.chart.houses.cusps2[(hidx[4] - 1)][1]),
         (
          lons[5], 0.0, self.chart.houses.cusps2[(hidx[5] - 1)][0], self.chart.houses.cusps2[(hidx[5] - 1)][1]))
        y = y + (planets.Planets.BODIES_NUM - 1) * self.LINE_HEIGHT + self.SPACE_PLANETSHCSY
        draw.line((x, y, x + self.TABLE_WIDTH, y), fill=tableclr)
        for i in range(len(hidx)):
            self.drawanglesline(draw, x, y + i * self.LINE_HEIGHT, tableclr, common.common.housenames2[(hidx[i] - 1)], data[i])

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)

    def drawanglesline(self, draw, x, y, clr, txt, data, AscMC=False):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        SPEC = 2
        j = 0
        summa = 0
        for i in range(len(self.options.speculums[self.speculum]) + 1 + 1):
            if i >= SPEC and not self.options.speculums[self.speculum][(i - SPEC)]:
                continue
            draw.line((x + summa + offs[j], y, x + summa + offs[j], y + self.LINE_HEIGHT), fill=clr)
            j += 1
            summa += offs[i]

        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        fnt = self.fntSymbol
        if not AscMC:
            fnt = self.fntText
        w, h = draw.textbbox((0, 0), txt, fnt)[2:]
        offset = (self.SMALL_CELL_WIDTH - w) // 2
        draw.text((x + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=fnt)
        offs = (
         self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        j = 0
        summa = 0
        for i in range(placspec.PlacidianSpeculum.DECL + 1):
            if not self.options.speculums[self.speculum][i]:
                continue
            d, m, s = util.decToDeg(data[i])
            if i == placspec.PlacidianSpeculum.LON:
                sign = d // chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textbbox((0, 0), ' ', self.fntText)[2:]
                wsg, hsg = draw.textbbox((0, 0), self.signs[sign], self.fntMorinus)[2:]
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - (w + wsp + wsg)) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset + w + wsp, y + (self.LINE_HEIGHT - hsg) // 2), self.signs[sign], fill=txtclr, font=self.fntMorinus)
            elif i == placspec.PlacidianSpeculum.LAT or i == placspec.PlacidianSpeculum.DECL:
                sign = ''
                if data[i] < 0.0:
                    sign = '-'
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - w) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
            elif i == placspec.PlacidianSpeculum.RA:
                txt = str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                if self.options.intime:
                    d, m, s = util.decToDeg(data[i] / 15.0)
                    txt = str(d).rjust(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                else:
                    txt = str(d).rjust(3) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - w) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=txtclr, font=self.fntText)
            j += 1
            summa += offs[i]

    def drawplacidianline(self, draw, x, y, clr, txt, data, ayanlon, idxpl=0, speed=0.0):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        SPEC = 2
        j = 0
        summa = 0
        for i in range(len(self.options.speculums[self.speculum]) + 1 + 1):
            if i >= SPEC and not self.options.speculums[self.speculum][(i - SPEC)]:
                continue
            draw.line((x + summa + offs[j], y, x + summa + offs[j], y + self.LINE_HEIGHT), fill=clr)
            j += 1
            summa += offs[i]

        clrpl = (0, 0, 0)
        if not self.bw:
            clrpl = self.options.clrplanets[idxpl]
        fnt = self.fntMorinus
        w, h = draw.textbbox((0, 0), txt, fnt)[2:]
        offset = (self.SMALL_CELL_WIDTH - w) // 2
        draw.text((x + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clrpl, font=fnt)
        if speed <= 0.0:
            t = common.common.retr
            fnt = self.fntMorinusRetr
            if speed == 0.0:
                t = 'S'
                fnt = self.fntRText
            draw.text((x + offset + w, y + (self.LINE_HEIGHT - h) // 2 + self.RETRYOFFS), t, fill=clrpl, font=fnt)
        offs = (
         self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        j = 0
        summa = 0
        for i in range(len(self.options.speculums[self.speculum])):
            if not self.options.speculums[self.speculum][i]:
                continue
            d, m, s = util.decToDeg(data[i])
            if i == placspec.PlacidianSpeculum.LON:
                if self.options.ayanamsha != 0:
                    d, m, s = util.decToDeg(ayanlon)
                sign = d // chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textbbox((0, 0), ' ', self.fntText)[2:]
                wsg, hsg = draw.textbbox((0, 0), self.signs[sign], self.fntMorinus)[2:]
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - (w + wsp + wsg)) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clrpl, font=self.fntText)
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset + w + wsp, y + (self.LINE_HEIGHT - hsg) // 2), self.signs[sign], fill=clrpl, font=self.fntMorinus)
            elif i == placspec.PlacidianSpeculum.LAT or i == placspec.PlacidianSpeculum.DECL or i == placspec.PlacidianSpeculum.ADLAT:
                sign = ''
                if data[i] < 0.0:
                    sign = '-'
                if i == placspec.PlacidianSpeculum.LAT and idxpl == planets.Planets.SUN:
                    d, m, s = (0, 0, 0)
                    sign = ''
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - w) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clrpl, font=self.fntText)
            elif i == placspec.PlacidianSpeculum.RA or i == placspec.PlacidianSpeculum.PMP or i == placspec.PlacidianSpeculum.ADPH or i == placspec.PlacidianSpeculum.POH:
                txt = str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                if i == placspec.PlacidianSpeculum.RA:
                    if self.options.intime:
                        d, m, s = util.decToDeg(data[i] / 15.0)
                        txt = str(d).rjust(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                    else:
                        txt = str(d).rjust(3) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - w) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clrpl, font=self.fntText)
            elif i == placspec.PlacidianSpeculum.SA or i == placspec.PlacidianSpeculum.MD or i == placspec.PlacidianSpeculum.HD or i == placspec.PlacidianSpeculum.TH or i == placspec.PlacidianSpeculum.HOD or i == placspec.PlacidianSpeculum.AODO:
                sign = ''
                if i == placspec.PlacidianSpeculum.SA or i == placspec.PlacidianSpeculum.TH or i == placspec.PlacidianSpeculum.HOD:
                    sign = 'D'
                    if data[i] < 0.0:
                        sign = 'N'
                elif i == placspec.PlacidianSpeculum.MD:
                    sign = 'M'
                    if data[i] < 0.0:
                        sign = 'I'
                elif i == placspec.PlacidianSpeculum.HD:
                    sign = 'A'
                    if data[i] < 0.0:
                        sign = 'D'
                elif i == placspec.PlacidianSpeculum.AODO:
                    sign = 'A'
                    if data[i] < 0.0:
                        sign = 'D'
                txt = sign + str(d).rjust(3) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - w) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clrpl, font=self.fntText)
            j += 1
            summa += offs[i]

    def drawregiomontanline(self, draw, x, y, clr, txt, data, ayanlon, idxpl=0, speed=0.0):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        SPEC = 2
        j = 0
        summa = 0
        for i in range(len(self.options.speculums[self.speculum]) + 1 + 1):
            if i >= SPEC and not self.options.speculums[self.speculum][(i - SPEC)]:
                continue
            draw.line((x + summa + offs[j], y, x + summa + offs[j], y + self.LINE_HEIGHT), fill=clr)
            j += 1
            summa += offs[i]

        clrpl = (0, 0, 0)
        if not self.bw:
            clrpl = self.options.clrplanets[idxpl]
        fnt = self.fntMorinus
        w, h = draw.textbbox((0, 0), txt, fnt)[2:]
        offset = (self.SMALL_CELL_WIDTH - w) // 2
        draw.text((x + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clrpl, font=fnt)
        if speed <= 0.0:
            t = 'R'
            if speed == 0.0:
                t = 'S'
            draw.text((x + offset + w, y + (self.LINE_HEIGHT - h) // 2 + self.RETRYOFFS), t, fill=clrpl, font=self.fntRText)
        offs = (
         self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        j = 0
        summa = 0
        for i in range(len(self.options.speculums[self.speculum])):
            if not self.options.speculums[self.speculum][i]:
                continue
            d, m, s = util.decToDeg(data[i])
            if i == regiospec.RegiomontanianSpeculum.LON:
                sign = d // chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textbbox((0, 0), ' ', self.fntText)[2:]
                wsg, hsg = draw.textbbox((0, 0), self.signs[sign], self.fntMorinus)[2:]
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - (w + wsp + wsg)) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clrpl, font=self.fntText)
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset + w + wsp, y + (self.LINE_HEIGHT - hsg) // 2), self.signs[sign], fill=clrpl, font=self.fntMorinus)
            elif i == regiospec.RegiomontanianSpeculum.LAT or i == regiospec.RegiomontanianSpeculum.DECL or i == regiospec.RegiomontanianSpeculum.Q:
                sign = ''
                if data[i] < 0.0:
                    sign = '-'
                if i == regiospec.RegiomontanianSpeculum.LAT and idxpl == planets.Planets.SUN:
                    d, m, s = (0, 0, 0)
                    sign = ''
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - w) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clrpl, font=self.fntText)
            elif i == regiospec.RegiomontanianSpeculum.RA or i == regiospec.RegiomontanianSpeculum.ZD or i == regiospec.RegiomontanianSpeculum.POLE or i == regiospec.RegiomontanianSpeculum.W or i == regiospec.RegiomontanianSpeculum.CMP:
                sign = ''
                if i == regiospec.RegiomontanianSpeculum.ZD:
                    sign = 'Z'
                    if data[i] < 0.0:
                        sign = 'N'
                txt = sign + str(d).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                if i == regiospec.RegiomontanianSpeculum.RA:
                    if self.options.intime:
                        d, m, s = util.decToDeg(data[i] / 15.0)
                        txt = str(d).rjust(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
                    else:
                        txt = str(d).rjust(3) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - w) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clrpl, font=self.fntText)
            elif i == regiospec.RegiomontanianSpeculum.RMD or i == regiospec.RegiomontanianSpeculum.RHD:
                sign = ''
                if i == regiospec.RegiomontanianSpeculum.RMD:
                    sign = 'M'
                    if data[i] < 0.0:
                        sign = 'I'
                else:
                    sign = 'A'
                    if data[i] < 0.0:
                        sign = 'D'
                txt = sign + str(d).rjust(3) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textbbox((0, 0), txt, self.fntText)[2:]
                offset = (offs[i] - w) // 2
                draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt, fill=clrpl, font=self.fntText)
            j += 1
            summa += offs[i]