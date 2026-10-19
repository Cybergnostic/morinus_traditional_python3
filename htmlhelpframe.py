# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import wx
import wx.html

class HtmlHelpFrame(wx.Frame):
    XSIZE = 640
    YSIZE = 400

    def __init__(self, parent, id, title, fname):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(HtmlHelpFrame.XSIZE, HtmlHelpFrame.YSIZE))
        self.myhtml = wx.html.HtmlWindow(self, id)
        self.myhtml.LoadPage(fname)