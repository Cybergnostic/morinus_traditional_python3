# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, houses, planets, chart, fortune, common, Image, ImageDraw, ImageFont, util, mtexts

class SquareChart:
    SMALL_SIZE = 400
    MEDIUM_SIZE = 600

    def __init__(self, chrt, size, opts, bw):
        self.chart = chrt
        self.options = opts
        self.w, self.h = size
        self.bw = bw
        self.buffer = wx.EmptyBitmap(self.w, self.h)
        self.bdc = wx.BufferedDC(None, self.buffer)
        self.chartsize = min(self.w, self.h)
        self.maxradius = self.chartsize / 2
        self.center = wx.Point(self.w / 2, self.h / 2)
        self.symbolSize = self.maxradius / 16
        self.smallSize = self.maxradius / 18
        self.fontSize = self.symbolSize
        self.fntMorinus = ImageFont.truetype(common.common.symbols, self.symbolSize)
        self.fntMorinusSmall = ImageFont.truetype(common.common.symbols, self.smallSize)
        self.fntText = ImageFont.truetype(common.common.abc, self.fontSize)
        self.fntTextSmall = ImageFont.truetype(common.common.abc, 3 * self.fontSize / 4)
        self.fntTextSmaller = ImageFont.truetype(common.common.abc, self.fontSize / 2)
        self.fntRetr = ImageFont.truetype(common.common.symbols, self.symbolSize / 2)
        self.deg_symbol = '\xb0'
        self.SPACE = self.fontSize / 5
        self.LINE_HEIGHT = self.SPACE + self.fontSize + self.SPACE
        self.ayans = {0: mtexts.txtsayanamsha['None'], 1: mtexts.txtsayanamsha['FaganBradley'], 2: mtexts.txtsayanamsha['Lahiri'], 3: mtexts.txtsayanamsha['Deluce'], 4: mtexts.txtsayanamsha['Raman'], 5: mtexts.txtsayanamsha['Ushashashi'], 6: mtexts.txtsayanamsha['Krishnamurti'], 7: mtexts.txtsayanamsha['DjwhalKhul'], 8: mtexts.txtsayanamsha['Yukteshwar'], 9: mtexts.txtsayanamsha['JNBhasin'], 10: mtexts.txtsayanamsha['BabylonianKuglerI2'], 11: mtexts.txtsayanamsha['BabylonianKuglerII2'], 12: mtexts.txtsayanamsha['BabylonianKuglerIII2'], 13: mtexts.txtsayanamsha['BabylonianHuber2'], 14: mtexts.txtsayanamsha['BabylonianMercier2'], 15: mtexts.txtsayanamsha['Aldebaran15Tau2'], 16: mtexts.txtsayanamsha['Hipparchos'], 17: mtexts.txtsayanamsha['Sassanian'], 18: mtexts.txtsayanamsha['GalacticCenter0Sag2'], 19: mtexts.txtsayanamsha['J2000'], 20: mtexts.txtsayanamsha['J1900'], 21: mtexts.txtsayanamsha['B1950']}
        self.hsystem = (
         mtexts.txtscommon['HSPlacidus'], mtexts.txtscommon['HSKoch'], mtexts.txtscommon['HSRegiomontanus'], mtexts.txtscommon['HSCampanus'], mtexts.txtscommon['HSEqual'], mtexts.txtscommon['HSWholeSign'], mtexts.txtscommon['HSAxial'], mtexts.txtscommon['HSMorinus'], mtexts.txtscommon['HSHorizontal'], mtexts.txtscommon['HSPagePolich'], mtexts.txtscommon['HSAlcabitus'], mtexts.txtscommon['HSPorphyrius'])
        return

    def drawChart(self):
        frameclr = (
         0, 0, 0)
        posclr = (0, 0, 0)
        txtclr = (0, 0, 0)
        bkgclr = (255, 255, 255)
        signsclr = (0, 0, 0)
        if not self.bw:
            bkgclr = self.options.clrbackground
            frameclr = self.options.clrframe
            txtclr = self.options.clrtexts
            signsclr = self.options.clrsigns
        self.bdc.SetBackground(wx.Brush(bkgclr))
        self.bdc.SetBrush(wx.Brush(bkgclr))
        self.bdc.Clear()
        self.bdc.BeginDrawing()
        cx, cy = self.center.Get()
        w = 4
        if self.chartsize <= SquareChart.SMALL_SIZE:
            w = 2
        elif self.chartsize <= SquareChart.MEDIUM_SIZE:
            w = 3
        pen = wx.Pen(frameclr, w)
        self.bdc.SetPen(pen)
        radius = self.maxradius * 0.9
        x = cx - radius
        y = cy - radius
        w = h = 2 * radius + w
        self.bdc.DrawRectangle(x, y, w, h)
        w = 3
        if self.chartsize <= SquareChart.SMALL_SIZE:
            w = 1
        else:
            if self.chartsize <= SquareChart.MEDIUM_SIZE:
                w = 2
        pen = wx.Pen(frameclr, w)
        self.bdc.SetPen(pen)
        x1 = cx
        y1 = cy - radius
        x2 = cx - radius
        y2 = cy
        self.bdc.DrawLine(x1, y1, x2, y2)
        x1 = cx - radius
        y1 = cy
        x2 = cx
        y2 = cy + radius
        self.bdc.DrawLine(x1, y1, x2, y2)
        x1 = cx
        y1 = cy + radius
        x2 = cx + radius
        y2 = cy
        self.bdc.DrawLine(x1, y1, x2, y2)
        x1 = cx + radius
        y1 = cy
        x2 = cx
        y2 = cy - radius
        self.bdc.DrawLine(x1, y1, x2, y2)
        x1 = cx - radius
        y1 = cy - radius
        x2 = cx - radius / 2
        y2 = cy - radius / 2
        self.bdc.DrawLine(x1, y1, x2, y2)
        x1 = cx - radius
        y1 = cy + radius
        x2 = cx - radius / 2
        y2 = cy + radius / 2
        self.bdc.DrawLine(x1, y1, x2, y2)
        x1 = cx + radius
        y1 = cy + radius
        x2 = cx + radius / 2
        y2 = cy + radius / 2
        self.bdc.DrawLine(x1, y1, x2, y2)
        x1 = cx + radius
        y1 = cy - radius
        x2 = cx + radius / 2
        y2 = cy - radius / 2
        self.bdc.DrawLine(x1, y1, x2, y2)
        x = cx - radius / 2
        y = cy - radius / 2
        w = h = radius + 1
        self.bdc.DrawRectangle(x, y, w, h)
        self.bdc.EndDrawing()
        wxImag = self.buffer.ConvertToImage()
        img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
        img.fromstring(wxImag.GetData())
        draw = ImageDraw.Draw(img)
        datetxt = str(self.chart.time.origyear) + '.' + mtexts.months[(self.chart.time.origmonth - 1)] + '.' + str(self.chart.time.origday).zfill(2)
        if self.chart.time.cal == chart.Time.JULIAN:
            datetxt += ' ' + mtexts.txtscommon['J']
        zonetxts = (mtexts.txtscommon['ZN'], mtexts.txtscommon['UT'], mtexts.txtscommon['LC'], mtexts.txtscommon['LC'])
        timetxt = str(self.chart.time.hour).zfill(2) + ':' + str(self.chart.time.minute).zfill(2) + ':' + str(self.chart.time.second).zfill(2) + ' ' + zonetxts[self.chart.time.zt]
        placetxt = self.chart.place.placename
        dirlontxt = mtexts.txtscommon['E']
        if not self.chart.place.east:
            dirlontxt = mtexts.txtscommon['W']
        dirlattxt = mtexts.txtscommon['N']
        if not self.chart.place.north:
            dirlattxt = mtexts.txtscommon['S']
        coordtxt = str(self.chart.place.deglon).zfill(2) + self.deg_symbol + str(self.chart.place.minlon).zfill(2) + "'" + dirlontxt + '  ' + str(self.chart.place.deglat).zfill(2) + self.deg_symbol + str(self.chart.place.minlat).zfill(2) + "'" + dirlattxt
        nametxt = self.chart.name
        typetxt = mtexts.typeList[self.chart.htype]
        hstxt = self.hsystem[self.options.hsys]
        ayantxt = mtexts.txtsayanamsha['Tropical']
        if self.options.ayanamsha != 0:
            ayantxt = self.ayans[self.options.ayanamsha]
        x = cx - radius / 3
        y = cy - radius / 3
        if self.chart.time.ph != None:
            y -= self.LINE_HEIGHT
        draw.text((x, y), datetxt, fill=txtclr, font=self.fntText)
        draw.text((x, y + self.LINE_HEIGHT), timetxt, fill=txtclr, font=self.fntText)
        draw.text((x, y + 2 * self.LINE_HEIGHT), placetxt, fill=txtclr, font=self.fntText)
        draw.text((x, y + 3 * self.LINE_HEIGHT), coordtxt, fill=txtclr, font=self.fntText)
        draw.text((x, y + 4 * self.LINE_HEIGHT), nametxt, fill=txtclr, font=self.fntText)
        draw.text((x, y + 5 * self.LINE_HEIGHT), typetxt, fill=txtclr, font=self.fntText)
        draw.text((x, y + 6 * self.LINE_HEIGHT), ayantxt, fill=txtclr, font=self.fntText)
        draw.text((x, y + 7 * self.LINE_HEIGHT), hstxt, fill=txtclr, font=self.fntText)
        ar = (
         6, 2, 5, 1, 4, 0, 3)
        draw.text((x, y + 8 * self.LINE_HEIGHT), common.common.planets[ar[self.chart.time.ph.weekday]], fill=txtclr, font=self.fntMorinus)
        wsym, hsym = draw.textsize(common.common.planets[ar[self.chart.time.ph.weekday]], self.fntMorinus)
        wsp, hsp = draw.textsize(' ', self.fntText)
        draw.text((x + wsym + wsp, y + 8 * self.LINE_HEIGHT), mtexts.txtscommon['Day'], fill=txtclr, font=self.fntText)
        wday, hday = draw.textsize(mtexts.txtscommon['Day'], self.fntText)
        draw.text((x + wsym + wsp + wday + 2 * wsp, y + 8 * self.LINE_HEIGHT), common.common.planets[self.chart.time.ph.planetaryhour], fill=txtclr, font=self.fntMorinus)
        wsym2, hsym2 = draw.textsize(common.common.planets[self.chart.time.ph.planetaryhour], self.fntMorinus)
        draw.text((x + wsym + wsp + wday + wsp + wsym2 + 2 * wsp, y + 8 * self.LINE_HEIGHT), mtexts.txtscommon['Hour'], fill=txtclr, font=self.fntText)
        ar = (
         (
          (
           cx - 3 * radius / 4 - 3 * self.fontSize / 2, cy - radius / 3 + self.fontSize), (cx - 3 * radius / 4 - self.fontSize / 2, cy - radius / 3), (cx - 3 * radius / 4 + self.fontSize / 2, cy - radius / 3 - self.fontSize / 2)), ((cx - 3 * radius / 4 - self.fontSize, cy + radius / 3 - 3 * self.fontSize), (cx - 3 * radius / 4, cy + radius / 3 - 2 * self.fontSize - self.fontSize / 4), (cx - 3 * radius / 4 + self.fontSize, cy + radius / 3 - self.fontSize)), ((cx - 3 * radius / 4 - 5 * self.fontSize / 2, cy + 3 * radius / 4 + 4 * self.fontSize / 5), (cx - 3 * radius / 4 - 3 * self.fontSize / 2, cy + 3 * radius / 4 - self.fontSize / 5), (cx - 3 * radius / 4 - self.fontSize / 2, cy + 3 * radius / 4 - 4 * self.fontSize / 5)), ((cx - radius / 4 - 2 * self.fontSize, cy + 3 * radius / 4 - self.fontSize), (cx - radius / 4 - self.fontSize, cy + 3 * radius / 4 - self.fontSize / 4), (cx - radius / 4, cy + 3 * radius / 4 + self.fontSize)), ((cx + radius / 4 - 5 * self.fontSize / 2, cy + 3 * radius / 4 + 4 * self.fontSize / 5), (cx + radius / 4 - 3 * self.fontSize / 2, cy + 3 * radius / 4 - self.fontSize / 5), (cx + radius / 4 - self.fontSize / 2, cy + 3 * radius / 4 - 4 * self.fontSize / 5)), ((cx + 3 * radius / 4 - 2 * self.fontSize, cy + 3 * radius / 4 - self.fontSize), (cx + 3 * radius / 4 - self.fontSize, cy + 3 * radius / 4 - self.fontSize / 4), (cx + 3 * radius / 4, cy + 3 * radius / 4 + self.fontSize)), ((cx + 3 * radius / 4 - 3 * self.fontSize / 4, cy + radius / 3 - self.fontSize / 2), (cx + 3 * radius / 4 + self.fontSize / 4, cy + radius / 3 - 3 * self.fontSize / 2), (cx + 3 * radius / 4 + 5 * self.fontSize / 4, cy + radius / 3 - 9 * self.fontSize / 4)), ((cx + 3 * radius / 4 - 3 * self.fontSize / 2, cy - radius / 3 + self.fontSize), (cx + 3 * radius / 4 - self.fontSize / 4, cy - radius / 3 + 7 * self.fontSize / 4), (cx + 3 * radius / 4 + 3 * self.fontSize / 4, cy - radius / 3 + 11 * self.fontSize / 4)), ((cx + 3 * radius / 4 - self.fontSize, cy - 3 * radius / 4 + self.fontSize), (cx + 3 * radius / 4, cy - 3 * radius / 4), (cx + 3 * radius / 4 + self.fontSize, cy - 3 * radius / 4 - 3 * self.fontSize / 4)), ((cx + radius / 4 - self.fontSize / 4, cy - 3 * radius / 4 - self.fontSize), (cx + radius / 4 + 3 * self.fontSize / 4, cy - 3 * radius / 4 - self.fontSize / 4), (cx + radius / 4 + 7 * self.fontSize / 4, cy - 3 * radius / 4 + self.fontSize)), ((cx - radius / 4 - self.fontSize, cy - 3 * radius / 4 + self.fontSize), (cx - radius / 4, cy - 3 * radius / 4), (cx - radius / 4 + self.fontSize, cy - 3 * radius / 4 - 3 * self.fontSize / 4)), ((cx - 3 * radius / 4, cy - 3 * radius / 4 - self.fontSize), (cx - 3 * radius / 4 + self.fontSize, cy - 3 * radius / 4), (cx - 3 * radius / 4 + 2 * self.fontSize, cy - 3 * radius / 4 + 5 * self.fontSize / 4)))
        arpl = (
         (
          cx - 3 * radius / 4 - 3 * self.fontSize / 4, cy - self.fontSize / 2), (cx - radius + self.fontSize / 2, cy + radius / 2 - self.fontSize / 2), (cx - 3 * radius / 4 + self.fontSize, cy + 3 * radius / 4 + self.fontSize), (cx - radius / 5 + self.fontSize, cy + radius / 2 + 2 * self.fontSize), (cx + radius / 2 - 5 * self.fontSize / 2, cy + 3 * radius / 4 + self.fontSize), (cx + 2 * radius / 3 + self.fontSize / 2, cy + radius / 2 - self.fontSize / 2), (cx + radius / 2 + self.fontSize / 2, cy - self.fontSize / 2), (cx + 2 * radius / 3 + self.fontSize / 2, cy - radius / 2 - self.fontSize / 2), (cx + radius / 2 - 2 * self.fontSize, cy - radius + 2 * self.fontSize), (cx - radius / 6 + self.fontSize, cy - 3 * radius / 4 + self.fontSize / 2), (cx - 3 * radius / 4 + 2 * self.fontSize, cy - radius + 2 * self.fontSize), (cx - radius + self.fontSize / 2, cy - radius / 2 - self.fontSize / 2))
        lh = self.fontSize
        lhoffs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(houses.Houses.HOUSE_NUM):
            lon = self.chart.houses.cusps[(i + 1)]
            if self.options.ayanamsha != 0 and self.options.hsys != 5:
                lon -= self.chart.ayanamsha
                lon = util.normalize(lon)
            d, m, s = util.decToDeg(lon)
            sign = d / chart.Chart.SIGN_DEG
            pos = d % chart.Chart.SIGN_DEG
            txt = str(pos).rjust(2) + self.deg_symbol
            draw.text((ar[i][0][0], ar[i][0][1]), txt, fill=(0, 0, 0), font=self.fntTextSmall)
            draw.text((ar[i][1][0], ar[i][1][1]), common.common.signs[sign], fill=signsclr, font=self.fntMorinusSmall)
            txt = str(m).zfill(2) + "'"
            draw.text((ar[i][2][0], ar[i][2][1]), txt, fill=(0, 0, 0), font=self.fntTextSmaller)
            order, mixed = self.getPlanetsInHouse(i)
            num = len(order)
            if num > 1 and num % 2 == 0:
                lhoffs[i] -= lh / 2
            if num > 2:
                shift = num
                if shift % 2 == 0:
                    shift -= 1
                lhoffs[i] -= int(shift / 2) * lh
            for j in range(num):
                idxpl = mixed[j]
                lon = order[j]
                if self.options.ayanamsha != 0:
                    lon -= self.chart.ayanamsha
                    lon = util.normalize(lon)
                d, m, s = util.decToDeg(lon)
                x, y = (
                 arpl[i][0], arpl[i][1])
                pl = ''
                if idxpl < planets.Planets.BODIES_NUM:
                    pl = common.common.planets[idxpl]
                else:
                    pl = common.common.fortune
                wpl, hpl = draw.textsize('F', self.fntMorinusSmall)
                wpl2, hpl2 = draw.textsize(pl, self.fntMorinusSmall)
                clrpl = (
                 0, 0, 0)
                if not self.bw:
                    idxobj = idxpl
                    if idxobj >= planets.Planets.BODIES_NUM - 1:
                        idxobj -= 1
                    if idxobj < planets.Planets.BODIES_NUM - 1:
                        clrpl = self.options.clrplanets[idxobj]
                    else:
                        clrpl = self.options.clrLoF
                draw.text((x, y + lhoffs[i]), pl, fill=clrpl, font=self.fntMorinusSmall)
                wr, hr = draw.textsize('R', self.fntTextSmaller)
                wsp, hsp = draw.textsize(' ', self.fntTextSmall)
                if idxpl < planets.Planets.PLANETS_NUM:
                    speed = self.chart.planets.planets[idxpl].data[planets.Planet.SPLON]
                    if speed <= 0.0:
                        t = common.common.retr
                        fnt = self.fntRetr
                        if speed == 0.0:
                            t = 'S'
                            fnt = self.fntTextSmaller
                        draw.text((x + wpl2, y + lhoffs[i] + self.fontSize / 2), t, fill=clrpl, font=fnt)
                sign = d / chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                txtdeg = str(pos).zfill(2) + self.deg_symbol
                txtmin = str(m).zfill(2) + "'"
                wdeg, hdeg = draw.textsize(txtdeg, self.fntTextSmall)
                wsg, hsg = draw.textsize(common.common.signs[sign], self.fntMorinusSmall)
                wmin, hmin = draw.textsize(txtmin, self.fntTextSmaller)
                draw.text((x + wpl + wr + wsp, y + lhoffs[i]), txtdeg, fill=clrpl, font=self.fntTextSmall)
                draw.text((x + wpl + wr + wsp + wdeg, y + lhoffs[i]), common.common.signs[sign], fill=clrpl, font=self.fntMorinusSmall)
                draw.text((x + wpl + wr + wsp + wdeg + wsp + wsg, y + lhoffs[i]), txtmin, fill=clrpl, font=self.fntTextSmaller)
                lhoffs[i] += lh

        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)
        return self.buffer

    def getPlanetsInHouse(self, hnum):
        inhouse = []
        mixed = []
        for i in range(planets.Planets.BODIES_NUM):
            lon = self.chart.planets.planets[i].data[planets.Planet.LON]
            if self.options.ayanamsha != 0 and self.options.hsys == 5:
                lon -= self.chart.ayanamsha
                lon = util.normalize(lon)
            num = self.chart.houses.getHousePos(lon, self.options)
            if self.options.ayanamsha != 0 and self.options.hsys == 5:
                lon += self.chart.ayanamsha
                lon = util.normalize(lon)
            if num == hnum:
                inhouse.append(lon)
                mixed.append(i)

        lon = self.chart.fortune.fortune[fortune.Fortune.LON]
        if self.options.ayanamsha != 0 and self.options.hsys != 5:
            lon += self.chart.ayanamsha
            lon = util.normalize(lon)
        num = self.chart.houses.getHousePos(lon, self.options)
        if self.options.ayanamsha != 0 and self.options.hsys == 5:
            lon += self.chart.ayanamsha
            lon = util.normalize(lon)
        if num == hnum:
            addendum = 0.0
            if self.options.lotsusehouses:
                addendum = 15.0
            inhouse.append(lon + addendum)
            mixed.append(planets.Planets.BODIES_NUM)
        num = len(inhouse)
        for j in range(num):
            for i in range(num - 1):
                if inhouse[i] > inhouse[(i + 1)]:
                    tmp = inhouse[i]
                    inhouse[i] = inhouse[(i + 1)]
                    inhouse[i + 1] = tmp
                    tmp = mixed[i]
                    mixed[i] = mixed[(i + 1)]
                    mixed[i + 1] = tmp

        if hnum >= 5 and hnum <= 10:
            inhouse.reverse()
            mixed.reverse()
        return (tuple(inhouse), tuple(mixed))