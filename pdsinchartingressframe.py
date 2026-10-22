# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
import wx
import menubars
import chart
import pdsinchartingresswnd
import mtexts

class PDsInChartIngressFrame(wx.Frame):
    XSIZE = 512
    YSIZE = 512

    def __init__(self, parent, title, radix, pdchart, ingchart, options):
        wx.Frame.__init__(self, parent, -1, i18n.tr(title), wx.DefaultPosition, wx.Size(PDsInChartIngressFrame.XSIZE, PDsInChartIngressFrame.YSIZE))
        self.chartRadix = radix
        self.chartPDs = pdchart
        self.chartIngress = ingchart
        self.options = options
        self.parent = parent
        self.title = title
        self.pmenu = wx.Menu()
        menubars.later(self, 'Chart')
        self.ID_SaveAsBitmap = wx.NewId()
        self.ID_BlackAndWhite = wx.NewId()
        self.pmenu.Append(self.ID_SaveAsBitmap, i18n.tr(mtexts.txtspopupmenu['SaveAsBmp']), i18n.tr(mtexts.txtspopupmenu['SaveChart']))
        self.mbw = self.pmenu.Append(self.ID_BlackAndWhite, i18n.tr(mtexts.txtspopupmenu['BlackAndWhite']), i18n.tr(mtexts.txtspopupmenu['ChartBW']), wx.ITEM_CHECK)
        self.SetMinSize((200, 200))
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
        self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)
        if self.options.bw:
            self.mbw.Check()
        self.w = pdsinchartingresswnd.PDsInChartIngressWnd(self, self.chartRadix, self.chartPDs, self.chartIngress, self.options, self.parent)

    def change(self, chrt, y, m, d, ho, mi, se, pdtypetxt, pdkeytxt, txtdir, da):
        self.chartPDs = chrt
        self.w.chartPDs = chrt
        tim = chart.Time(y, m, d, ho, mi, se, self.chartRadix.time.bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, self.chartRadix.place)
        chrtIng = chart.Chart(self.chartRadix.name, self.chartRadix.male, tim, self.chartRadix.place, chart.Chart.PDINCHART, '', self.options, False)
        self.chartIngress = chrtIng
        self.w.chartIngress = chrtIng
        self.w.drawBkg()
        self.w.Refresh()
        txt = pdtypetxt + ' ' + pdkeytxt + ' ' + txtdir + ' ' + str(y) + '.' + str(m).zfill(2) + '.' + str(d).zfill(2) + ' ' + str(ho).zfill(2) + ':' + str(mi).zfill(2) + ':' + str(se).zfill(2) + '  ' + str(da)
        self.SetTitle(i18n.tr(txt))

    def onPopupMenu(self, event):
        self.PopupMenu(self.pmenu, event.GetPosition())

    def onSaveAsBitmap(self, event):
        self.w.onSaveAsBitmap(event)

    def onBlackAndWhite(self, event):
        self.w.onBlackAndWhite(event)