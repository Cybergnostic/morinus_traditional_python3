# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import hourswnd

class HoursFrame(wx.Frame):
    XSIZE = 320
    YSIZE = 480

    def __init__(self, parent, title, chrt, options):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(HoursFrame.XSIZE, HoursFrame.YSIZE))
        sw = hourswnd.HoursWnd(self, chrt, options, parent)
        self.SetMinSize((200, 200))