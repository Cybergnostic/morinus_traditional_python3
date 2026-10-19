# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import chart
import positionswnd
import positionswnd2
import transitwnd
import squarechartwnd
import mtexts

class PDsInChartFrame(wx.Frame):
    XSIZE = 512
    YSIZE = 512
    CHART = 0
    COMPOUND = 1
    POSITIONS = 2
    SQUARE = 3

    def __init__(self, parent, title, chrt, radix, options, sel=0):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(PDsInChartFrame.XSIZE, PDsInChartFrame.YSIZE))
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
        self.selmenu = wx.Menu()
        self.chartmenu = self.selmenu.Append(self.ID_Chart, mtexts.txtspopupmenu['Chart'], '', wx.ITEM_RADIO)
        self.compoundmenu = self.selmenu.Append(self.ID_Comparison, mtexts.txtspopupmenu['Comparison'], '', wx.ITEM_RADIO)
        self.positionsmenu = self.selmenu.Append(self.ID_Positions, mtexts.txtspopupmenu['Positions'], '', wx.ITEM_RADIO)
        self.squaremenu = self.selmenu.Append(self.ID_Square, mtexts.txtspopupmenu['Square'], '', wx.ITEM_RADIO)
        self.pmenu.Append(wx.MenuItem(self.pmenu, self.ID_Selection, mtexts.txtspopupmenu['Windows'], subMenu=self.selmenu))
        self.pmenu.Append(self.ID_SaveAsBitmap, mtexts.txtspopupmenu['SaveAsBmp'], mtexts.txtspopupmenu['SaveChart'])
        self.mbw = self.pmenu.Append(self.ID_BlackAndWhite, mtexts.txtspopupmenu['BlackAndWhite'], mtexts.txtspopupmenu['ChartBW'], wx.ITEM_CHECK)
        self.SetMinSize((200, 200))
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_MENU, self.onChart, id=self.ID_Chart)
        self.Bind(wx.EVT_MENU, self.onComparison, id=self.ID_Comparison)
        self.Bind(wx.EVT_MENU, self.onPositions, id=self.ID_Positions)
        self.Bind(wx.EVT_MENU, self.onSquare, id=self.ID_Square)
        self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
        self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)
        if self.options.bw:
            self.mbw.Check()
        self.selection = sel
        if sel == PDsInChartFrame.CHART:
            self.w = transitwnd.TransitWnd(self, self.chart, radix, options, parent)
            self.chartmenu.Check()
        else:
            self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, True)
            self.compoundmenu.Check()

    def onPopupMenu(self, event):
        self.PopupMenu(self.pmenu, event.GetPosition())

    def onChart(self, event):
        if self.selection != PDsInChartFrame.CHART:
            self.selection = PDsInChartFrame.CHART
            self.w.Destroy()
            self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, False, -1, self.GetClientSize())

    def onComparison(self, event):
        if self.selection != PDsInChartFrame.COMPOUND:
            self.selection = PDsInChartFrame.COMPOUND
            self.w.Destroy()
            self.w = transitwnd.TransitWnd(self, self.chart, self.radix, self.options, self.parent, True, -1, self.GetClientSize())

    def onPositions(self, event):
        if self.selection != PDsInChartFrame.POSITIONS:
            self.selection = PDsInChartFrame.POSITIONS
            self.w.Destroy()
            if wx.Platform == '__WXMSW__':
                self.w = positionswnd2.PositionsWnd2(self, self.chart, self.options, self.parent, -1, self.GetClientSize())
                self.w.Refresh()
            else:
                self.w = positionswnd.PositionsWnd(self, self.chart, self.options, self.parent, -1, self.GetClientSize())

    def onSquare(self, event):
        if self.selection != PDsInChartFrame.SQUARE:
            self.selection = PDsInChartFrame.SQUARE
            self.w.Destroy()
            self.w = squarechartwnd.SquareChartWnd(self, self.chart, self.options, self.parent, -1, self.GetClientSize())

    def change(self, chrt, y, m, d, ho, mi, se, pdtypetxt, pdkeytxt, txtdir, da):
        self.chart = chrt
        self.w.chart = chrt
        self.w.drawBkg()
        self.w.Refresh()
        txt = pdtypetxt + ' ' + pdkeytxt + ' ' + txtdir + ' ' + str(y) + '.' + str(m).zfill(2) + '.' + str(d).zfill(2) + ' ' + str(ho).zfill(2) + ':' + str(mi).zfill(2) + ':' + str(se).zfill(2) + '  ' + str(da)
        self.SetTitle(txt)

    def onSaveAsBitmap(self, event):
        self.w.onSaveAsBitmap(event)

    def onBlackAndWhite(self, event):
        self.w.onBlackAndWhite(event)