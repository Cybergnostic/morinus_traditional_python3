# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
import wx
import antisciawnd

class AntisciaFrame(wx.Frame):
    XSIZE = 570
    YSIZE = 450

    def __init__(self, parent, title, chrt, options):
        wx.Frame.__init__(self, parent, -1, i18n.tr(title), wx.DefaultPosition, wx.Size(AntisciaFrame.XSIZE, AntisciaFrame.YSIZE))
        self.w = antisciawnd.AntisciaWnd(self, chrt, options, parent)
        # wide enough for the columns of planets on the antiscia
        self.SetSize((min(self.w.WIDTH + 30, 1600), AntisciaFrame.YSIZE))
        self.SetMinSize((200, 200))