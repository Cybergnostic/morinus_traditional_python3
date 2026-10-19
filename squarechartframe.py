# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import squarechartwnd
import mtexts

class SquareChartFrame(wx.Frame):
    XSIZE = 512
    YSIZE = 512

    def __init__(self, parent, title, chrt, opts):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(SquareChartFrame.XSIZE, SquareChartFrame.YSIZE))
        self.chart = chrt
        self.options = opts
        self.parent = parent
        self.pmenu = wx.Menu()
        self.ID_SaveAsBitmap = wx.NewId()
        self.ID_BlackAndWhite = wx.NewId()
        self.pmenu.Append(self.ID_SaveAsBitmap, mtexts.txtspopupmenu['SaveAsBmp'], mtexts.txtspopupmenu['SaveChart'])
        self.mbw = self.pmenu.Append(self.ID_BlackAndWhite, mtexts.txtspopupmenu['BlackAndWhite'], mtexts.txtspopupmenu['ChartBW'], wx.ITEM_CHECK)
        self.w = squarechartwnd.SquareChartWnd(self, self.chart, opts, parent)
        self.SetMinSize((200, 200))
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
        self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)
        if self.options.bw:
            self.mbw.Check()

    def onPopupMenu(self, event):
        self.PopupMenu(self.pmenu, event.GetPosition())

    def onSaveAsBitmap(self, event):
        self.w.onSaveAsBitmap(event)

    def onBlackAndWhite(self, event):
        self.w.onBlackAndWhite(event)