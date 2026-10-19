# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import zodparswnd

class ZodParsFrame(wx.Frame):
    XSIZE = 580
    YSIZE = 310

    def __init__(self, parent, title, chrt, options):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(ZodParsFrame.XSIZE, ZodParsFrame.YSIZE))
        self.w = zodparswnd.ZodParsWnd(self, chrt, options, parent)
        self.SetMinSize((200, 200))