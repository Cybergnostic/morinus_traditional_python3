# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import i18n
import wx
import menubars
import positionswnd
import mtexts

class PositionsFrame(wx.Frame):
    XSIZE = 590
    YSIZE = 512

    def __init__(self, parent, title, chrt, options, speculum_index=None, userpoint=None):
        wx.Frame.__init__(self, parent, -1, i18n.tr(title), wx.DefaultPosition, wx.Size(PositionsFrame.XSIZE, PositionsFrame.YSIZE))
        self.pmenu = wx.Menu()
        menubars.later(self, 'Table')
        self.ID_SaveAsBitmap = wx.NewId()
        self.ID_BlackAndWhite = wx.NewId()
        self.pmenu.Append(self.ID_SaveAsBitmap, i18n.tr(mtexts.txtspopupmenu['SaveAsBmp']), i18n.tr(mtexts.txtspopupmenu['SaveTable']))
        self.mbw = self.pmenu.Append(self.ID_BlackAndWhite, i18n.tr(mtexts.txtspopupmenu['BlackAndWhite']), i18n.tr(mtexts.txtspopupmenu['TableBW']), wx.ITEM_CHECK)
        self.w = positionswnd.PositionsWnd(self, chrt, options, parent, speculum_index=speculum_index, userpoint=userpoint)
        self.SetMinSize((200, 200))
        self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
        self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)
        if options.bw:
            self.mbw.Check()

    def onPopupMenu(self, event):
        self.PopupMenu(self.pmenu, event.GetPosition())

    def onSaveAsBitmap(self, event):
        self.w.onSaveAsBitmap(event)

    def onBlackAndWhite(self, event):
        self.w.onBlackAndWhite(event)