# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
import wx
import menubars
import chart
import positionswnd
import positionswnd2
import transitwnd
import squarechartwnd
import primdirs
import placidiansapd
import placidianutppd
import regiomontanpd
import primdirsrevlistframe
import wx.lib.newevent
import _thread
import mtexts
import electionstepperdlg
import returnstepperdlg
import returnslist
import divisionswnd
import util
import sidebar
import time as _time
import tradoptions
PDReadyEvent, EVT_PDREADY = wx.lib.newevent.NewEvent()
pdlock = _thread.allocate_lock()

class TransitFrame(wx.Frame):
    XSIZE = 512
    YSIZE = 512
    CHART = 0
    COMPOUND = 1
    POSITIONS = 2
    SQUARE = 3

    def __init__(self, parent, title, chrt, radix, options, sel=0, stepper=None):
        wx.Frame.__init__(self, parent, -1, i18n.tr(title), wx.DefaultPosition, wx.Size(TransitFrame.XSIZE, TransitFrame.YSIZE))
        self.chart = chrt
        self.radix = radix
        self.options = options
        self.parent = parent
        self.title = title
        self.pmenu = wx.Menu()
        menubars.later(self, 'Chart')
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
        self.ID_Divisions = wx.NewId()
        self.selmenu = wx.Menu()
        self.chartmenu = self.selmenu.Append(self.ID_Chart, i18n.tr(mtexts.txtspopupmenu['Chart']), '', wx.ITEM_RADIO)
        self.compoundmenu = self.selmenu.Append(self.ID_Comparison, i18n.tr(mtexts.txtspopupmenu['Comparison']), '', wx.ITEM_RADIO)
        self.positionsmenu = self.selmenu.Append(self.ID_Positions, i18n.tr(mtexts.txtspopupmenu['Positions']), '', wx.ITEM_RADIO)
        self.squaremenu = self.selmenu.Append(self.ID_Square, i18n.tr(mtexts.txtspopupmenu['Square']), '', wx.ITEM_RADIO)
        self.pmenu.Append(wx.MenuItem(self.pmenu, self.ID_Selection, mtexts.txtspopupmenu['Windows'], subMenu=self.selmenu))
        if self.chart.htype == chart.Chart.SOLAR or self.chart.htype == chart.Chart.LUNAR:
            self.pdselmenu = wx.Menu()
            self.pddirectmenu = self.pdselmenu.Append(self.ID_PDDirect, i18n.tr(mtexts.txtspopupmenu['Direct']), '')
            self.pdconversemenu = self.pdselmenu.Append(self.ID_PDConverse, i18n.tr(mtexts.txtspopupmenu['Converse']), '')
            self.pdtoradix = self.pdselmenu.Append(self.ID_PDRadix, i18n.tr(mtexts.txtspopupmenu['PDRadix']), '', wx.ITEM_CHECK)
            self.pmenu.Append(wx.MenuItem(self.pmenu, self.ID_PrimaryDirections, mtexts.txtspopupmenu['PrimaryDirs'], subMenu=self.pdselmenu))
            self.pdtoradix.Enable(False)
        if self.chart.htype == chart.Chart.SOLAR:
            self.pmenu.Append(self.ID_Divisions, i18n.tr('Divisions (Valens)'),
                              i18n.tr('Planetary periods in this solar year'))
        # stepping: previous/next return for solar and lunar returns, time steps otherwise
        self.ID_Step = wx.NewIdRef()
        # stepper(chart, forward) -> the chart before or after (e.g. the lunations)
        self.stepper = stepper
        steptxt = {chart.Chart.SOLAR: 'Step solar returns... (arrow keys)', chart.Chart.LUNAR: 'Step lunar returns... (arrow keys)', chart.Chart.TRANSIT: 'Step time... (arrow keys)'}.get(self.chart.htype)
        if stepper is not None:
            for label, forward in (('Previous lunation (Left)', False), ('Next lunation (Right)', True)):
                item = self.pmenu.Append(wx.NewIdRef(), i18n.tr(label), i18n.tr('The New or Full Moon before or after this one'))
                self.Bind(wx.EVT_MENU, lambda e, f=forward: self.stepTo(f), id=item.GetId())
            self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
        elif steptxt is not None:
            self.pmenu.Append(self.ID_Step, i18n.tr(steptxt), i18n.tr('Move the chart forward or backward in time'))
            self.Bind(wx.EVT_MENU, self.onStep, id=self.ID_Step)
            self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
        self.pmenu.Append(self.ID_SaveAsBitmap, i18n.tr(mtexts.txtspopupmenu['SaveAsBmp']), i18n.tr(mtexts.txtspopupmenu['SaveChart']))
        self.mbw = self.pmenu.Append(self.ID_BlackAndWhite, i18n.tr(mtexts.txtspopupmenu['BlackAndWhite']), i18n.tr(mtexts.txtspopupmenu['ChartBW']), wx.ITEM_CHECK)
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
        if self.chart.htype == chart.Chart.SOLAR:
            self.Bind(wx.EVT_MENU, self.onDivisions, id=self.ID_Divisions)
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
        # Same resizable sidebar as the main chart.
        self.sidebar_width = tradoptions.get('sidebar_width')
        self._sidebar_last_draw = 0.0
        self.sidebar = sidebar.Sidebar(self, self.onSidebarResize)
        self.sidebar.setChart(self.chart, self.radix)
        self.msidebar = self.pmenu.AppendCheckItem(wx.NewIdRef(), i18n.tr('Planet sidebar'), i18n.tr('Show the planet, chart and time lords beside the chart'))
        self.msidebar.Check(tradoptions.get('show_sidebar'))
        self.Bind(wx.EVT_MENU, self.onSidebar, id=self.msidebar.GetId())
        self.Bind(wx.EVT_SIZE, self.onFrameSize)
        if tradoptions.get('show_sidebar'):
            self.SetSize((TransitFrame.XSIZE + self.sidebar_width, TransitFrame.YSIZE))
        self.layout()

    def layout(self):
        """The chart (or table) on the left, the sidebar on the right."""
        w, h = self.GetClientSize()
        show = tradoptions.get('show_sidebar')
        sw = sidebar.fit_width(w, self.sidebar_width) if show else 0
        self.sidebar.Show(show)
        if show:
            self.sidebar.SetSize(w - sw, 0, sw, h)
        self.w.SetSize(0, 0, max(w - sw, 50), h)

    def onSidebarResize(self, preferred, finished):
        """Drag the panel edge and remember the width when released."""
        width = sidebar.fit_width(self.GetClientSize().width, preferred)
        if width == self.sidebar.GetSize().width and not finished:
            return
        self.sidebar_width = width
        now = _time.monotonic()
        if finished:
            tradoptions.set({'sidebar_width': width})
            if self.options.autosave:
                tradoptions.save()
        if finished or now - self._sidebar_last_draw >= 0.08:
            self._sidebar_last_draw = now
            self.layout()
        else:
            # between redraws of the chart the panel still follows the mouse
            w, h = self.GetClientSize()
            self.sidebar.SetSize(w - width, 0, width, h)

    def onFrameSize(self, event):
        self.layout()

    def onSidebar(self, event):
        tradoptions.set({'show_sidebar': self.msidebar.IsChecked()})
        if self.options.autosave:
            tradoptions.save()
        self.layout()

    def onPopupMenu(self, event):
        self.PopupMenu(self.pmenu, event.GetPosition())

    def onChart(self, event):
        if self.selection != TransitFrame.CHART:
            self.selection = TransitFrame.CHART
            self.w.Destroy()
            self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, False, -1, self.GetClientSize())
            self.layout()

    def onComparison(self, event):
        if self.selection != TransitFrame.COMPOUND:
            self.selection = TransitFrame.COMPOUND
            self.w.Destroy()
            self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, True, -1, self.GetClientSize())
            self.layout()

    def onPositions(self, event):
        if self.selection != TransitFrame.POSITIONS:
            self.selection = TransitFrame.POSITIONS
            self.w.Destroy()
            if wx.Platform == '__WXMSW__':
                self.w = positionswnd2.PositionsWnd2(self, self.chart, self.options, self.parent, -1, self.GetClientSize())
                self.layout()
                self.w.Refresh()
            else:
                self.w = positionswnd.PositionsWnd(self, self.chart, self.options, self.parent, -1, self.GetClientSize())
                self.layout()

    def onSquare(self, event):
        if self.selection != TransitFrame.SQUARE:
            self.selection = TransitFrame.SQUARE
            self.w.Destroy()
            self.w = squarechartwnd.SquareChartWnd(self, self.chart, self.options, self.parent, -1, self.GetClientSize())
            self.layout()

    def onStep(self, event):
        if self.chart.htype in (chart.Chart.SOLAR, chart.Chart.LUNAR):
            dlg = returnstepperdlg.ReturnStepperDlg(self, self.radix)
        else:
            dlg = electionstepperdlg.ElectionStepperDlg(self, self.chart, self.options, self.title)
        dlg.CenterOnParent()
        dlg.Show(True)

    def onKey(self, event):
        """Left/Right: previous/next return; for transits a day (Shift: an hour,
        Ctrl: a month, Ctrl+Shift: a year)."""
        key = event.GetKeyCode()
        if key not in (wx.WXK_LEFT, wx.WXK_RIGHT) or event.AltDown():
            event.Skip()
            return
        if self.stepper is not None:
            self.stepTo(key == wx.WXK_RIGHT)
            return
        forward = key == wx.WXK_RIGHT
        wait = wx.BusyCursor()
        if self.chart.htype in (chart.Chart.SOLAR, chart.Chart.LUNAR):
            chrt = returnslist.step_return(self.radix, self.chart, forward)
            if chrt is not None:
                self.change(chrt)
            return
        t = self.chart.time
        y, m, d, h = t.origyear, t.origmonth, t.origday, t.hour
        if event.ControlDown() and event.ShiftDown():
            y += 1 if forward else -1
        elif event.ControlDown():
            y, m = util.incrMonth(y, m) if forward else util.decrMonth(y, m)
        elif event.ShiftDown():
            y, m, d, h = util.addHour(y, m, d, h) if forward else util.subtractHour(y, m, d, h)
        else:
            y, m, d = util.incrDay(y, m, d) if forward else util.decrDay(y, m, d)
        while d > 28 and not util.checkDate(y, m, d):	# e.g. a month after 31 January
            d -= 1
        time = chart.Time(y, m, d, h, t.minute, t.second, t.bc, t.cal, t.zt, t.plus, t.zh, t.zm, t.daylightsaving, self.chart.place)
        self.change(chart.Chart(self.chart.name, self.chart.male, time, self.chart.place, chart.Chart.TRANSIT, '', self.options, False))

    def stepTo(self, forward):
        wait = wx.BusyCursor()
        chrt = self.stepper(self.chart, forward)
        if chrt is not None:
            self.change(chrt)
            if chrt.notes:	# e.g. 'Full Moon'
                self.SetTitle(self.title + ' \u2014 ' + chrt.notes)

    def change(self, chrt, title=None):
        """Shows another chart (used by the steppers), keeping the current view."""
        self.chart = chrt
        view = self.selection
        self.selection = -1
        {TransitFrame.CHART: self.onChart, TransitFrame.COMPOUND: self.onComparison,
         TransitFrame.POSITIONS: self.onPositions, TransitFrame.SQUARE: self.onSquare}[view](None)
        self.sidebar.setChart(self.chart, self.radix)

    def onPDDirect(self, event):
        self.onPD(primdirs.PrimDirs.DIRECT)

    def onPDConverse(self, event):
        self.onPD(primdirs.PrimDirs.CONVERSE)

    def onPDRadix(self, event):
        pass

    def onDivisions(self, event):
        try:
            frame = divisionswnd.DivisionsFrame(self, self.title, self.radix, self.chart, self.options)
            frame.Show(True)
        except (ValueError, OverflowError) as exc:
            wx.MessageBox(str(exc), i18n.tr('Divisions (Valens)'), wx.OK | wx.ICON_WARNING, self)

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
        self.progbar = wx.ProgressDialog(i18n.tr(mtexts.txtscommon['Calculating']), i18n.tr(txt), parent=self, style=wx.PD_CAN_ABORT | wx.PD_APP_MODAL)
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
            self.pds = placidianutppd.PlacidianUTPPD(self.chart, self.options, pdrange, direction, self.abort)
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
            dlgm = wx.MessageDialog(self, i18n.tr(mtexts.txtscommon['NoPDsWithSettings']), i18n.tr(mtexts.txtscommon['Information']), wx.OK | wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()
        if self.pds != None:
            del self.pds
        del self.abort
        return
