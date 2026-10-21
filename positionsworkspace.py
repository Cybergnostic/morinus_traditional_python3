"""Tabbed Positions workspace using Morinus's unchanged specialist table views.

The underlying zodiacal speculum, mundane positions, motion and miscellaneous
calculations remain in their original modules. This window only owns navigation,
toolbar actions and backwards-compatible standalone-window access.
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


TABS = ('Zodiacal / speculum', 'Mundane', 'Motion', 'Chart data')
DESCRIPTIONS = (
    'Zodiacal positions and the full Placidus or Regiomontanus speculum. '
    'The chosen columns are controlled by Appearance II.',
    'Mundane house positions and the mundane Lot of Fortune.',
    'Longitude and latitude speeds of the planets.',
    'Sidereal time, obliquity of the ecliptic, and Julian day.',
)
SPECULUMS = ('Placidian speculum', 'Regiomontanian speculum')


def initial_speculum(options):
    """Default to the method used by the legacy Positions window."""
    return int(options.primarydir == primdirs.PrimDirs.REGIOMONTAN)


def has_columns(options, method):
    """Keep the original guard against an empty specialist table."""
    return method in (0, 1) and any(options.speculums[method])


class PositionsWorkspace(wx.Frame):
    """An alternative way to browse the ORIGINAL four table renderers."""

    def __init__(self, mainfr, title, chart, options, tab=0):
        super().__init__(mainfr, -1, 'Positions workspace — ' + chart.name,
                         size=(1110, 730), style=wx.DEFAULT_FRAME_STYLE)
        self.mainfr = mainfr
        self.chart = chart
        self.options = options
        self.SetMinSize((700, 450))
        self.views = {}
        self.spec_views = {}
        self.spec_method = initial_speculum(options)
        self.configureMenu()

        self.notebook = wx.Notebook(self)
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChanged)

        # Pages have their own parent to retain the original table window's
        # parent.mbw and parent.onPopupMenu compatibility.
        self.pages = [wx.Panel(self.notebook) for _ in TABS]
        for page in self.pages:
            page.mbw = self.mbw
            page.onPopupMenu = self.onPositionsPopup

        self.makeSpeculumPage(self.pages[0])
        constructors = (munposwnd.MunPosWnd, speedswnd.SpeedsWnd, miscwnd.MiscWnd)
        for index, cls in enumerate(constructors, 1):
            page = self.pages[index]
            layout = wx.BoxSizer(wx.VERTICAL)
            view = cls(page, chart, options, mainfr)
            layout.Add(view, 1, wx.EXPAND)
            page.SetSizer(layout)
            self.views[index] = view

        for index, page in enumerate(self.pages):
            self.notebook.AddPage(page, TABS[index])

        self.intro = wx.StaticText(self, -1, '')
        self.intro.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
        self.separate = wx.Button(self, -1, 'Open separately')
        self.separate.SetToolTip('Open the original, independent Morinus table window')
        self.separate.Bind(wx.EVT_BUTTON, self.onOpenSeparate)

        bottom = wx.BoxSizer(wx.HORIZONTAL)
        bottom.Add(self.intro, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 12)
        bottom.Add(self.separate, 0)
        outer = wx.BoxSizer(wx.VERTICAL)
        outer.Add(self.notebook, 1, wx.EXPAND)
        outer.Add(bottom, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(outer)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.selectTab(tab)

    def configureMenu(self):
        menu = wx.Menu()
        self.ID_SaveImage = wx.NewIdRef()
        self.ID_CopyText = wx.NewIdRef()
        self.ID_CopyImage = wx.NewIdRef()
        self.ID_ExportCSV = wx.NewIdRef()
        self.ID_BW = wx.NewIdRef()
        self.ID_Separate = wx.NewIdRef()
        self.ID_Close = wx.NewIdRef()
        menu.Append(self.ID_SaveImage, 'Save table as image...')
        menu.Append(self.ID_CopyText, 'Copy table as text')
        menu.Append(self.ID_CopyImage, 'Copy table as image')
        menu.Append(self.ID_ExportCSV, 'Export table as CSV...')
        menu.AppendSeparator()
        self.mbw = menu.AppendCheckItem(self.ID_BW, 'Black and white')
        menu.AppendSeparator()
        menu.Append(self.ID_Separate, 'Open this table separately')
        menu.Append(self.ID_Close, 'Close workspace')
        self.mbw.Check(self.options.bw)
        menubar = wx.MenuBar()
        menubar.Append(menu, 'Table')
        self.SetMenuBar(menubar)
        self.positions_popup = wx.Menu()
        self.positions_popup.Append(self.ID_SaveImage, 'Save table as image...')
        self.positions_popup.AppendSeparator()
        self.positions_popup.Append(self.ID_Separate, 'Open separately')

        self.Bind(wx.EVT_MENU, self.onSaveImage, id=self.ID_SaveImage)
        self.Bind(wx.EVT_MENU, self.onCopyText, id=self.ID_CopyText)
        self.Bind(wx.EVT_MENU, self.onCopyImage, id=self.ID_CopyImage)
        self.Bind(wx.EVT_MENU, self.onExportCSV, id=self.ID_ExportCSV)
        self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BW)
        self.Bind(wx.EVT_MENU, self.onOpenSeparate, id=self.ID_Separate)
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), id=self.ID_Close)

    def makeSpeculumPage(self, page):
        selector = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(page, -1, 'Speculum method:')
        self.choice = wx.Choice(page, -1, choices=list(SPECULUMS))
        self.choice.SetSelection(self.spec_method)
        self.choice.SetToolTip('Change the table, not the primary-directions settings')
        self.choice.Bind(wx.EVT_CHOICE, self.onMethodChanged)
        settings = wx.Button(page, -1, 'Configure columns...')
        settings.SetToolTip('Use Appearance II to choose speculum columns')
        settings.Bind(wx.EVT_BUTTON, lambda event: self.mainfr.onAppearance2(wx.CommandEvent()))
        selector.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        selector.Add(self.choice, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 12)
        selector.Add(settings, 0, wx.ALIGN_CENTER_VERTICAL)

        container = wx.BoxSizer(wx.VERTICAL)
        container.Add(selector, 0, wx.EXPAND | wx.ALL, 10)
        self.spec_area = wx.Panel(page)
        self.spec_stack = wx.BoxSizer(wx.VERTICAL)
        for method in range(2):
            if has_columns(self.options, method):
                view = positionswnd.PositionsWnd(self.spec_area, self.chart, self.options,
                                                 self.mainfr, speculum_index=method)
            else:
                view = wx.StaticText(self.spec_area, -1,
                    'No columns selected for this speculum. Choose Configure columns to select them.')
            # The legacy PositionsWnd needs the popup and B&W controls on its parent.
            # Here the container is a panel rather than a standalone frame.
            self.spec_views[method] = view
            self.spec_stack.Add(view, 1, wx.EXPAND)
            view.Show(method == self.spec_method)
        self.spec_area.SetSizer(self.spec_stack)
        # PositionsWnd's direct parent is spec_area, not the Notebook page.
        self.spec_area.mbw = self.mbw
        self.spec_area.onPopupMenu = self.onPositionsPopup
        container.Add(self.spec_area, 1, wx.EXPAND)
        page.SetSizer(container)

    def onMethodChanged(self, event):
        self.spec_method = self.choice.GetSelection()
        for method, view in self.spec_views.items():
            view.Show(method == self.spec_method)
        self.spec_area.Layout()
        self.pages[0].Layout()
        self.syncMenu()

    def activeView(self):
        tab = self.notebook.GetSelection()
        return self.spec_views.get(self.spec_method) if tab == 0 else self.views.get(tab)

    def selectTab(self, tab):
        index = max(0, min(int(tab), len(TABS) - 1))
        self.notebook.SetSelection(index)
        self.syncMenu()

    def onTabChanged(self, event):
        self.syncMenu()
        event.Skip()

    def syncMenu(self):
        tab = self.notebook.GetSelection()
        view = self.activeView()
        can_export = hasattr(view, 'tableRows')
        self.GetMenuBar().Enable(self.ID_CopyText, can_export)
        self.GetMenuBar().Enable(self.ID_CopyImage, can_export)
        self.GetMenuBar().Enable(self.ID_ExportCSV, can_export)
        self.GetMenuBar().Enable(self.ID_SaveImage, hasattr(view, 'onSaveAsBitmap'))
        self.GetMenuBar().Enable(self.ID_Separate, True)
        self.mbw.Check(getattr(view, 'bw', self.options.bw))
        self.intro.SetLabel(DESCRIPTIONS[tab])
        self.Layout()

    def onPositionsPopup(self, event):
        """Preserve the old right-click menu for the embedded speculum."""
        self.PopupMenu(self.positions_popup)

    def onSaveImage(self, event):
        view = self.activeView()
        if hasattr(view, 'onSaveAsBitmap'):
            view.onSaveAsBitmap(event)

    def onCopyText(self, event):
        view = self.activeView()
        if hasattr(view, 'onCopyAsText'):
            view.onCopyAsText(event)

    def onCopyImage(self, event):
        view = self.activeView()
        if hasattr(view, 'onCopyAsImage'):
            view.onCopyAsImage(event)

    def onExportCSV(self, event):
        view = self.activeView()
        if hasattr(view, 'onExportCSV'):
            view.onExportCSV(event)

    def onBlackAndWhite(self, event):
        view = self.activeView()
        if hasattr(view, 'onBlackAndWhite'):
            view.onBlackAndWhite(event)

    def onOpenSeparate(self, event):
        tab = self.notebook.GetSelection()
        original = (positionsframe.PositionsFrame, munposframe.MunPosFrame,
                    speedsframe.SpeedsFrame, miscframe.MiscFrame)[tab]
        if tab == 0:
            if not has_columns(self.options, self.spec_method):
                wx.MessageBox(mtexts.txtspositions['SelectColumn'], 'Positions', wx.OK | wx.ICON_INFORMATION)
                return
            frame = original(self.mainfr, self.mainfr.title, self.chart, self.options,
                             speculum_index=self.spec_method)
        else:
            frame = original(self.mainfr, self.mainfr.title, self.chart, self.options)
        frame.Show()

    def onClose(self, event):
        if getattr(self.mainfr, 'positions_workspace', None) is self:
            self.mainfr.positions_workspace = None
        event.Skip()


def show(mainfr, tab=0):
    """Reuse an open workspace; old table commands become tab aliases."""
    wnd = getattr(mainfr, 'positions_workspace', None)
    if wnd is None or not wnd:
        wnd = PositionsWorkspace(mainfr, mainfr.title, mainfr.horoscope,
                                 mainfr.options, tab)
        mainfr.positions_workspace = wnd
    else:
        wnd.selectTab(tab)
    wnd.Show(True)
    wnd.Raise()
    return wnd
