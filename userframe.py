# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx, userwnd, mtexts

class UserFrame(wx.Frame):
    XSIZE = 640
    YSIZE = 400

    def __init__(self, parent, title, chrt, options, usr):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(UserFrame.XSIZE, UserFrame.YSIZE))
        self.w = userwnd.UserWnd(self, chrt, options, parent, usr)
        self.SetMinSize((200, 200))