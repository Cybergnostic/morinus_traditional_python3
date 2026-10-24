"""Reusable, lazy tab host for original bitmap-based Morinus table windows.

Each tab is constructed on demand. Table data and drawing remain in the
legacy view classes; menu commands merely delegate to the active view.
"""
import i18n
import wx


class TableWorkspace(wx.Frame):
    def __init__(self, mainfr, heading, specs, start_tab=0, size=(1050, 680),
                 attribute=None):
        super().__init__(mainfr, -1, i18n.tr(heading), size=size)
        self.mainfr = mainfr
        self.specs = specs   # (label, description, view factory(page), standalone factory(view))
        self.attribute = attribute
        self.views = {}
        self.SetMinSize((600, 390))
        self._build_menu()
        self.book = wx.Notebook(self)
        self.pages = []
        for title, description, factory, standalone in specs:
            page = wx.Panel(self.book)
            self.pages.append(page)
            self.book.AddPage(page, i18n.tr(title))

        self.explanation = wx.StaticText(self, -1, '')
        self.explanation.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))

        footer = wx.BoxSizer(wx.HORIZONTAL)
        footer.Add(self.explanation, 1, wx.ALIGN_CENTER_VERTICAL)
        outer = wx.BoxSizer(wx.VERTICAL)
        outer.Add(self.book, 1, wx.EXPAND)
        outer.Add(footer, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(outer)
        self.book.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChanged)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.selectTab(start_tab)

    def _build_menu(self):
        bar = wx.MenuBar()
        menu = wx.Menu()
        self.save_id = wx.NewIdRef()
        self.copy_text_id = wx.NewIdRef()
        self.copy_image_id = wx.NewIdRef()
        self.csv_id = wx.NewIdRef()
        self.bw_id = wx.NewIdRef()
        self.separate_id = wx.NewIdRef()
        self.close_id = wx.NewIdRef()
        menu.Append(self.save_id, i18n.tr('Save table as image...'))
        menu.Append(self.copy_text_id, i18n.tr('Copy table as text'))
        menu.Append(self.copy_image_id, i18n.tr('Copy table as image'))
        menu.Append(self.csv_id, i18n.tr('Export as CSV...'))
        menu.AppendSeparator()
        self.bw_item = menu.AppendCheckItem(self.bw_id, i18n.tr('Black and white'))
        menu.AppendSeparator()
        menu.Append(self.separate_id, i18n.tr('Open in a separate window'), i18n.tr('The table of this tab in a window of its own, e.g. to compare two tables'))
        menu.Append(self.close_id, i18n.tr('Close workspace'))
        bar.Append(menu, i18n.tr('Table'))
        self.SetMenuBar(bar)
        self.Bind(wx.EVT_MENU, lambda e: self.delegate('onSaveAsBitmap', e), id=self.save_id)
        self.Bind(wx.EVT_MENU, lambda e: self.delegate('onCopyAsText', e), id=self.copy_text_id)
        self.Bind(wx.EVT_MENU, lambda e: self.delegate('onCopyAsImage', e), id=self.copy_image_id)
        self.Bind(wx.EVT_MENU, lambda e: self.delegate('onExportCSV', e), id=self.csv_id)
        self.Bind(wx.EVT_MENU, lambda e: self.delegate('onBlackAndWhite', e), id=self.bw_id)
        self.Bind(wx.EVT_MENU, self.onOpenSeparately, id=self.separate_id)
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), id=self.close_id)

    def ensureTab(self, index):
        if index not in self.views:
            page = self.pages[index]
            view = self.specs[index][2](page)
            layout = wx.BoxSizer(wx.VERTICAL)
            layout.Add(view, 1, wx.EXPAND)
            page.SetSizer(layout)
            self.views[index] = view
            page.Layout()
        return self.views[index]

    def selectTab(self, index):
        index = max(0, min(int(index), len(self.specs) - 1))
        self.book.SetSelection(index)
        self.ensureTab(index)
        self.updateMenu()

    def onTabChanged(self, event):
        self.ensureTab(self.book.GetSelection())
        self.updateMenu()
        event.Skip()

    def activeView(self):
        return self.ensureTab(self.book.GetSelection())

    def updateMenu(self):
        index = self.book.GetSelection()
        # A lazy view may ask for a menu refresh from inside its own
        # constructor (SpeculumPanel.build does exactly this). Until
        # ensureTab() has registered it in self.views, there is nothing
        # to update. ensureTab()/onTabChanged will refresh after creation.
        if index < 0 or index not in self.views:
            return
        view = self.views[index]
        menu = self.GetMenuBar()
        for command_id, name in (
                (self.save_id, 'onSaveAsBitmap'),
                (self.copy_text_id, 'onCopyAsText'),
                (self.copy_image_id, 'onCopyAsImage'),
                (self.csv_id, 'onExportCSV')):
            menu.Enable(command_id, hasattr(view, name))
        self.bw_item.Enable(hasattr(view, 'onBlackAndWhite'))
        self.bw_item.Check(getattr(view, 'bw', False))
        self.explanation.SetLabel(i18n.tr(self.specs[index][1]))
        self.Layout()

    def delegate(self, method, event):
        target = self.activeView()
        callback = getattr(target, method, None)
        if callback is not None:
            callback(event)
        self.updateMenu()

    def onOpenSeparately(self, event):
        index = self.book.GetSelection()
        self.specs[index][3](self.views.get(index))

    def onClose(self, event):
        if self.attribute and getattr(self.mainfr, self.attribute, None) is self:
            setattr(self.mainfr, self.attribute, None)
        event.Skip()
