# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import os
import chart
import graphchart
import mtexts

class TransitWnd(wx.Window):

    def __init__(self, parent, chrt, radix, options, mainfr, compound=False, id=-1, size=wx.DefaultSize):
        wx.Window.__init__(self, parent, id, wx.DefaultPosition, size=size)
        self.parent = parent
        self.chart = chrt
        self.radix = radix
        self.options = options
        self.mainfr = mainfr
        self.compound = compound
        self.bw = self.options.bw
        self.SetMinSize((200, 200))
        self.parent.mbw.Check(self.bw)
        self.SetBackgroundColour(self.options.clrbackground)
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.clickedPlId = None
        self.drawBkg()
        return

    def drawBkg(self):
        self.gchart = None
        if self.compound:
            self.gchart = graphchart.GraphChart(self.radix, self.GetClientSize(), self.options, self.bw, self.clickedPlId, self.chart)
        else:
            self.gchart = graphchart.GraphChart(self.chart, self.GetClientSize(), self.options, self.bw, self.clickedPlId)
        self.buffer = self.gchart.drawChart()
        self.Refresh()
        return

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

    def onPopupMenu(self, event):
        self.parent.onPopupMenu(event)

    def onSaveAsBitmap(self, event):
        name = self.chart.name + mtexts.typeList[self.chart.htype][0:3].capitalize()
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

    def onLeftUp(self, event):
        if self.options.enableclick:
            self.clickedPlId = self.gchart.onClick(event.GetPosition())
            self.drawBkg()