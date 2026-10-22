"""Graphical, tabular and event ephemerides backed by one Swiss data series."""
import i18n
import calendar
import csv
import datetime
import io

import wx
import astrology
import chart
import graphephemwnd
import graphephemframe
import ephemerisdata
import transitframe


def event_datetime(year_data, jd):
    """UTC instant, rounded to a second (works for supported AD years)."""
    return datetime.datetime(year_data.year, 1, 1) + datetime.timedelta(
        days=jd - year_data.jds[0], microseconds=500000)


class EphemerisWorkspace(wx.Frame):
    def __init__(self, mainfr, year):
        super().__init__(mainfr, -1, i18n.tr('Ephemeris — %d') % year, size=(1180, 760))
        self.mainfr = mainfr
        self.options = mainfr.options
        self.SetMinSize((760, 500))
        self.cache = {}
        self.data = None
        self.selected_day = 0
        self.day_indices = []
        self.graph = None
        self._syncing = False
        self._build_layout(year)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.loadYear(year)

    def _build_layout(self, year):
        self.year = wx.SpinCtrl(self, -1, min=1, max=5000, initial=year, size=(95, -1))
        prev = wx.Button(self, -1, i18n.tr('◀ Previous year'))
        next_year = wx.Button(self, -1, i18n.tr('Next year ▶'))
        go = wx.Button(self, -1, i18n.tr('Go'))
        prev.Bind(wx.EVT_BUTTON, lambda event: self.loadYear(max(1, self.data.year - 1)))
        next_year.Bind(wx.EVT_BUTTON, lambda event: self.loadYear(min(5000, self.data.year + 1)))
        go.Bind(wx.EVT_BUTTON, lambda event: self.loadYear(self.year.GetValue()))
        self.year.Bind(wx.EVT_TEXT_ENTER, lambda event: self.loadYear(self.year.GetValue()))
        head = wx.BoxSizer(wx.HORIZONTAL)
        head.Add(wx.StaticText(self, -1, i18n.tr('Gregorian year')), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        head.Add(self.year, 0, wx.RIGHT, 9)
        head.Add(go, 0, wx.RIGHT, 20)
        head.Add(prev, 0, wx.RIGHT, 7)
        head.Add(next_year, 0)

        self.book = wx.Notebook(self)
        self.graph_page = wx.Panel(self.book)
        self.daily_page = wx.Panel(self.book)
        self.events_page = wx.Panel(self.book)
        self.book.AddPage(self.graph_page, i18n.tr('Graph'))
        self.book.AddPage(self.daily_page, i18n.tr('Daily positions'))
        self.book.AddPage(self.events_page, i18n.tr('Stations & ingresses'))

        self._build_graph_page()
        self._build_daily_page()
        self._build_events_page()

        self.status = wx.StaticText(self, -1, '')
        self.status.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
        outer = wx.BoxSizer(wx.VERTICAL)
        outer.Add(head, 0, wx.EXPAND | wx.ALL, 10)
        outer.Add(self.book, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        outer.Add(self.status, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(outer)
        self.book.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPage)
        self.graph_page.Bind(wx.EVT_SIZE, self.onGraphPageSize)

    def _build_graph_page(self):
        self.graph_menu = wx.Menu()
        self.graph_save = self.graph_menu.Append(wx.NewIdRef(), i18n.tr('Save graph as image...'))
        self.mbw = self.graph_menu.AppendCheckItem(wx.NewIdRef(), i18n.tr('Black and white'))
        self.mbw.Check(bool(self.options.bw))
        self.Bind(wx.EVT_MENU, self.onSaveGraph, id=self.graph_save.GetId())
        self.Bind(wx.EVT_MENU, self.onBW, id=self.mbw.GetId())
        self.graph_page.mbw = self.mbw
        self.graph_page.onPopupMenu = self.onGraphPopup

        self.show_moon = wx.CheckBox(self.graph_page, -1, i18n.tr('Show Moon on graph'))
        self.show_moon.SetToolTip(i18n.tr('Off reproduces the original six-planet Morinus graphical ephemeris'))
        self.show_moon.Bind(wx.EVT_CHECKBOX, self.onShowMoon)
        self.open_classic = wx.Button(self.graph_page, -1, i18n.tr('Open classic graph'))
        self.open_classic.Bind(wx.EVT_BUTTON, self.onOpenClassic)
        bar = wx.BoxSizer(wx.HORIZONTAL)
        bar.Add(self.show_moon, 0, wx.ALIGN_CENTER_VERTICAL)
        bar.AddStretchSpacer()
        bar.Add(self.open_classic, 0)
        self.graph_box = wx.BoxSizer(wx.VERTICAL)
        self.graph_box.Add(bar, 0, wx.EXPAND | wx.ALL, 8)
        self.graph_page.SetSizer(self.graph_box)

    def _build_daily_page(self):
        controls = wx.BoxSizer(wx.HORIZONTAL)
        self.month = wx.Choice(self.daily_page, -1,
                               choices=['All months'] + list(calendar.month_name)[1:])
        self.month.SetSelection(0)
        self.month.Bind(wx.EVT_CHOICE, lambda e: self.fillDays())
        self.with_speeds = wx.CheckBox(self.daily_page, -1, i18n.tr('Show speeds (°/day)'))
        self.with_speeds.Bind(wx.EVT_CHECKBOX, lambda e: self.fillDays())
        copy = wx.Button(self.daily_page, -1, i18n.tr('Copy CSV'))
        export = wx.Button(self.daily_page, -1, i18n.tr('Export CSV...'))
        copy.Bind(wx.EVT_BUTTON, lambda e: self.copyCSV(self.dailyRows()))
        export.Bind(wx.EVT_BUTTON, lambda e: self.saveCSV(self.dailyRows(), 'ephemeris'))
        controls.Add(wx.StaticText(self.daily_page, -1, i18n.tr('Month')), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 7)
        controls.Add(self.month, 0, wx.RIGHT, 18)
        controls.Add(self.with_speeds, 0, wx.ALIGN_CENTER_VERTICAL)
        controls.AddStretchSpacer()
        controls.Add(copy, 0, wx.RIGHT, 7)
        controls.Add(export, 0)
        self.days = wx.ListCtrl(self.daily_page, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.days.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onDaySelected)
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(controls, 0, wx.EXPAND | wx.ALL, 9)
        layout.Add(self.days, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
        self.daily_page.SetSizer(layout)

    def _build_events_page(self):
        top = wx.BoxSizer(wx.HORIZONTAL)
        self.kind = wx.Choice(self.events_page, -1,
                              choices=i18n.tr(['All events', 'Stations only', 'Ingresses only']))
        self.kind.SetSelection(0)
        self.kind.Bind(wx.EVT_CHOICE, lambda e: self.fillEvents())
        self.open_event = wx.Button(self.events_page, -1, i18n.tr('Open event chart'))
        self.open_event.Bind(wx.EVT_BUTTON, self.onOpenEvent)
        copy = wx.Button(self.events_page, -1, i18n.tr('Copy CSV'))
        export = wx.Button(self.events_page, -1, i18n.tr('Export CSV...'))
        copy.Bind(wx.EVT_BUTTON, lambda e: self.copyCSV(self.eventRows()))
        export.Bind(wx.EVT_BUTTON, lambda e: self.saveCSV(self.eventRows(), 'events'))
        top.Add(self.kind, 0, wx.RIGHT, 8)
        top.Add(self.open_event, 0, wx.RIGHT, 8)
        top.AddStretchSpacer()
        top.Add(copy, 0, wx.RIGHT, 8)
        top.Add(export, 0)
        self.events = wx.ListCtrl(self.events_page, -1,
                                  style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        columns = [('UT date and time', 190), ('Planet', 105), ('Event', 110),
                   ('Details', 230)]
        for index, (heading, width) in enumerate(columns):
            self.events.InsertColumn(index, i18n.tr(heading), width=width)
        self.events.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onEventSelected)
        self.events.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onOpenEvent)
        self.event_indices = []
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(top, 0, wx.EXPAND | wx.ALL, 9)
        layout.Add(self.events, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
        self.events_page.SetSizer(layout)

    def loadYear(self, year):
        year = int(year)
        if self.data is not None and self.data.year == year:
            return
        wx.BeginBusyCursor()
        try:
            if year not in self.cache:
                self.cache[year] = ephemerisdata.year_from_swiss(year, self.options)
                # Keep only the last two years in memory.
                if len(self.cache) > 2:
                    self.cache.pop(next(iter(self.cache)))
            self.data = self.cache[year]
            self.year.SetValue(year)
            self.SetTitle(i18n.tr('Ephemeris — %s') % year)
            self.selected_day = 0
            self.fillDays()
            self.fillEvents()
            if self.graph is not None:
                self.graph.year = year
                self.graph.posArr = self.data.longitudes
                self.graph.setFocusDay(0)
            self.updateStatus()
        finally:
            wx.EndBusyCursor()
        wx.CallAfter(self.mountGraph)

    def fillDays(self):
        if self.data is None:
            return
        self._syncing = True
        try:
            self.days.Freeze()
            self.days.ClearAll()
            self.days.InsertColumn(0, i18n.tr('Date (00:00 UT)'), width=155)
            widths = 210 if self.with_speeds.GetValue() else 139
            for idx, planet in enumerate(ephemerisdata.PLANETS, 1):
                self.days.InsertColumn(idx, i18n.tr(planet), width=widths)
            self.day_indices = []
            month = self.month.GetSelection()
            for day, date in enumerate(self.data.dates):
                if month and date.month != month:
                    continue
                index = self.days.InsertItem(self.days.GetItemCount(), date.isoformat())
                self.day_indices.append(day)
                for planet in range(len(ephemerisdata.PLANETS)):
                    lon = self.data.longitudes[planet][day]
                    speed = self.data.speeds[planet][day]
                    label = ephemerisdata.format_position(lon, speed)
                    if self.with_speeds.GetValue():
                        label += ' (%+.4f)' % speed
                    self.days.SetItem(index, planet + 1, i18n.tr(label))
            if self.selected_day in self.day_indices:
                row = self.day_indices.index(self.selected_day)
                self.days.Select(row)
                self.days.EnsureVisible(row)
        finally:
            self.days.Thaw()
            self._syncing = False

    def fillEvents(self):
        if self.data is None:
            return
        self.events.Freeze()
        try:
            self.events.DeleteAllItems()
            self.event_indices = []
            wanted = self.kind.GetSelection()
            for index, event in enumerate(self.data.events):
                if wanted == 1 and event.kind != 'Station':
                    continue
                if wanted == 2 and event.kind != 'Ingress':
                    continue
                self.event_indices.append(index)
                row = self.events.InsertItem(self.events.GetItemCount(),
                    event_datetime(self.data, event.jd).strftime('%Y-%m-%d %H:%M:%S'))
                self.events.SetItem(row, 1, i18n.tr(ephemerisdata.PLANETS[event.planet]))
                self.events.SetItem(row, 2, i18n.tr(event.kind))
                self.events.SetItem(row, 3, i18n.tr(event.detail))
            self.open_event.Enable(bool(self.event_indices))
        finally:
            self.events.Thaw()

    def onDaySelected(self, event):
        if not self._syncing and event.GetIndex() < len(self.day_indices):
            self.selectDay(self.day_indices[event.GetIndex()])

    def selectDay(self, day):
        if self.data is None:
            return
        self.selected_day = max(0, min(day, len(self.data.dates) - 1))
        if self.graph is not None:
            self.graph.setFocusDay(self.selected_day)
        self.updateStatus()
        if self.selected_day in self.day_indices:
            row = self.day_indices.index(self.selected_day)
            self._syncing = True
            try:
                self.days.Select(row)
                self.days.EnsureVisible(row)
            finally:
                self._syncing = False

    def onEventSelected(self, event):
        if event.GetIndex() < len(self.event_indices):
            record = self.data.events[self.event_indices[event.GetIndex()]]
            day = max(0, min(len(self.data.dates) - 1, int(record.jd - self.data.jds[0])))
            self.selectDay(day)

    def updateStatus(self):
        if self.data is None:
            return
        date = self.data.dates[self.selected_day].isoformat()
        mode = ('sidereal (ayanamsha of date)' if self.options.ayanamsha
                else 'tropical of date')
        self.status.SetLabel(i18n.tr('%s • midnight UT • %s • 7 visible planets • '
                             '%d days • %d stations/ingresses') %
                             (date, mode, len(self.data.dates), len(self.data.events)))

    def onPage(self, event):
        if self.book.GetSelection() == 0:
            wx.CallAfter(self.mountGraph)
        event.Skip()

    def onGraphPageSize(self, event):
        event.Skip()
        if self.data is not None and self.graph is None:
            wx.CallAfter(self.mountGraph)

    def mountGraph(self):
        if self.data is None or self.graph is not None:
            return
        # Never initialise the legacy wx.Bitmap renderer on a hidden/0x0 tab.
        if not self.graph_page.IsShownOnScreen():
            return
        w, h = self.graph_page.GetClientSize()
        if w < 250 or h < 220:
            return
        self.graph = graphephemwnd.GraphEphemWnd(
            self.graph_page, self.data.year, self.data.longitudes,
            self.options, self.mainfr, size=(w, max(240, h - 45)),
            show_moon=self.show_moon.GetValue())
        self.graph.on_select_day = self.selectDay
        self.graph_box.Insert(0, self.graph, 1, wx.EXPAND)
        self.graph_page.Layout()
        self.graph.setFocusDay(self.selected_day)

    def onShowMoon(self, event):
        if self.graph is not None:
            self.graph.setShowMoon(self.show_moon.GetValue())

    def onGraphPopup(self, event):
        self.PopupMenu(self.graph_menu)

    def onSaveGraph(self, event):
        if self.graph is not None:
            self.graph.onSaveAsBitmap(event)

    def onBW(self, event):
        if self.graph is not None:
            self.graph.onBlackAndWhite(event)

    def onOpenClassic(self, event):
        frame = graphephemframe.GraphEphemFrame(
            self.mainfr, 'Graphical ephemeris', self.data.year,
            self.data.longitudes, self.options)
        frame.Show()

    def dailyRows(self):
        headers = ['Date UT (00:00)'] + list(ephemerisdata.PLANETS) + [
            planet + ' speed (deg/day)' for planet in ephemerisdata.PLANETS]
        rows = [headers]
        for i, date in enumerate(self.data.dates):
            rows.append([date.isoformat()] +
                        ['%.6f' % self.data.longitudes[p][i] for p in range(7)] +
                        ['%+.6f' % self.data.speeds[p][i] for p in range(7)])
        return rows

    def eventRows(self):
        rows = [['Date and time UT', 'Planet', 'Type', 'Event']]
        for event in self.data.events:
            rows.append([event_datetime(self.data, event.jd).strftime('%Y-%m-%d %H:%M:%S'),
                         ephemerisdata.PLANETS[event.planet], event.kind, event.detail])
        return rows

    def copyCSV(self, rows):
        with io.StringIO(newline='') as buffer:
            csv.writer(buffer).writerows(rows)
            data = buffer.getvalue()
        if wx.TheClipboard.Open():
            try:
                wx.TheClipboard.SetData(wx.TextDataObject(data))
                wx.TheClipboard.Flush()
            finally:
                wx.TheClipboard.Close()

    def saveCSV(self, rows, suffix):
        name = '%d_%s.csv' % (self.data.year, suffix)
        with wx.FileDialog(self, i18n.tr('Export ephemeris CSV'), wildcard='CSV files (*.csv)|*.csv',
                           defaultFile=name, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            with open(dlg.GetPath(), 'w', encoding='utf-8-sig', newline='') as f:
                csv.writer(f).writerows(rows)

    def onOpenEvent(self, event):
        selected = self.events.GetFirstSelected()
        if selected == -1 or selected >= len(self.event_indices):
            return
        record = self.data.events[self.event_indices[selected]]
        instant = event_datetime(self.data, record.jd)
        radix = None if self.mainfr.splash else self.mainfr.horoscope
        if radix is None:
            wx.MessageBox(i18n.tr('Open a natal chart before creating an event wheel.'),
                          i18n.tr('Ephemeris'), wx.OK | wx.ICON_INFORMATION, self)
            return
        place = radix.place
        time = chart.Time(instant.year, instant.month, instant.day,
                          instant.hour, instant.minute, instant.second,
                          False, chart.Time.GREGORIAN, chart.Time.GREENWICH,
                          True, 0, 0, False, place)
        eventchart = chart.Chart(radix.name, radix.male, time, place,
                                 chart.Chart.TRANSIT, record.detail,
                                 self.options, False)
        wnd = transitframe.TransitFrame(self.mainfr,
                self.mainfr.title + ' — ' + i18n.tr(record.detail),
                eventchart, radix, self.options)
        wnd.Show()

    def onClose(self, event):
        if getattr(self.mainfr, 'ephemeris_workspace', None) is self:
            self.mainfr.ephemeris_workspace = None
        event.Skip()


def show(mainfr, year=None):
    if year is None:
        if not mainfr.splash and not mainfr.horoscope.time.bc:
            year = mainfr.horoscope.time.origyear
        else:
            year = datetime.date.today().year
    year = max(1, min(5000, int(year)))
    wnd = getattr(mainfr, 'ephemeris_workspace', None)
    if wnd is None or not wnd:
        wnd = EphemerisWorkspace(mainfr, year)
        mainfr.ephemeris_workspace = wnd
    else:
        wnd.loadYear(year)
    wnd.Show()
    wnd.Raise()
    wx.CallAfter(wnd.mountGraph)
    return wnd
