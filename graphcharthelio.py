# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import math, wx, Image, ImageDraw, ImageFont, chart, planets, options, common, util, mtexts

class GraphChartHelio:
    DEG30 = math.pi / 6
    SMALL_SIZE = 400
    MEDIUM_SIZE = 600

    def __init__(self, chrt, size, opts, bw):
        self.w, self.h = size
        self.chart = chrt
        self.options = opts
        self.bw = bw
        self.buffer = wx.EmptyBitmap(self.w, self.h)
        self.bdc = wx.BufferedDC(None, self.buffer)
        self.chartsize = min(self.w, self.h)
        self.maxradius = self.chartsize / 2
        self.center = wx.Point(size[0] / 2, size[1] / 2)
        self.symbolSize = self.maxradius / 12
        self.signSize = self.maxradius / 12
        signsectorlen = 0.16
        self.r30 = self.maxradius * 0.96
        self.signoffs = (signsectorlen / 2.0 - 0.01) * self.maxradius
        self.rSign = self.r30 - self.signoffs
        self.r0 = self.r30 - signsectorlen * self.maxradius
        self.rMercury = self.maxradius * 0.1
        self.rVenus = self.maxradius * 0.2
        self.rEarth = self.maxradius * 0.3
        self.rMars = self.maxradius * 0.43
        self.rJupiter = self.maxradius * 0.6
        self.rSaturn = self.maxradius * 0.75
        self.rads = (self.rSaturn, self.rJupiter, self.rMars, self.rEarth, self.rVenus, self.rMercury)
        self.fntMorinus = ImageFont.truetype(common.common.symbols, self.symbolSize)
        self.fntMorinusSigns = ImageFont.truetype(common.common.symbols, self.signSize)
        return

    def drawChart(self):
        self.drawCircles()
        wxImag = self.buffer.ConvertToImage()
        self.img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
        self.img.fromstring(wxImag.GetData())
        self.draw = ImageDraw.Draw(self.img)
        self.drawSigns()
        self.drawSymbols()
        wxImg = wx.EmptyImage(self.img.size[0], self.img.size[1])
        wxImg.SetData(self.img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)
        return self.buffer

    def drawCircles(self):
        bkgclr = self.options.clrbackground
        if self.bw:
            bkgclr = (255, 255, 255)
        self.bdc.SetBackground(wx.Brush(bkgclr))
        self.bdc.Clear()
        self.bdc.BeginDrawing()
        self.bdc.SetBrush(wx.Brush(bkgclr))
        cx, cy = self.center.Get()
        clr = self.options.clrframe
        if self.bw:
            clr = (0, 0, 0)
        pen = wx.Pen(clr, 1)
        self.bdc.SetPen(pen)
        self.bdc.DrawCircle(cx, cy, self.r30)
        clr = self.options.clrframe
        if self.bw:
            clr = (0, 0, 0)
        w = 3
        if self.chartsize <= GraphChartHelio.SMALL_SIZE:
            w = 1
        elif self.chartsize <= GraphChartHelio.MEDIUM_SIZE:
            w = 2
        pen = wx.Pen(clr, w)
        self.bdc.SetPen(pen)
        self.bdc.DrawCircle(cx, cy, self.r0)
        lon = 0.0
        if self.options.ayanamsha != 0:
            lon -= self.chart.ayanamsha
            lon = util.normalize(lon)
        clr = self.options.clrframe
        if self.bw:
            clr = (0, 0, 0)
        w = 3
        if self.chartsize <= GraphChartHelio.SMALL_SIZE:
            w = 1
        else:
            if self.chartsize <= GraphChartHelio.MEDIUM_SIZE:
                w = 2
        pen = wx.Pen(clr, w)
        self.bdc.SetPen(pen)
        self.drawLines(GraphChartHelio.DEG30, lon, self.r0, self.r30)
        clr = (0, 0, 0)
        for i in range(planets.Planets.MOON):
            if not self.bw:
                clr = self.options.clrplanets[i]
                if i == planets.Planets.SUN:
                    clr = self.options.clrLoF
            pen = wx.Pen(clr, 1)
            self.bdc.SetPen(pen)
            self.bdc.DrawCircle(cx, cy, self.rads[i])

        self.bdc.EndDrawing()

    def drawLines(self, deg, shift, r1, r2):
        cx, cy = self.center.Get()
        i = math.pi + math.radians(shift)
        while i > -math.pi + math.radians(shift):
            x1 = cx + math.cos(i) * r1
            y1 = cy + math.sin(i) * r1
            x2 = cx + math.cos(i) * r2
            y2 = cy + math.sin(i) * r2
            self.bdc.DrawLine(x1, y1, x2, y2)
            i -= deg

    def drawSigns(self):
        cx, cy = self.center.Get()
        clr = self.options.clrsigns
        if self.bw:
            clr = (0, 0, 0)
        lon = 0.0
        if self.options.ayanamsha != 0:
            lon -= self.chart.ayanamsha
            lon = util.normalize(lon)
        i = math.pi + math.radians(lon) - GraphChartHelio.DEG30 / 2
        signs = common.common.signs
        j = 0
        while j < chart.Chart.SIGN_NUM:
            x = cx + math.cos(i) * self.rSign
            y = cy + math.sin(i) * self.rSign
            self.draw.text((x - self.signSize / 2, y - self.signSize / 2), signs[j], font=self.fntMorinusSigns, fill=clr)
            i -= GraphChartHelio.DEG30
            j += 1

    def drawSymbols(self):
        cx, cy = self.center.Get()
        clr = (0, 0, 0)
        if not self.bw:
            clr = self.options.clrplanets[planets.Planets.SUN]
        self.draw.text((cx - self.symbolSize / 2, cy - self.symbolSize / 2), common.common.planets[planets.Planets.SUN], fill=clr, font=self.fntMorinus)
        for i in range(planets.Planets.MOON):
            lon = self.chart.planetshelio.lons[i]
            x = cx + math.cos(math.pi + math.radians(-lon)) * self.rads[i]
            y = cy + math.sin(math.pi + math.radians(-lon)) * self.rads[i]
            sym = common.common.fortune
            if not self.bw:
                clr = self.options.clrLoF
            if i != planets.Planets.SUN:
                sym = common.common.planets[i]
                if not self.bw:
                    clr = self.options.clrplanets[i]
            self.draw.text((x - self.symbolSize / 2, y - self.symbolSize / 2), sym, fill=clr, font=self.fntMorinus)