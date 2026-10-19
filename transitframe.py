# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, chart, positionswnd, positionswnd2, transitwnd, squarechartwnd, primdirs, placidiansapd, placidianutppd, regiomontanpd, primdirsrevlistframe, wx.lib.newevent, _thread, mtexts
PDReadyEvent, EVT_PDREADY = wx.lib.newevent.NewEvent()
pdlock = _thread.allocate_lock()

class TransitFrame(wx.Frame):
    XSIZE = 512
    YSIZE = 512
    CHART = 0
    COMPOUND = 1
    POSITIONS = 2
    SQUARE = 3

    def __init__(self, parent, title, chrt, radix, options, sel=0):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(TransitFrame.XSIZE, TransitFrame.YSIZE))
        self.chart = chrt
        self.radix = radix
        self.options = options
        self.parent = parent
        self.title = title
        self.pmenu = wx.Menu()
        self.ID_Selection = wx.NewId()
        self.ID_PrimaryDirections = wx.NewId()
        self.ID_SaveAsBitmap = wx.NewId()
        self.ID_BlackAndWhite = wx.NewId()
        self.ID_Chart = wx.NewId()
        self.ID_Comparison = wx.NewId()
        self.ID_Positions = wx.NewId()
        self.ID_Square = wx.NewId()
        self.ID_PDDirect = wx.NewId()
        self.ID_PDConverse = wx.NewId()
        self.ID_PDRadix = wx.NewId()
        self.selmenu = wx.Menu()
        self.chartmenu = self.selmenu.Append(self.ID_Chart, mtexts.txtspopupmenu['Chart'], '', wx.ITEM_RADIO)
        self.compoundmenu = self.selmenu.Append(self.ID_Comparison, mtexts.txtspopupmenu['Comparison'], '', wx.ITEM_RADIO)
        self.positionsmenu = self.selmenu.Append(self.ID_Positions, mtexts.txtspopupmenu['Positions'], '', wx.ITEM_RADIO)
        self.squaremenu = self.selmenu.Append(self.ID_Square, mtexts.txtspopupmenu['Square'], '', wx.ITEM_RADIO)
        self.pmenu.AppendMenu(self.ID_Selection, mtexts.txtspopupmenu['Windows'], self.selmenu)
        if self.chart.htype == chart.Chart.SOLAR or self.chart.htype == chart.Chart.LUNAR:
            self.pdselmenu = wx.Menu()
            self.pddirectmenu = self.pdselmenu.Append(self.ID_PDDirect, mtexts.txtspopupmenu['Direct'], '')
            self.pdconversemenu = self.pdselmenu.Append(self.ID_PDConverse, mtexts.txtspopupmenu['Converse'], '')
            self.pdtoradix = self.pdselmenu.Append(self.ID_PDRadix, mtexts.txtspopupmenu['PDRadix'], '', wx.ITEM_CHECK)
            self.pmenu.AppendMenu(self.ID_PrimaryDirections, mtexts.txtspopupmenu['PrimaryDirs'], self.pdselmenu)
            self.pdtoradix.Enable(False)
        self.pmenu.Append(self.ID_SaveAsBitmap, mtexts.txtspopupmenu['SaveAsBmp'], mtexts.txtspopupmenu['SaveChart'])
        self.mbw = self.pmenu.Append(self.ID_BlackAndWhite, mtexts.txtspopupmenu['BlackAndWhite'], mtexts.txtspopupmenu['ChartBW'], wx.ITEM_CHECK)
        self.SetMinSize((200, 200))
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_MENU, self.onChart, id=self.ID_Chart)
        self.Bind(wx.EVT_MENU, self.onComparison, id=self.ID_Comparison)
        self.Bind(wx.EVT_MENU, self.onPositions, id=self.ID_Positions)
        self.Bind(wx.EVT_MENU, self.onSquare, id=self.ID_Square)
        if self.chart.htype == chart.Chart.SOLAR or self.chart.htype == chart.Chart.LUNAR:
            self.Bind(wx.EVT_MENU, self.onPDDirect, id=self.ID_PDDirect)
            self.Bind(wx.EVT_MENU, self.onPDConverse, id=self.ID_PDConverse)
            self.Bind(wx.EVT_MENU, self.onPDRadix, id=self.ID_PDRadix)
        self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
        self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)
        if self.options.bw:
            self.mbw.Check()
        self.selection = sel
        if sel == TransitFrame.CHART:
            self.w = transitwnd.TransitWnd(self, self.chart, radix, options, parent)
            self.chartmenu.Check()
        else:
            self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, True)
            self.compoundmenu.Check()
        self.Bind(EVT_PDREADY, self.OnPDReady)

    def onPopupMenu(self, event):
        self.PopupMenu(self.pmenu, event.GetPosition())

    def onChart(self, event):
        if self.selection != TransitFrame.CHART:
            self.selection = TransitFrame.CHART
            self.w.Destroy()
            self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, False, -1, self.GetClientSize())

    def onComparison(self, event):
        if self.selection != TransitFrame.COMPOUND:
            self.selection = TransitFrame.COMPOUND
            self.w.Destroy()
            self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, True, -1, self.GetClientSize())

    def onPositions(self, event):
        if self.selection != TransitFrame.POSITIONS:
            self.selection = TransitFrame.POSITIONS
            self.w.Destroy()
            if wx.Platform == '__WXMSW__':
                self.w = positionswnd2.PositionsWnd2(self, self.chart, self.options, self.parent, -1, self.GetClientSize())
                self.w.Refresh()
            else:
                self.w = positionswnd.PositionsWnd(self, self.chart, self.options, self.parent, -1, self.GetClientSize())

    def onSquare(self, event):
        if self.selection != TransitFrame.SQUARE:
            self.selection = TransitFrame.SQUARE
            self.w.Destroy()
            self.w = squarechartwnd.SquareChartWnd(self, self.chart, self.options, self.parent, -1, self.GetClientSize())

    def onPDDirect(self, event):
        self.onPD(primdirs.PrimDirs.DIRECT)

    def onPDConverse(self, event):
        self.onPD(primdirs.PrimDirs.CONVERSE)

    def onPDRadix(self, event):
        pass

    def onSaveAsBitmap(self, event):
        self.w.onSaveAsBitmap(event)

    def onBlackAndWhite(self, event):
        self.w.onBlackAndWhite(event)

    def onPD(self, direction):
        pdrange = primdirs.PrimDirs.RANGEREV
        keytxt = ''
        if self.options.pdkeydyn:
            keytxt = mtexts.typeListDyn[self.options.pdkeyd]
        else:
            keytxt = mtexts.typeListStat[self.options.pdkeys]
        txt = mtexts.typeListDirs[self.options.primarydir] + '; ' + keytxt + '\n' + mtexts.txtscommon['BusyInfo']
        self.progbar = wx.ProgressDialog(mtexts.txtscommon['Calculating'], txt, parent=self, style=wx.PD_CAN_ABORT | wx.PD_APP_MODAL)
        self.progbar.Fit()
        self.pds = None
        self.pdready = False
        self.abort = primdirs.AbortPD()
        thId = _thread.start_new_thread(self.calcPDs, (pdrange, direction, self))
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(500)
        return

    def calcPDs(self, pdrange, direction, win):
        if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC:
            self.pds = placidiansapd.PlacidianSAPD(self.chart, self.options, pdrange, direction, self.abort)
        elif self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
            self.pds = placidianutppd.PlacidianUTPPD(self.chat, self.options, pdrange, direction, self.abort)
        else:
            self.pds = regiomontanpd.RegiomontanPD(self.chart, self.options, pdrange, direction, self.abort)
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
                self.abort.aborting()
        pdlock.release()

    def OnPDReady(self, event):
        self.timer.Stop()
        del self.timer
        self.progbar.Destroy()
        del self.progbar
        if self.abort.abort:
            self.Refresh()
        elif self.pds != None and len(self.pds.pds) > 0:
            pdw = primdirsrevlistframe.PrimDirsRevListFrame(self, self.parent, self.chart, self.options, self.pds, self.title.replace(mtexts.typeList[self.chart.htype], mtexts.txtsprimdirslist['PrimaryDirs']))
            pdw.Show(True)
        else:
            dlgm = wx.MessageDialog(self, mtexts.txtscommon['NoPDsWithSettings'], mtexts.txtscommon['Information'], wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
        if self.pds != None:
            del self.pds
        del self.abort
        return