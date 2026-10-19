# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, chart, primdirs, placidiansapd, placidianutppd, regiomontanpd, campanianpd, primdirslistwnd, intvalidator, rangechecker, mtexts, util, thread, wx.lib.newevent
PDReadyEvent, EVT_PDREADY = wx.lib.newevent.NewEvent()
pdlock = thread.allocate_lock()

class PrimDirsListFrame(wx.Frame):
    XSIZE = 640
    YSIZE = 400
    SEC1 = 0
    SEC5 = 1
    SEC10 = 2
    MIN1 = 3
    MIN5 = 4
    MIN10 = 5

    def __init__(self, parent, chrt, options, pds, title):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, size=wx.Size(PrimDirsListFrame.XSIZE, PrimDirsListFrame.YSIZE))
        self.parent = parent
        self.chart = chrt
        self.pdrange = pds.pdrange
        self.direction = pds.direction
        self.horoscope = None
        self.tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        tsize = (24, 24)
        tostart_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, tsize)
        back_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_TOOLBAR, tsize)
        forward_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, tsize)
        toend_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, tsize)
        self.tb.SetToolBitmapSize(tsize)
        self.ID_Start = 10
        self.tb.AddLabelTool(10, 'Start', tostart_bmp, shortHelp=mtexts.txtsprimdirslist['Start'], longHelp=mtexts.txtsprimdirslist['ToFirstPage'])
        self.Bind(wx.EVT_TOOL, self.OnStart, id=self.ID_Start)
        self.ID_Back = 20
        self.tb.AddLabelTool(20, 'Back', back_bmp, shortHelp=mtexts.txtsprimdirslist['Back'], longHelp=mtexts.txtsprimdirslist['ToBackPage'])
        self.Bind(wx.EVT_TOOL, self.OnBack, id=self.ID_Back)
        self.ID_Forward = 30
        self.tb.AddLabelTool(30, 'Forward', forward_bmp, shortHelp=mtexts.txtsprimdirslist['Forward'], longHelp=mtexts.txtsprimdirslist['ToForwardPage'])
        self.Bind(wx.EVT_TOOL, self.OnForward, id=self.ID_Forward)
        self.ID_End = 40
        self.tb.AddLabelTool(40, 'End', toend_bmp, shortHelp=mtexts.txtsprimdirslist['End'], longHelp=mtexts.txtsprimdirslist['ToLastPage'])
        self.Bind(wx.EVT_TOOL, self.OnEnd, id=self.ID_End)
        self.tb.AddSeparator()
        self.tb.AddControl(wx.StaticText(self.tb, -1, '              '))
        rnge = 3000
        checker = rangechecker.RangeChecker()
        if checker.isExtended():
            rnge = 5000
        self.year = wx.TextCtrl(self.tb, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,
                                                                                                     -1), style=wx.TE_READONLY)
        if checker.isExtended():
            self.year.SetHelpText(mtexts.txtsprimdirslist['HelpYear'])
        else:
            self.year.SetHelpText(mtexts.txtsprimdirslist['HelpYear2'])
        self.year.SetMaxLength(4)
        self.year.SetValue(str(chrt.time.origyear))
        self.tb.AddControl(self.year)
        self.tb.AddControl(wx.StaticText(self.tb, -1, ' '))
        self.month = wx.TextCtrl(self.tb, -1, '', validator=intvalidator.IntValidator(1, 12), size=(30,
                                                                                                    -1), style=wx.TE_READONLY)
        self.month.SetHelpText(mtexts.txtsprimdirslist['HelpMonth'])
        self.month.SetMaxLength(2)
        self.month.SetValue(str(chrt.time.origmonth).zfill(2))
        self.tb.AddControl(self.month)
        self.tb.AddControl(wx.StaticText(self.tb, -1, ' '))
        self.day = wx.TextCtrl(self.tb, -1, '', validator=intvalidator.IntValidator(1, 31), size=(30,
                                                                                                  -1), style=wx.TE_READONLY)
        self.day.SetHelpText(mtexts.txtsprimdirslist['HelpDay'])
        self.day.SetMaxLength(2)
        self.day.SetValue(str(chrt.time.origday).zfill(2))
        self.tb.AddControl(self.day)
        self.tb.AddControl(wx.StaticText(self.tb, -1, '   '))
        self.hour = wx.TextCtrl(self.tb, -1, '', validator=intvalidator.IntValidator(0, 23), size=(30,
                                                                                                   -1), style=wx.TE_READONLY)
        self.hour.SetHelpText(mtexts.txtsprimdirslist['HelpHour'])
        self.hour.SetMaxLength(2)
        self.hour.SetValue(str(chrt.time.hour))
        self.tb.AddControl(self.hour)
        self.tb.AddControl(wx.StaticText(self.tb, -1, ':'))
        self.minute = wx.TextCtrl(self.tb, -1, '', validator=intvalidator.IntValidator(0, 59), size=(30,
                                                                                                     -1), style=wx.TE_READONLY)
        self.minute.SetHelpText(mtexts.txtsprimdirslist['HelpMin'])
        self.minute.SetMaxLength(2)
        self.minute.SetValue(str(chrt.time.minute).zfill(2))
        self.tb.AddControl(self.minute)
        self.tb.AddControl(wx.StaticText(self.tb, -1, ':'))
        self.sec = wx.TextCtrl(self.tb, -1, '', validator=intvalidator.IntValidator(0, 59), size=(30,
                                                                                                  -1), style=wx.TE_READONLY)
        self.sec.SetHelpText(mtexts.txtsprimdirslist['HelpMin'])
        self.sec.SetMaxLength(2)
        self.sec.SetValue(str(chrt.time.second).zfill(2))
        self.tb.AddControl(self.sec)
        self.tb.AddControl(wx.StaticText(self.tb, -1, '     '))
        self.tb.AddControl(wx.StaticText(self.tb, -1, mtexts.txtsprimdirslist['Rectification']))
        self.tb.AddControl(wx.StaticText(self.tb, -1, ': '))
        self.recttypes = ('1s', '5s', '10s', '1m', '5m', '10m')
        self.rectcb = wx.ComboBox(self.tb, -1, self.recttypes[0], size=(70, -1), choices=self.recttypes, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.rectcb.SetSelection(0)
        self.tb.AddControl(self.rectcb)
        self.tb.AddControl(wx.StaticText(self.tb, -1, ' '))
        self.btnIncr = wx.Button(self.tb, -1, '+', size=(40, 30))
        self.tb.AddControl(self.btnIncr)
        self.btnDecr = wx.Button(self.tb, -1, '-', size=(40, 30))
        self.tb.AddControl(self.btnDecr)
        self.tb.AddControl(wx.StaticText(self.tb, -1, '  '))
        self.btnCalc = wx.Button(self.tb, -1, mtexts.txtsprimdirslist['Calculate'], size=(-1,
                                                                                          30))
        self.tb.AddControl(self.btnCalc)
        self.Bind(wx.EVT_BUTTON, self.onIncr, id=self.btnIncr.GetId())
        self.Bind(wx.EVT_BUTTON, self.onDecr, id=self.btnDecr.GetId())
        self.Bind(wx.EVT_BUTTON, self.onCalc, id=self.btnCalc.GetId())
        self.tb.Realize()
        self.initTB(chrt, options, pds, parent)
        self.SetMinSize((200, 200))
        self.Bind(EVT_PDREADY, self.OnPDReady)
        return

    def initTB(self, chrt, options, pds, parent):
        self.pdsmaxnum = len(pds.pds)
        self.currpage = 1
        self.LINE_NUM = 40
        self.PAGE = self.LINE_NUM * 2
        remainder = self.pdsmaxnum % self.PAGE
        addition = 0
        if remainder > 0:
            addition = 1
        self.maxpage = int(self.pdsmaxnum / self.PAGE) + addition
        fr, to = self.getRange()
        self.w = primdirslistwnd.PrimDirsListWnd(self, chrt, options, pds, parent, 1, self.maxpage, fr, to, -1, self.GetClientSize())
        self.tb.EnableTool(self.ID_Start, False)
        self.tb.EnableTool(self.ID_Back, False)
        if self.maxpage == 1:
            self.tb.EnableTool(self.ID_End, False)
            self.tb.EnableTool(self.ID_Forward, False)
        else:
            self.tb.EnableTool(self.ID_End, True)
            self.tb.EnableTool(self.ID_Forward, True)

    def OnStart(self, event):
        if self.currpage != 1:
            wait = wx.BusyCursor()
            self.currpage = 1
            self.tb.EnableTool(self.ID_Start, False)
            self.tb.EnableTool(self.ID_Back, False)
            self.tb.EnableTool(self.ID_End, True)
            self.tb.EnableTool(self.ID_Forward, True)
            fr, to = self.getRange()
            self.w.display(self.currpage, fr, to)

    def OnBack(self, event):
        if self.currpage != 1:
            wait = wx.BusyCursor()
            self.currpage -= 1
            self.tb.EnableTool(self.ID_Start, self.currpage != 1)
            self.tb.EnableTool(self.ID_Back, self.currpage != 1)
            self.tb.EnableTool(self.ID_End, True)
            self.tb.EnableTool(self.ID_Forward, True)
            fr, to = self.getRange()
            self.w.display(self.currpage, fr, to)

    def OnForward(self, event):
        if self.currpage != self.maxpage:
            wait = wx.BusyCursor()
            self.currpage += 1
            self.tb.EnableTool(self.ID_End, self.currpage != self.maxpage)
            self.tb.EnableTool(self.ID_Forward, self.currpage != self.maxpage)
            self.tb.EnableTool(self.ID_Start, True)
            self.tb.EnableTool(self.ID_Back, True)
            fr, to = self.getRange()
            self.w.display(self.currpage, fr, to)

    def OnEnd(self, event):
        if self.currpage != self.maxpage:
            wait = wx.BusyCursor()
            self.currpage = self.maxpage
            self.tb.EnableTool(self.ID_End, False)
            self.tb.EnableTool(self.ID_Forward, False)
            self.tb.EnableTool(self.ID_Start, True)
            self.tb.EnableTool(self.ID_Back, True)
            fr, to = self.getRange()
            self.w.display(self.currpage, fr, to)

    def getRange(self):
        fr = (self.currpage - 1) * self.PAGE
        to = self.currpage * self.PAGE
        if to > self.pdsmaxnum:
            to = self.pdsmaxnum
        return (fr, to)

    def onIncr(self, evt):
        idx = self.rectcb.GetCurrentSelection()
        y, m, d, h, mi, s = (
         int(self.year.GetValue()), int(self.month.GetValue()), int(self.day.GetValue()), int(self.hour.GetValue()), int(self.minute.GetValue()), int(self.sec.GetValue()))
        if idx == PrimDirsListFrame.SEC1 or idx == PrimDirsListFrame.SEC5 or idx == PrimDirsListFrame.SEC10:
            sadd = 1
            if idx == PrimDirsListFrame.SEC5:
                sadd = 5
            if idx == PrimDirsListFrame.SEC10:
                sadd = 10
            y, m, d, h, mi, s = util.addSecs(y, m, d, h, mi, s, sadd)
        else:
            madd = 1
            if idx == PrimDirsListFrame.MIN5:
                madd = 5
            if idx == PrimDirsListFrame.MIN10:
                madd = 10
            y, m, d, h, mi = util.addMins(y, m, d, h, mi, madd)
        self.year.SetValue(str(y))
        self.month.SetValue(str(m).zfill(2))
        self.day.SetValue(str(d).zfill(2))
        self.hour.SetValue(str(h))
        self.minute.SetValue(str(mi).zfill(2))
        self.sec.SetValue(str(s).zfill(2))

    def onDecr(self, evt):
        if int(self.year.GetValue()) <= 1:
            return
        idx = self.rectcb.GetCurrentSelection()
        y, m, d, h, mi, s = (
         int(self.year.GetValue()), int(self.month.GetValue()), int(self.day.GetValue()), int(self.hour.GetValue()), int(self.minute.GetValue()), int(self.sec.GetValue()))
        if idx == PrimDirsListFrame.SEC1 or idx == PrimDirsListFrame.SEC5 or idx == PrimDirsListFrame.SEC10:
            ssub = 1
            if idx == PrimDirsListFrame.SEC5:
                ssub = 5
            if idx == PrimDirsListFrame.SEC10:
                ssub = 10
            y, m, d, h, mi, s = util.subtractSecs(y, m, d, h, mi, s, ssub)
        else:
            msub = 1
            if idx == PrimDirsListFrame.MIN5:
                msub = 5
            if idx == PrimDirsListFrame.MIN10:
                msub = 10
            y, m, d, h, mi = util.subtractMins(y, m, d, h, mi, msub)
        self.year.SetValue(str(y))
        self.month.SetValue(str(m).zfill(2))
        self.day.SetValue(str(d).zfill(2))
        self.hour.SetValue(str(h))
        self.minute.SetValue(str(mi).zfill(2))
        self.sec.SetValue(str(s).zfill(2))

    def onCalc(self, evt):
        time = chart.Time(int(self.year.GetValue()), int(self.month.GetValue()), int(self.day.GetValue()), int(self.hour.GetValue()), int(self.minute.GetValue()), int(self.sec.GetValue()), self.chart.time.bc, self.chart.time.cal, self.chart.time.zt, self.chart.time.plus, self.chart.time.zh, self.chart.time.zm, self.chart.time.daylightsaving, self.chart.place)
        self.horoscope = chart.Chart(self.chart.name, self.chart.male, time, self.chart.place, self.chart.htype, self.chart.notes, self.chart.options)
        keytxt = ''
        if self.chart.options.pdkeydyn:
            keytxt = mtexts.typeListDyn[self.chart.options.pdkeyd]
        else:
            keytxt = mtexts.typeListStat[self.chart.options.pdkeys]
        txt = mtexts.typeListDirs[self.chart.options.primarydir] + '; ' + keytxt + '\n' + mtexts.txtscommon['BusyInfo']
        self.progbar = wx.ProgressDialog(mtexts.txtscommon['Calculating'], txt, parent=self, style=wx.PD_CAN_ABORT | wx.PD_APP_MODAL)
        self.progbar.Fit()
        self.pds = None
        self.pdready = False
        self.abort = primdirs.AbortPD()
        thId = thread.start_new_thread(self.calcPDs, (self.pdrange, self.direction, self))
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(500)
        return

    def calcPDs(self, pdrange, direction, win):
        if self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC:
            self.pds = placidiansapd.PlacidianSAPD(self.horoscope, self.chart.options, pdrange, direction, self.abort)
        elif self.chart.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
            self.pds = placidianutppd.PlacidianUTPPD(self.horoscope, self.chart.options, pdrange, direction, self.abort)
        elif self.chart.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
            self.pds = regiomontanpd.RegiomontanPD(self.horoscope, self.chart.options, pdrange, direction, self.abort)
        else:
            self.pds = campanianpd.CampanianPD(self.horoscope, self.options, pdrange, direction, self.abort)
        pdlock.acquire()
        self.pdready = True
        pdlock.release()
        evt = PDReadyEvent()
        wx.PostEvent(win, evt)

    def OnTimer(self, event):
        pdlock.acquire()
        if not self.pdready:
            keepGoing, skip = self.progbar.Pulse()
            if not keepGoing:
                self.abort.abort = True
        pdlock.release()

    def OnPDReady(self, event):
        self.timer.Stop()
        del self.timer
        self.progbar.Destroy()
        del self.progbar
        if self.abort.abort:
            self.Refresh()
        elif self.pds != None and len(self.pds.pds) > 0:
            self.w.Destroy()
            self.initTB(self.horoscope, self.chart.options, self.pds, self.parent)
        else:
            dlgm = wx.MessageDialog(self, mtexts.txtscommon['NoPDsWithSettings'], mtexts.txtscommon['Information'], wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
        if self.pds != None:
            del self.pds
        del self.abort
        return