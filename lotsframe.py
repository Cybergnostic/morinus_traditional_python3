# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import lotswnd

class LotsFrame(wx.Frame):
    XSIZE = 640
    YSIZE = 512

    def __init__(self, parent, title, chrt, options):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(LotsFrame.XSIZE, LotsFrame.YSIZE))
        bar = wx.Panel(self)
        barsizer = wx.BoxSizer(wx.HORIZONTAL)
        barsizer.Add(wx.StaticText(bar, -1, 'Formulas:'), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.sectcb = wx.Choice(bar, -1, choices=['Day', 'Night'])
        barsizer.Add(self.sectcb, 0, wx.ALL, 3)
        bar.SetSizer(barsizer)
        self.sw = lotswnd.LotsWnd(self, chrt, options, parent)
        # opens on the chart's sect; the other choice shows the lots as computed for the other sect
        self.sectcb.SetSelection(1 if self.sw.night else 0)
        self.sectcb.Bind(wx.EVT_CHOICE, self.onSect)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(bar, 0, wx.EXPAND)
        sizer.Add(self.sw, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetMinSize((200, 200))

    def onSect(self, event):
        self.sw.setNight(self.sectcb.GetSelection() == 1)