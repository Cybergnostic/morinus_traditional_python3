"""Independent lunar-phase navigator; never changes the prenatal syzygy."""
import wx
import astrology
import chart
import transitframe
import lunationnav
import zodiacalreleasing



def event_chart(radix, jd, kind, options):
    """The chart of a lunation at UT jd, at the place of radix (None before AD 1)."""
    calflag = (astrology.SE_GREG_CAL if radix.time.cal == chart.Time.GREGORIAN
               else astrology.SE_JUL_CAL)
    # Round through the Julian-day conversion to avoid a spurious :60.
    y, m, d, fraction = astrology.swe_revjul(jd + 0.5 / 86400.0, calflag)
    if y <= 0:
        return None
    hour, remainder = divmod(int(fraction * 3600), 3600)
    minute, second = divmod(remainder, 60)
    tim = chart.Time(y, m, d, hour, minute, second, False, radix.time.cal,
                     chart.Time.GREENWICH, True, 0, 0, False, radix.place)
    return chart.Chart(radix.name, radix.male, tim, radix.place, chart.Chart.TRANSIT, kind, options, False)


def stepper(radix, options):
    """For a chart window: the New or Full Moon before or after a chart."""
    sampler = lunationnav.ephemeris_sampler()

    def step(chrt, forward):
        jd = chrt.time.jd
        events = lunationnav.find_events(jd + (8 if forward else -8), sampler, 20)
        if forward:
            found = [e for e in events if e[0] > jd + 0.001]
            event = found[0] if found else None
        else:
            found = [e for e in events if e[0] < jd - 0.001]
            event = found[-1] if found else None
        return event_chart(radix, event[0], event[1], options) if event else None
    return step


class LunationNavigator(wx.Frame):
    def __init__(self, mainfr):
        super().__init__(mainfr, -1, 'Syzygies and lunar phases — ' + mainfr.horoscope.name,
                         size=(850, 580))
        self.mainfr = mainfr
        self.radix = mainfr.horoscope
        self.center_jd = self.radix.time.jd
        self.events = []
        self.sampler = lunationnav.ephemeris_sampler()
        self.SetMinSize((650, 430))
        self.heading = wx.StaticText(self, -1,
            'New and Full Moons near the chart date (geocentric ecliptic conjunction/opposition)')
        self.note = wx.StaticText(self, -1,
            'Times shown in the birth chart\'s entered time convention. '
            'The prenatal syzygy used by lots, almutens and traditional techniques is unchanged.')
        self.note.Wrap(780)

        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        for i, (name, width) in enumerate((
                ('Event', 125), ('Chart time', 200), ('Days from birth', 130),
                ('Sun longitude', 130), ('Moon longitude', 130))):
            self.list.InsertColumn(i, name, width=width)
        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelection)
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onOpenChart)

        self.earlier = wx.Button(self, -1, 'Earlier')
        self.later = wx.Button(self, -1, 'Later')
        self.reset = wx.Button(self, -1, 'Birth date')
        self.open = wx.Button(self, -1, 'Open event chart')
        self.prenatal = wx.Button(self, -1, 'Prenatal syzygy chart')
        self.other_prenatal = wx.Button(self, -1, 'Other prenatal lunation chart')
        self.close = wx.Button(self, wx.ID_CLOSE, 'Close')
        self.earlier.Bind(wx.EVT_BUTTON, lambda e: self.shift(-55))
        self.later.Bind(wx.EVT_BUTTON, lambda e: self.shift(55))
        self.reset.Bind(wx.EVT_BUTTON, lambda e: self.resetDate())
        self.open.Bind(wx.EVT_BUTTON, self.onOpenChart)
        # These retain the original configured prenatal-chart calculations.
        self.prenatal.Bind(wx.EVT_BUTTON, self.mainfr.onSyzygyChart)
        self.other_prenatal.Bind(wx.EVT_BUTTON, self.mainfr.onSyzygyChart2)
        self.close.Bind(wx.EVT_BUTTON, lambda e: self.Close())
        self.Bind(wx.EVT_CLOSE, self.onClose)

        traditional = wx.BoxSizer(wx.HORIZONTAL)
        traditional.Add(wx.StaticText(self, -1, 'Traditional syzygies:'), 0,
                        wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        traditional.Add(self.prenatal, 0, wx.RIGHT, 8)
        traditional.Add(self.other_prenatal, 0)
        nav = wx.BoxSizer(wx.HORIZONTAL)
        for b in (self.earlier, self.reset, self.later):
            nav.Add(b, 0, wx.RIGHT, 7)
        nav.AddStretchSpacer()
        nav.Add(self.open, 0, wx.RIGHT, 7)
        nav.Add(self.close, 0)
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.heading, 0, wx.ALL, 12)
        layout.Add(self.list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 12)
        layout.Add(self.note, 0, wx.EXPAND | wx.ALL, 12)
        layout.Add(traditional, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        layout.Add(nav, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        self.SetSizer(layout)
        self.populate()

    def populate(self):
        original = self.radix.syzygy
        self.events = lunationnav.find_events(self.center_jd, self.sampler)
        self.list.DeleteAllItems()
        for idx, (jd, kind, sun, moon) in enumerate(self.events):
            self.list.InsertItem(idx, kind)
            cells = (
                zodiacalreleasing.datestr(self.radix, jd, hours=True),
                '%+.2f' % (jd - self.radix.time.jd),
                '%.3f°' % (sun % 360),
                '%.3f°' % (moon % 360),
            )
            for col, value in enumerate(cells, 1):
                self.list.SetItem(idx, col, value)
        if self.events:
            selected = min(range(len(self.events)),
                           key=lambda i: abs(self.events[i][0] - self.center_jd))
            self.list.Select(selected)
            self.list.Focus(selected)
        self.open.Enable(bool(self.events))
        assert self.radix.syzygy is original, 'Lunation navigator modified prenatal syzygy'

    def shift(self, days):
        self.center_jd += days
        self.populate()

    def resetDate(self):
        self.center_jd = self.radix.time.jd
        self.populate()

    def onSelection(self, event):
        self.open.Enable(self.list.GetFirstSelected() != -1)

    def onOpenChart(self, event):
        selection = self.list.GetFirstSelected()
        if selection == -1:
            return
        jd, kind, sun, moon = self.events[selection]
        eventchart = event_chart(self.radix, jd, kind, self.mainfr.options)
        if eventchart is None:
            wx.MessageBox('Event charts before AD 1 are not supported here.',
                          'Syzygies and lunar phases', wx.OK | wx.ICON_INFORMATION, self)
            return
        frame = transitframe.TransitFrame(self.mainfr,
                 self.mainfr.title + ' — ' + kind, eventchart,
                 self.radix, self.mainfr.options, stepper=stepper(self.radix, self.mainfr.options))
        frame.Show(True)

    def onClose(self, event):
        if getattr(self.mainfr, 'lunation_navigator', None) is self:
            self.mainfr.lunation_navigator = None
        event.Skip()


def show(mainfr):
    if mainfr.splash:
        return None
    if mainfr.horoscope.time.bc:
        wx.MessageBox('Lunation navigation is not available for BC charts.',
                      'New and Full Moons', wx.OK | wx.ICON_INFORMATION, mainfr)
        return None
    existing = getattr(mainfr, 'lunation_navigator', None)
    if existing:
        existing.Show()
        existing.Raise()
        return existing
    wnd = LunationNavigator(mainfr)
    mainfr.lunation_navigator = wnd
    wnd.Show()
    wnd.Raise()
    return wnd
