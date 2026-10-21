"""Tabbed Positions workspace using Morinus's unchanged specialist table views.

The underlying zodiacal speculum, mundane positions, motion and miscellaneous
calculations remain in their original modules. The window is the shared
legacytabworkspace.TableWorkspace; the speculum tab adds the choice between the
Placidian and Regiomontanian speculum (without changing the primary-directions
settings) and the columns of Appearance II.
"""
import wx
import positionswnd
import positionsframe
import munposwnd
import munposframe
import speedswnd
import speedsframe
import miscwnd
import miscframe
import mtexts
import primdirs
import positionscatalog
import legacytabworkspace


TABS = positionscatalog.TABS
DESCRIPTIONS = positionscatalog.DESCRIPTIONS
SPECULUMS = ('Placidian speculum', 'Regiomontanian speculum')


def initial_speculum(options):
    return positionscatalog.initial_speculum(options.primarydir,
                                             primdirs.PrimDirs.REGIOMONTAN)


def has_columns(options, method):
    return positionscatalog.has_columns(options.speculums, method)


class _NoCheck:
    """PositionsWnd checks its parent's B/W menu item; the workspace menu shows it instead."""
    def Check(self, *args):
        pass


class SpeculumPanel(wx.Panel):
    """The Zodiacal / speculum tab: the chosen speculum with its columns."""

    def __init__(self, parent, chart, options, mainfr):
        super().__init__(parent)
        self.chart, self.options, self.mainfr = chart, options, mainfr
        self.method = initial_speculum(options)
        self.view = None
        self.choice = wx.Choice(self, -1, choices=list(SPECULUMS))
        self.choice.SetSelection(self.method)
        self.choice.SetToolTip('Change the table, not the primary-directions settings')
        self.choice.Bind(wx.EVT_CHOICE, lambda e: self.setMethod(self.choice.GetSelection()))
        configure = wx.Button(self, -1, 'Configure columns...')
        configure.SetToolTip('Choose the speculum columns (Appearance II)')
        configure.Bind(wx.EVT_BUTTON, self.onConfigure)
        selector = wx.BoxSizer(wx.HORIZONTAL)
        selector.Add(wx.StaticText(self, -1, 'Speculum method:'), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        selector.Add(self.choice, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 12)
        selector.Add(configure, 0, wx.ALIGN_CENTER_VERTICAL)
        # PositionsWnd reads parent.mbw and calls parent.onPopupMenu
        self.area = wx.Panel(self)
        self.area.mbw = _NoCheck()
        self.area.onPopupMenu = self.onPopupMenu
        self.area.SetSizer(wx.BoxSizer(wx.VERTICAL))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(selector, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.area, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.build()

    def build(self):
        """The view of the chosen method, as the options are now."""
        bw = getattr(self.view, 'bw', self.options.bw)
        if self.view is not None:
            self.view.Destroy()
        if has_columns(self.options, self.method):
            self.view = positionswnd.PositionsWnd(self.area, self.chart, self.options, self.mainfr, speculum_index=self.method)
            if self.view.bw != bw:
                self.view.bw = bw
                self.view.drawBkg()
        else:
            self.view = wx.StaticText(self.area, -1, '\n  No columns are selected for this speculum: choose them with Configure columns.')
        self.area.GetSizer().Add(self.view, 1, wx.EXPAND)
        self.area.Layout()
        workspace = self.GetTopLevelParent()
        if 0 in getattr(workspace, 'views', {}):
            workspace.updateMenu()

    def setMethod(self, method):
        self.method = method
        self.choice.SetSelection(method)
        self.build()

    def onConfigure(self, event):
        # Changing Appearance II closes the main window's tables; keep this one
        # open and rebuild its speculum instead.
        workspace = self.GetTopLevelParent()
        self.mainfr.keep_open = (workspace,)
        try:
            self.mainfr.onAppearance2(wx.CommandEvent())
        finally:
            self.mainfr.keep_open = ()
        if self:
            self.build()

    def onPopupMenu(self, event):
        menu = wx.Menu()
        for label, method in (('Save table as image...', 'onSaveAsBitmap'), ('Copy table as text', 'onCopyAsText'),
                              ('Copy table as image', 'onCopyAsImage'), ('Export as CSV...', 'onExportCSV')):
            item = menu.Append(wx.ID_ANY, label)
            self.Bind(wx.EVT_MENU, lambda e, m=method: self.forward(m, e), id=item.GetId())
        self.PopupMenu(menu)
        menu.Destroy()

    def forward(self, method, event):
        callback = getattr(self.view, method, None)
        if callback is not None:
            callback(event)

    # the commands of the workspace's Table menu
    def onSaveAsBitmap(self, event):
        self.forward('onSaveAsBitmap', event)

    def onCopyAsText(self, event):
        self.forward('onCopyAsText', event)

    def onCopyAsImage(self, event):
        self.forward('onCopyAsImage', event)

    def onExportCSV(self, event):
        self.forward('onExportCSV', event)

    def onBlackAndWhite(self, event):
        self.forward('onBlackAndWhite', event)

    @property
    def bw(self):
        return getattr(self.view, 'bw', self.options.bw)


def _open_speculum(mainfr, chart, options, panel):
    method = panel.method if panel is not None else initial_speculum(options)
    if not has_columns(options, method):
        wx.MessageBox(mtexts.txtspositions['SelectColumn'], 'Positions', wx.OK | wx.ICON_INFORMATION, parent=mainfr)
        return None
    frame = positionsframe.PositionsFrame(mainfr, mainfr.title, chart, options, speculum_index=method)
    frame.Show()
    return frame


def _open(frameclass, mainfr, chart, options):
    frame = frameclass(mainfr, mainfr.title, chart, options)
    frame.Show()
    return frame


def show(mainfr, tab=0):
    """Reuse an open workspace; old table commands become tab aliases."""
    wnd = getattr(mainfr, 'positions_workspace', None)
    if wnd:
        wnd.selectTab(tab)
    else:
        chart, options = mainfr.horoscope, mainfr.options
        specs = (
            (TABS[0], DESCRIPTIONS[0], lambda page: SpeculumPanel(page, chart, options, mainfr),
             lambda view: _open_speculum(mainfr, chart, options, view)),
            (TABS[1], DESCRIPTIONS[1], lambda page: munposwnd.MunPosWnd(page, chart, options, mainfr),
             lambda view: _open(munposframe.MunPosFrame, mainfr, chart, options)),
            (TABS[2], DESCRIPTIONS[2], lambda page: speedswnd.SpeedsWnd(page, chart, options, mainfr),
             lambda view: _open(speedsframe.SpeedsFrame, mainfr, chart, options)),
            (TABS[3], DESCRIPTIONS[3], lambda page: miscwnd.MiscWnd(page, chart, options, mainfr),
             lambda view: _open(miscframe.MiscFrame, mainfr, chart, options)),
        )
        wnd = legacytabworkspace.TableWorkspace(mainfr, 'Positions and data — ' + chart.name, specs, tab,
                                                size=(1110, 730), attribute='positions_workspace')
        mainfr.positions_workspace = wnd
    wnd.Show(True)
    wnd.Raise()
    return wnd
