# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, risesetwnd

class RiseSetFrame(wx.Frame):
    XSIZE = 500
    YSIZE = 500

    def __init__(self, parent, title, chrt, options):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(RiseSetFrame.XSIZE, RiseSetFrame.YSIZE))
        rw = risesetwnd.RiseSetWnd(self, chrt, options, parent)
        self.SetMinSize((200, 200))