# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import os, wx, mtexts

class CommonWnd(wx.ScrolledWindow):
    SCROLL_RATE = 20
    BORDER = 20

    def __init__(self, parent, chrt, options, id=-1, size=wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)
        self.parent = parent
        self.chart = chrt
        self.options = options
        self.bw = self.options.bw
        self.SetBackgroundColour(self.options.clrbackground)
        self.SetScrollRate(CommonWnd.SCROLL_RATE, CommonWnd.SCROLL_RATE)
        self.pmenu = wx.Menu()
        self.ID_SaveAsBitmap = wx.NewId()
        self.ID_BlackAndWhite = wx.NewId()
        self.pmenu.Append(self.ID_SaveAsBitmap, mtexts.txtspopupmenu['SaveAsBmp'], mtexts.txtspopupmenu['SaveTable'])
        mbw = self.pmenu.Append(self.ID_BlackAndWhite, mtexts.txtspopupmenu['BlackAndWhite'], mtexts.txtspopupmenu['TableBW'], wx.ITEM_CHECK)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
        self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)
        if self.bw:
            mbw.Check()

    def onPopupMenu(self, event):
        self.PopupMenu(self.pmenu, event.GetPosition())

    def onSaveAsBitmap(self, event):
        name = self.chart.name + self.getExt()
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

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)