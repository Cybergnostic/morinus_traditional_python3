# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, planets, chart, lots, common, commonwnd, Image, ImageDraw, ImageFont, util, mtexts

class LotsWnd(commonwnd.CommonWnd):

    def __init__(self, parent, chrt, opts, mainfr, id=-1, size=wx.DefaultSize):
        commonwnd.CommonWnd.__init__(self, parent, chrt, opts, id, size)
        self.mainfr = mainfr
        self.FONT_SIZE = int(21 * self.options.tablesize)
        self.SPACE = self.FONT_SIZE / 2
        self.LINE_HEIGHT = self.SPACE + self.FONT_SIZE + self.SPACE
        lengthlots = 0
        for l in range(len(self.options.lotsvisible)):
            if self.options.lotsvisible[l]:
                lengthlots += 1

        self.LINE_NUM = lengthlots
        self.COLUMN_NUM = 4
        self.SMALL_CELL_WIDTH = 3 * self.FONT_SIZE
        self.CELL_WIDTH = 12 * self.FONT_SIZE
        self.TITLE_HEIGHT = self.LINE_HEIGHT
        self.TITLE_WIDTH = self.SMALL_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.SPACE_TITLEY = 0
        self.TABLE_WIDTH = self.SMALL_CELL_WIDTH + self.COLUMN_NUM * self.CELL_WIDTH
        self.TABLE_HEIGHT = self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_NUM * self.LINE_HEIGHT
        self.WIDTH = commonwnd.CommonWnd.BORDER + self.TABLE_WIDTH + commonwnd.CommonWnd.BORDER
        self.HEIGHT = commonwnd.CommonWnd.BORDER + self.TABLE_HEIGHT + commonwnd.CommonWnd.BORDER
        self.SetVirtualSize((self.WIDTH, self.HEIGHT))
        self.fntMorinus = ImageFont.truetype(common.common.symbols, int(5.0 / 4.0 * self.FONT_SIZE))
        self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
        self.fntLord = ImageFont.truetype(common.common.abc, int(5.0 / 4.0 * self.FONT_SIZE))
        self.signs = common.common.signs
        self.deg_symbol = '\xb0'
        self.lordtxt = '!'
        self.drawBkg()

    def getExt(self):
        return mtexts.txtsabbrevs['Lot']

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
        txts = (mtexts.txtslots['Name'], mtexts.txtslots['Formula'], mtexts.txtslots['Longitude'], mtexts.txtslots['Almuten'])
        for i in range(len(txts)):
            w, h = draw.textsize(txts[i], self.fntText)
            draw.text((BOR + self.SMALL_CELL_WIDTH + self.CELL_WIDTH * i + (self.CELL_WIDTH - w) / 2, BOR + (self.TITLE_HEIGHT - h) / 2), txts[i], fill=txtclr, font=self.fntText)

        x = BOR
        y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY
        if self.chart.lots.lots != None:
            num = len(self.chart.lots.lots)
            x = BOR
            l = 0
            for i in range(num):
                if self.options.lotsvisible[i]:
                    y = BOR + self.TITLE_HEIGHT + self.SPACE_TITLEY + self.LINE_HEIGHT * l
                    self.drawline(draw, x, y, self.chart.lots.lots, tableclr, i, l)
                    l += 1

        wxImg = wx.EmptyImage(img.size[0], img.size[1])
        wxImg.SetData(img.tostring())
        self.buffer = wx.BitmapFromImage(wxImg)
        return

    def drawline(self, draw, x, y, data, clr, idx, ln):
        draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)
        offs = (
         0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
        BOR = commonwnd.CommonWnd.BORDER
        summa = 0
        txtclr = (0, 0, 0)
        if not self.bw:
            txtclr = self.options.clrtexts
        for i in range(self.COLUMN_NUM + 1 + 1 + 1):
            draw.line((x + summa + offs[i], y, x + summa + offs[i], y + self.LINE_HEIGHT), fill=clr)
            if i == 0:
                w, h = draw.textsize(str(idx + 1), self.fntText)
                draw.text((x + summa + (offs[(i + 1)] - w) / 2, y + (self.LINE_HEIGHT - h) / 2), str(idx + 1), fill=txtclr, font=self.fntText)
            elif i == lots.Lots.NAME + 1:
                name = data[idx][(i - 1)]
                w, h = draw.textsize(name, self.fntText)
                draw.text((x + summa + self.SMALL_CELL_WIDTH + (offs[(i + 1)] - w) / 2, y + (self.LINE_HEIGHT - h) / 2), name, fill=txtclr, font=self.fntText)
            elif i == lots.Lots.FORMULA + 1:
                A = mtexts.lotstxts[data[idx][lots.Lots.FORMULA][0]]
                B = mtexts.lotstxts[data[idx][lots.Lots.FORMULA][1]]
                C = mtexts.lotstxts[data[idx][lots.Lots.FORMULA][2]]
                origfs = (
                 A, B, C)
                wall = 0
                ar = [
                 [
                  [
                   A, self.fntText, txtclr, [0, 0]], ['', self.fntText, txtclr, [0, 0]], ['', self.fntText, txtclr, [0, 0]]], [[B, self.fntText, txtclr, [0, 0]], ['', self.fntText, txtclr, [0, 0]], ['', self.fntText, txtclr, [0, 0]]], [[C, self.fntText, txtclr, [0, 0]], ['', self.fntText, txtclr, [0, 0]], ['', self.fntText, txtclr, [0, 0]]]]
                delimtxts = [' + ', ' - ', '']
                for f in range(3):
                    for ff in range(3):
                        if data[idx][lots.Lots.FORMULA][f] >= lots.Lots.PLOFFS and data[idx][lots.Lots.FORMULA][f] <= lots.Lots.MOON or data[idx][lots.Lots.FORMULA][f] >= lots.Lots.PLLORDOFFS and data[idx][lots.Lots.FORMULA][f] <= lots.Lots.MOONLORD:
                            ploffs = lots.Lots.PLOFFS
                            lordtxt = ''
                            if data[idx][lots.Lots.FORMULA][f] >= lots.Lots.PLLORDOFFS and data[idx][lots.Lots.FORMULA][f] <= lots.Lots.MOONLORD:
                                ploffs = lots.Lots.PLLORDOFFS
                                lordtxt = self.lordtxt
                            plid = data[idx][lots.Lots.FORMULA][f] - ploffs
                            ar[f][0][0] = common.common.planets[plid]
                            ar[f][0][1] = self.fntMorinus
                            ar[f][1][0] = lordtxt
                            clrsym = (0, 0, 0)
                            if not self.bw:
                                clrsym = self.options.clrplanets[plid]
                            ar[f][0][2] = clrsym
                        elif data[idx][lots.Lots.FORMULA][f] == lots.Lots.DEG or data[idx][lots.Lots.FORMULA][f] == lots.Lots.DEGLORD:
                            lordtxt = ''
                            if data[idx][lots.Lots.FORMULA][f] == lots.Lots.DEGLORD:
                                lordtxt = self.lordtxt
                            sign = data[idx][lots.Lots.REFORDEG][f] / chart.Chart.SIGN_DEG
                            deg = data[idx][lots.Lots.REFORDEG][f] % chart.Chart.SIGN_DEG
                            ar[f][0][0] = str(deg)
                            ar[f][1][0] = common.common.signs[sign]
                            ar[f][1][1] = self.fntMorinus
                            ar[f][2][0] = lordtxt
                            clrsym = (0, 0, 0)
                            if not self.bw:
                                clrsym = self.options.clrsigns
                            ar[f][1][2] = clrsym
                        elif data[idx][lots.Lots.FORMULA][f] == lots.Lots.REF or data[idx][lots.Lots.FORMULA][f] == lots.Lots.REFLORD:
                            lordtxt = ''
                            if data[idx][lots.Lots.FORMULA][f] == lots.Lots.REFLORD:
                                lordtxt = self.lordtxt
                            sign = data[idx][lots.Lots.REFORDEG][f] / chart.Chart.SIGN_DEG
                            deg = data[idx][lots.Lots.REFORDEG][f] % chart.Chart.SIGN_DEG
                            ar[f][0][0] = mtexts.txtslotsdlg['R'] + str(data[idx][lots.Lots.REFORDEG][f])
                            ar[f][1][0] = lordtxt
                        elif data[idx][lots.Lots.FORMULA][f] == lots.Lots.LTI or data[idx][lots.Lots.FORMULA][f] == lots.Lots.LTILORD:
                            lordtxt = ''
                            if data[idx][lots.Lots.FORMULA][f] == lots.Lots.LTILORD:
                                lordtxt = self.lordtxt
                            abovehorizonSun = self.chart.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].abovehorizon
                            if self.chart.options.usedaynightorb:
                                abovehorizonSun = self.chart.abovehorizonwithorb
                            idLTI = planets.Planets.MOON
                            if not abovehorizonSun:
                                idLTI = planets.Planets.SUN
                            ar[f][0][0] = common.common.planets[idLTI]
                            ar[f][0][1] = self.fntMorinus
                            ar[f][1][0] = lordtxt
                            clrsym = (0, 0, 0)
                            if not self.bw:
                                clrsym = self.options.clrplanets[idLTI]
                            ar[f][0][2] = clrsym
                        elif data[idx][lots.Lots.FORMULA][f] == lots.Lots.LHO or data[idx][lots.Lots.FORMULA][f] == lots.Lots.LHOLORD:
                            lordtxt = ''
                            if data[idx][lots.Lots.FORMULA][f] == lots.Lots.LHOLORD:
                                lordtxt = self.lordtxt
                            ar[f][0][0] = common.common.planets[self.chart.time.ph.planetaryhour]
                            ar[f][0][1] = self.fntMorinus
                            ar[f][1][0] = lordtxt
                            clrsym = (0, 0, 0)
                            if not self.bw:
                                clrsym = self.options.clrplanets[self.chart.time.ph.planetaryhour]
                            ar[f][0][2] = clrsym
                        ar[f][ff][3] = draw.textsize(ar[f][ff][0], ar[f][ff][1])
                        wall += ar[f][ff][3][0]

                    ww, hh = draw.textsize(delimtxts[f], self.fntText)
                    wall += ww

                if data[idx][lots.Lots.DIURNAL] and not self.chart.planets.planets[planets.Planets.SUN].speculums[planets.Planet.PLACIDIAN].abovehorizon:
                    tmp = ar[1]
                    ar[1] = ar[2]
                    ar[2] = tmp
                begx = x + summa + self.CELL_WIDTH + (offs[i] - wall) / 2
                subwall = 0
                for f in range(3):
                    for ff in range(3):
                        draw.text((begx + subwall, y + (self.LINE_HEIGHT - h) / 2), ar[f][ff][0], fill=ar[f][ff][2], font=ar[f][ff][1])
                        subwall += ar[f][ff][3][0]

                    draw.text((begx + subwall, y + (self.LINE_HEIGHT - h) / 2), delimtxts[f], fill=txtclr, font=self.fntText)
                    ww, hh = draw.textsize(delimtxts[f], self.fntText)
                    subwall += ww

            elif i == lots.Lots.LON + 1:
                lon = data[idx][(i - 1)]
                d, m, s = util.decToDeg(lon)
                sign = d / chart.Chart.SIGN_DEG
                pos = d % chart.Chart.SIGN_DEG
                wsp, hsp = draw.textsize(' ', self.fntText)
                txtsign = self.signs[sign]
                wsg, hsg = draw.textsize(txtsign, self.fntMorinus)
                txt = str(pos).rjust(2) + self.deg_symbol + str(m).zfill(2) + "'" + str(s).zfill(2) + '"'
                w, h = draw.textsize(txt, self.fntText)
                offset = (offs[i] - (w + wsp + wsg)) / 2
                draw.text((x + summa + offset, y + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)
                draw.text((x + summa + offset + w + wsp, y + (self.LINE_HEIGHT - h) / 2), txtsign, fill=txtclr, font=self.fntMorinus)
            elif i == lots.Lots.DEGWINNER + 1:
                self.drawDegWinner2(draw, x + summa, y, data[idx][(i - 1)], txtclr)
            if i != lots.Lots.REFORDEG + 1:
                summa += offs[i]

    def drawDegWinner(self, draw, x, y, i, onlyone, degwinner, txtclr):
        aux = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        subnum = len(degwinner[0])
        mwidth = 0
        for j in range(subnum):
            pid = degwinner[i][j][0]
            if pid != -1:
                ptxt = common.common.planets[pid]
                wpl, hpl = draw.textsize(ptxt, self.fntMorinus)
                sco = degwinner[i][0][1]
                txt = '(' + str(sco) + ')'
                w, h = draw.textsize(txt, self.fntText)
                wsp, hsp = draw.textsize(' ', self.fntText)
                aux[j][0] = pid
                aux[j][1] = sco
                aux[j][2] = wpl + wsp + w
                if mwidth != 0:
                    mwidth += wsp
                mwidth += wpl + wsp + w
            else:
                break

        for j in range(subnum):
            if aux[j][0] != -1:
                clr = (0, 0, 0)
                if not self.bw:
                    clr = self.options.clrplanets[aux[j][0]]
                pltxt = common.common.planets[aux[j][0]]
                wpl, hpl = draw.textsize(pltxt, self.fntMorinus)
                txt = '(' + str(aux[j][1]) + ')'
                wsp, hsp = draw.textsize(' ', self.fntText)
                w, h = draw.textsize(txt, self.fntText)
                prev = 0
                for p in range(j):
                    prev += aux[j][2] + wsp

                offs = i
                if onlyone:
                    offs = 0
                draw.text((x + (self.CELL_WIDTH - mwidth) / 2 + prev, y + offs * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), pltxt, fill=clr, font=self.fntMorinus)
                draw.text((x + (self.CELL_WIDTH - mwidth) / 2 + prev + wpl + wsp, y + offs * self.LINE_HEIGHT + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)

    def drawDegWinner2(self, draw, x, y, degwinner, txtclr):
        aux = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        subnum = len(degwinner)
        mwidth = 0
        for j in range(subnum):
            pid = degwinner[j][0]
            if pid != -1:
                ptxt = common.common.planets[pid]
                wpl, hpl = draw.textsize(ptxt, self.fntMorinus)
                sco = degwinner[0][1]
                txt = '(' + str(sco) + ')'
                w, h = draw.textsize(txt, self.fntText)
                wsp, hsp = draw.textsize(' ', self.fntText)
                aux[j][0] = pid
                aux[j][1] = sco
                aux[j][2] = wpl + wsp + w
                if mwidth != 0:
                    mwidth += wsp
                mwidth += wpl + wsp + w
            else:
                break

        for j in range(subnum):
            if aux[j][0] != -1:
                clr = (0, 0, 0)
                if not self.bw:
                    clr = self.options.clrplanets[aux[j][0]]
                pltxt = common.common.planets[aux[j][0]]
                wpl, hpl = draw.textsize(pltxt, self.fntMorinus)
                txt = '(' + str(aux[j][1]) + ')'
                wsp, hsp = draw.textsize(' ', self.fntText)
                w, h = draw.textsize(txt, self.fntText)
                prev = 0
                for p in range(j):
                    prev += aux[j][2] + wsp

                draw.text((x + (self.CELL_WIDTH - mwidth) / 2 + prev, y + (self.LINE_HEIGHT - h) / 2), pltxt, fill=clr, font=self.fntMorinus)
                draw.text((x + (self.CELL_WIDTH - mwidth) / 2 + prev + wpl + wsp, y + (self.LINE_HEIGHT - h) / 2), txt, fill=txtclr, font=self.fntText)