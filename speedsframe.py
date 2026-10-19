# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, speedswnd

class SpeedsFrame(wx.Frame):
    XSIZE = 330
    YSIZE = 310

    def __init__(self, parent, title, chrt, options):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(SpeedsFrame.XSIZE, SpeedsFrame.YSIZE))
        sw = speedswnd.SpeedsWnd(self, chrt, options, parent)
        self.SetMinSize((200, 200))