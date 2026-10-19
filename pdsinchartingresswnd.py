# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, os, chart, graphchartpds, mtexts

class PDsInChartIngressWnd(wx.Window):

    def __init__(self, parent, chartRadix, chartPDs, chartIngress, options, mainfr, id=-1, size=wx.DefaultSize):
        wx.Window.__init__(self, parent, id, wx.DefaultPosition, size=size)
        self.parent = parent
        self.chartRadix = chartRadix
        self.chartPDs = chartPDs
        self.chartIngress = chartIngress
        self.options = options
        self.mainfr = mainfr
        self.bw = self.options.bw
        self.SetMinSize((200, 200))
        self.parent.mbw.Check(self.bw)
        self.SetBackgroundColour(self.options.clrbackground)
        self.drawBkg()
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)

    def drawBkg(self):
        gchart = graphchartpds.GraphChartPDs(self.chartRadix, self.chartPDs, self.chartIngress, self.GetClientSize(), self.options, self.bw)
        self.buffer = gchart.drawChart()
        self.Refresh()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

    def onPopupMenu(self, event):
        self.parent.onPopupMenu(event)

    def onSaveAsBitmap(self, event):
        name = self.chartRadix.name + mtexts.txtspdsinchartoptsdlg['PDsInChart']
        dlg = wx.FileDialog(self, mtexts.txtsfiles['SaveAsBmp'], '', name, mtexts.txtsfiles['BMPFiles'], wx.FD_SAVE)
        if os.path.isdir(self.mainfr.fpathimgs):
            dlg.SetDirectory(self.mainfr.fpathimgs)
        else:
            dlg.SetDirectory(u'.')
        if dlg.ShowModal() == wx.ID_OK:
            dpath = dlg.GetDirectory()
            fpath = dlg.GetPath()
            if not fpath.endswith(u'.png'):
                fpath += u'.png'
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