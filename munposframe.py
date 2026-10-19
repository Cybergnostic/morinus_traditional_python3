# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, munposwnd

class MunPosFrame(wx.Frame):
    XSIZE = 640
    YSIZE = 480

    def __init__(self, parent, title, chrt, options):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(MunPosFrame.XSIZE, MunPosFrame.YSIZE))
        sw = munposwnd.MunPosWnd(self, chrt, options, parent)
        self.SetMinSize((200, 200))