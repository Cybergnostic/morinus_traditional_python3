# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import os
import wx
import chart
import planets
import common
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import util
import mtexts

class GraphEphemWnd(wx.Window):
    SMALL_SIZE = 400
    INTERMEDIATE_SIZE = 500
    MEDIUM_SIZE = 600

    def __init__(self, parent, year, posArr, opts, mainfr, id=-1, size=wx.DefaultSize):
        wx.Window.__init__(self, parent, id, wx.DefaultPosition, size=size)
        self.parent = parent
        self.year = year
        self.posArr = posArr
        self.options = opts
        self.mainfr = mainfr
        self.bw = self.options.bw
        self.parent.mbw.Check(self.bw)
        self.SetBackgroundColour(self.options.clrbackground)
        self.drawBkg()
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)

    def drawBkg(self):
        size = self.GetClientSize()
        self.w, self.h = size
        self.buffer = wx.Bitmap(self.w, self.h)
        self.bdc = wx.BufferedDC(None, self.buffer)
        self.tableSize = min(self.w, self.h)
        self.planetSymbolSize = int(self.tableSize // 40)
        self.BORDER = self.planetSymbolSize
        self.spaceSize = self.planetSymbolSize // 3
        y1 = self.BORDER
        y2 = self.h - 4 * self.BORDER
        self.signSize = (y2 - y1) // (chart.Chart.SIGN_NUM + 2)
        self.signSymbolSize = self.signSize // 2
        self.fontSize = self.planetSymbolSize
        x1 = 2 * self.BORDER + self.signSymbolSize + self.spaceSize
        x2 = self.w - 2 * self.BORDER
        self.monthSize = (x2 - x1) // 13
        self.txtSymbolSize = self.monthSize // 4
        self.txtSymbolSize = min(self.signSize, self.monthSize) // 3
        self.signSymbolSize = self.txtSymbolSize
        self.fntPlanets = util.truetype(common.common.symbols, self.planetSymbolSize)
        self.fntSigns = util.truetype(common.common.symbols, self.signSymbolSize)
        self.fntTxt = util.truetype(common.common.abc, self.txtSymbolSize)
        tableclr = (0, 0, 0)
        txtclr = (0, 0, 0)
        bkgclr = (255, 255, 255)
        plsclr = (0, 0, 0)
        signsclr = (0, 0, 0)
        if not self.bw:
            bkgclr = self.options.clrbackground
            tableclr = self.options.clrframe
            txtclr = self.options.clrtexts
            signsclr = self.options.clrsigns
        self.bdc.SetBackground(wx.Brush(bkgclr))
        self.bdc.SetBrush(wx.Brush(bkgclr))
        self.bdc.Clear()
        w = 4
        if self.tableSize <= GraphEphemWnd.SMALL_SIZE:
            w = 2
        else:
            if self.tableSize <= GraphEphemWnd.MEDIUM_SIZE:
                w = 3
        pen = wx.Pen(tableclr, w)
        self.bdc.SetPen(pen)
        x1 = 2 * self.BORDER + self.signSymbolSize + self.spaceSize
        y1 = self.BORDER
        x2 = x1
        y2 = self.h - self.BORDER
        self.bdc.DrawLine(int(x1), int(y1), int(x2), int(y2))
        x1 = self.BORDER
        y1 = self.h - 4 * self.BORDER
        x2 = self.w - self.BORDER
        y2 = self.h - 4 * self.BORDER
        self.bdc.DrawLine(int(x1), int(y1), int(x2), int(y2))
        pen = wx.Pen(tableclr, 1, wx.USER_DASH)
        pen.SetDashes([6, 3])
        self.bdc.SetPen(pen)
        y1 = self.h - 4 * self.BORDER
        for i in range(chart.Chart.SIGN_NUM + 1):
            y1 -= self.signSize

        x1 = 2 * self.BORDER + self.signSymbolSize + self.spaceSize
        x2 = x1
        y2 = self.h - 4 * self.BORDER
        for i in range(13):
            x1 += self.monthSize
            x2 += self.monthSize
            self.bdc.DrawLine(int(x1), int(y1), int(x2), int(y2))

        x1 = 2 * self.BORDER + self.signSymbolSize + self.spaceSize
        y1 = self.h - 4 * self.BORDER
        y2 = self.h - 4 * self.BORDER
        for i in range(chart.Chart.SIGN_NUM + 1):
            y1 -= self.signSize
            y2 -= self.signSize
            self.bdc.DrawLine(int(x1), int(y1), int(x2), int(y2))

        plpixelpos = []
        pltoppixelpos = []
        plstopids = []
        plstop = []
        plbottompixelpos = []
        plsbottomids = []
        plsbottom = []
        xOrig = 2 * self.BORDER + self.signSymbolSize + self.spaceSize + self.monthSize
        yOrig = self.h - 4 * self.BORDER - self.signSize
        yOrig2 = yOrig
        for i in range(chart.Chart.SIGN_NUM):
            yOrig2 -= self.signSize

        pixelsPer360 = self.signSize * chart.Chart.SIGN_NUM
        pixelsPer365 = self.monthSize * 12
        scale360 = pixelsPer360 / 360.0
        scale365 = pixelsPer365 / 365.0
        plnum = len(self.posArr)
        posnum = len(self.posArr[0])
        for pl in range(planets.Planets.PLANETS_NUM - 1):
            prevx = prevy = 0.0
            for i in range(posnum):
                x = xOrig + i * scale365
                y = yOrig - self.posArr[pl][i] * scale360
                if i == 0:
                    plpixelpos.append(y)
                if not self.bw:
                    plsclr = self.options.clrplanets[pl]
                w = 2
                if self.tableSize <= GraphEphemWnd.INTERMEDIATE_SIZE:
                    w = 1
                pen = wx.Pen(plsclr, w)
                self.bdc.SetPen(pen)
                self.bdc.DrawPoint(int(x), int(y))
                transition = prevy > self.h - 4 * self.BORDER - 2 * self.signSize and y < yOrig2 + self.signSize or y > self.h - 4 * self.BORDER - 2 * self.signSize and prevy < yOrig2 + self.signSize
                if i != 0 and not transition:
                    self.bdc.DrawLine(int(prevx), int(prevy), int(x), int(y))
                if i != 0 and transition:
                    if prevy > self.h - 4 * self.BORDER - 2 * self.signSize and y < yOrig2 + self.signSize:
                        pltoppixelpos.append(x)
                        plstopids.append(pl)
                        plstop.append(common.common.planets[pl])
                    if y > self.h - 4 * self.BORDER - 2 * self.signSize and prevy < yOrig2 + self.signSize:
                        plbottompixelpos.append(x)
                        plsbottomids.append(pl)
                        plsbottom.append(common.common.planets[pl])
                prevx = x
                prevy = y

        bshift = self.arrange(common.common.planets, plpixelpos, yOrig2, yOrig)
        xOrig2 = xOrig
        for i in range(13):
            xOrig2 += self.monthSize

        if len(plstop) > 1:
            bshifttop = self.arrange(plstop, pltoppixelpos, xOrig, xOrig2)
        if len(plsbottom) > 1:
            bshiftbottom = self.arrange(plsbottom, plbottompixelpos, xOrig, xOrig2)
        x1 = 2 * self.BORDER + self.signSymbolSize + self.spaceSize + self.monthSize - 3 * self.spaceSize
        x2 = 2 * self.BORDER + self.signSymbolSize + self.spaceSize + self.monthSize
        for pl in range(planets.Planets.PLANETS_NUM - 1):
            y = plpixelpos[pl]
            if not self.bw:
                plsclr = self.options.clrplanets[pl]
            pen = wx.Pen(plsclr, 1)
            self.bdc.SetPen(pen)
            self.bdc.DrawLine(int(x1), int(y + bshift[pl]), int(x2), int(y))

        if len(plstop) != 0:
            y1 = yOrig2
            y2 = yOrig2 - 3 * self.spaceSize
            plstopnum = len(plstop)
            for pl in range(plstopnum):
                x = pltoppixelpos[pl]
                if not self.bw:
                    plsclr = self.options.clrplanets[plstopids[pl]]
                pen = wx.Pen(plsclr, 1)
                self.bdc.SetPen(pen)
                if len(plstop) > 1:
                    self.bdc.DrawLine(int(x), int(y1), int(x + bshifttop[pl]), int(y2))
                else:
                    self.bdc.DrawLine(int(x), int(y1), int(x), int(y2))

        if len(plsbottom) != 0:
            y1 = yOrig + 3 * self.spaceSize
            y2 = yOrig
            plsbottomnum = len(plsbottom)
            for pl in range(plsbottomnum):
                x = plbottompixelpos[pl]
                if not self.bw:
                    plsclr = self.options.clrplanets[plsbottomids[pl]]
                pen = wx.Pen(plsclr, 1)
                self.bdc.SetPen(pen)
                if len(plsbottom) > 1:
                    self.bdc.DrawLine(int(x + bshiftbottom[pl]), int(y1), int(x), int(y2))
                else:
                    self.bdc.DrawLine(int(x), int(y1), int(x), int(y2))

        wxImag = self.buffer.ConvertToImage()
        img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
        img.frombytes(wxImag.GetData())
        draw = ImageDraw.Draw(img)
        x = 2 * self.BORDER
        y = self.h - 4 * self.BORDER - self.signSize
        for i in range(chart.Chart.SIGN_NUM):
            wsym, hsym = draw.textbbox((0, 0), common.common.signs[i], self.fntSigns)[2:]
            draw.text((x, y - self.signSize // 2 - hsym // 2 - i * self.signSize), common.common.signs[i], fill=signsclr, font=self.fntSigns)

        txt = str(self.year)
        wtxt, htxt = draw.textbbox((0, 0), txt, self.fntTxt)[2:]
        x = 2 * self.BORDER + self.signSymbolSize + self.spaceSize
        y = self.h - 4 * self.BORDER + self.spaceSize
        offs = (self.monthSize - wtxt) // 2
        draw.text((x + offs, y), txt, fill=tableclr, font=self.fntTxt)
        x = 2 * self.BORDER + self.signSymbolSize + self.spaceSize + self.monthSize
        y = self.h - 4 * self.BORDER + self.spaceSize
        mnum = len(mtexts.monthabbr)
        for i in range(mnum):
            txt = mtexts.monthabbr[i]
            wtxt, htxt = draw.textbbox((0, 0), txt, self.fntTxt)[2:]
            offs = (self.monthSize - wtxt) // 2
            draw.text((x + i * self.monthSize + offs, y), txt, fill=tableclr, font=self.fntTxt)

        x = 2 * self.BORDER + self.signSymbolSize + self.spaceSize + self.monthSize - 2 * self.spaceSize
        for pl in range(planets.Planets.PLANETS_NUM - 1):
            y = plpixelpos[pl]
            if not self.bw:
                plsclr = self.options.clrplanets[pl]
            wsym, hsym = draw.textbbox((0, 0), common.common.planets[pl], self.fntPlanets)[2:]
            xoffs = 2 * self.spaceSize + wsym
            draw.text((x - xoffs, y - hsym // 2 + bshift[pl]), common.common.planets[pl], fill=plsclr, font=self.fntPlanets)

        if len(plstop) != 0:
            y = yOrig2 - 2 * self.spaceSize
            plstopnum = len(plstop)
            for pl in range(plstopnum):
                x = pltoppixelpos[pl]
                if not self.bw:
                    plsclr = self.options.clrplanets[plstopids[pl]]
                wsym, hsym = draw.textbbox((0, 0), plstop[pl], self.fntPlanets)[2:]
                yoffs = 2 * self.spaceSize + hsym
                if len(plstop) > 1:
                    draw.text((x - wsym // 2 + bshifttop[pl], y - yoffs), plstop[pl], fill=plsclr, font=self.fntPlanets)
                else:
                    draw.text((x - wsym // 2, y - yoffs), plstop[pl], fill=plsclr, font=self.fntPlanets)

        if len(plsbottom) != 0:
            y = yOrig + 2 * self.spaceSize
            plsbootmnum = len(plsbottom)
            for pl in range(plsbottomnum):
                x = plbottompixelpos[pl]
                if not self.bw:
                    plsclr = self.options.clrplanets[plsbottomids[pl]]
                wsym, hsym = draw.textbbox((0, 0), plsbottom[pl], self.fntPlanets)[2:]
                yoffs = 2 * self.spaceSize
                if len(plsbottom) > 1:
                    draw.text((x - wsym // 2 + bshiftbottom[pl], y + yoffs), plsbottom[pl], fill=plsclr, font=self.fntPlanets)
                else:
                    draw.text((x - wsym // 2, y + yoffs), plsbottom[pl], fill=plsclr, font=self.fntPlanets)

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)
        self.Refresh()
        return

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

    def onPopupMenu(self, event):
        self.parent.onPopupMenu(event)

    def onSaveAsBitmap(self, event):
        name = mtexts.txtsabbrevs['Ephem'] + str(self.year)
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

    def onSize(self, event):
        self.drawBkg()

    def arrange(self, pls, plpixelpos, smallerBOR, greaterBOR):
        """Arranges bodies so they won't overlap each other"""
        bshift = []
        order = []
        mixed = []
        num = len(plpixelpos)
        for i in range(num):
            order.append(plpixelpos[i])
            mixed.append(i)
            bshift.append(0.0)

        for j in range(num):
            for i in range(num - 1):
                if order[i] > order[(i + 1)]:
                    tmp = order[i]
                    order[i] = order[(i + 1)]
                    order[i + 1] = tmp
                    tmp = mixed[i]
                    mixed[i] = mixed[(i + 1)]
                    mixed[i + 1] = tmp

        for i in range(num + 1):
            self.doArrange(num, pls, bshift, order, mixed)

        BOR = smallerBOR
        if order[0] + bshift[mixed[0]] < BOR:
            diff = BOR - (order[0] + bshift[mixed[0]])
            bshift[mixed[0]] += diff
            for i in range(num - 1):
                w1, h1 = self.fntPlanets.getbbox(pls[i])[2:]
                w2, h2 = self.fntPlanets.getbbox(pls[(i + 1)])[2:]
                x1 = order[i] + bshift[mixed[i]]
                x2 = order[(i + 1)] + bshift[mixed[(i + 1)]]
                if order[i] + bshift[mixed[i]] > order[(i + 1)] + bshift[mixed[(i + 1)]] or self.overlap(x1, w1, x2, w2):
                    bshift[mixed[(i + 1)]] += diff
                else:
                    break

        lenord = num - 1
        val = order[lenord] + bshift[mixed[lenord]]
        if order[lenord] + bshift[mixed[lenord]] > greaterBOR:
            diff = order[lenord] + bshift[mixed[lenord]] - greaterBOR
            bshift[mixed[lenord]] -= diff
            for i in range(lenord, 0, -1):
                w1, h1 = self.fntPlanets.getbbox(pls[(i - 1)])[2:]
                w2, h2 = self.fntPlanets.getbbox(pls[i])[2:]
                x1 = order[(i - 1)] + bshift[mixed[(i - 1)]]
                x2 = order[i] + bshift[mixed[i]]
                if order[(i - 1)] + bshift[mixed[(i - 1)]] > order[i] + bshift[mixed[i]] or self.overlap(x1, w1, x2, w2):
                    bshift[(i - 1)] -= diff
                else:
                    break

        return bshift[:]

    def doArrange(self, num, pls, bshift, order, mixed, forward=False):
        shifted = False
        for i in range(num - 1):
            shifted = self.doShift(i, i + 1, pls, bshift, order, mixed, forward)

        if shifted:
            self.doArrange(num, pls, bshift, order, mixed, forward)

    def doShift(self, b1, b2, pls, bshift, order, mixed, forward=False):
        shifted = False
        x1 = order[b1] + bshift[mixed[b1]]
        x2 = order[b2] + bshift[mixed[b2]]
        w1, h1 = self.fntPlanets.getbbox(pls[mixed[b1]])[2:]
        w2, h2 = self.fntPlanets.getbbox(pls[mixed[b2]])[2:]
        while self.overlap(x1, w1, x2, w2):
            if not forward:
                bshift[mixed[b1]] -= 1.0
            bshift[mixed[b2]] += 1.0
            x1 = order[b1] + bshift[mixed[b1]]
            x2 = order[b2] + bshift[mixed[b2]]
            if not shifted:
                shifted = True

        return shifted

    def overlap(self, x1, w1, x2, w2):
        return x1 <= x2 and x2 <= x1 + w1 + self.spaceSize or x2 <= x1 and x1 <= x2 + w2 + self.spaceSize