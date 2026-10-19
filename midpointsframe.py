# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, midpointswnd

class MidPointsFrame(wx.Frame):
    XSIZE = 640
    YSIZE = 512

    def __init__(self, parent, title, chrt, options):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(MidPointsFrame.XSIZE, MidPointsFrame.YSIZE))
        sw = midpointswnd.MidPointsWnd(self, chrt, options, parent)
        self.SetMinSize((200, 200))