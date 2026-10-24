"""On-demand monthly solar returns for one solar year (Natalna 27)."""

import astrology
import chart
import i18n
import monthlysolar
import planets
import returnslist
import util
import wx


SIGNS = ('Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis')


def _crossings(radix, target, approximate_jd):
    year, month, _day, _hour = astrology.swe_revjul(approximate_jd, astrology.SE_GREG_CAL)
    previous = util.decrMonth(year, month)
    following = util.incrMonth(year, month)
    found = []
    for y, m in (previous, (year, month), following):
        found.extend(returnslist._month_returns(y, m, radix, planets.Planets.SUN, target))
    return found


def compute(radix, solar):
    if radix.options.ayanamsha != 0:
        raise ValueError('Monthly solar revolutions currently require the tropical zodiac')
    year = returnslist.solar_year_for_chart(radix, solar)
    next_t = returnslist.solar_return(radix, year + 1)
    if next_t is None:
        raise ValueError('Could not calculate the next solar return')
    natal_sun = radix.planets.planets[planets.Planets.SUN].data[planets.Planet.LON]
    return monthlysolar.choose_events(
        solar.time.jd, returnslist.gmt_time(next_t, radix).jd, natal_sun,
        lambda target, estimate: _crossings(radix, target, estimate),
    )


class MonthlySolarFrame(wx.Frame):
    def __init__(self, parent, title, radix, solar, options):
        wx.Frame.__init__(self, parent, -1, i18n.tr(title + ' - Monthly solar revolutions'),
                          size=(760, 490))
        self.parent = parent
        self.title = title
        self.radix = radix
        self.solar = solar
        self.options = options
        self.rows = []
        panel = wx.Panel(self)
        top = wx.StaticText(panel, label=i18n.tr(
            'Sun returns to the natal degree in each successive sign (tropical).'))
        self.list = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES)
        for col, (heading, width) in enumerate((
            ('Month', 100), ('Sun at', 130), ('Date (UT)', 140),
            ('Time (UT)', 125), ('Type', 190),
        )):
            self.list.InsertColumn(col, i18n.tr(heading))
            self.list.SetColumnWidth(col, width)
        hint = wx.StaticText(panel, label=i18n.tr('Double-click a row to open that monthly chart.'))
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(top, 0, wx.ALL, 8)
        layout.Add(self.list, 1, wx.EXPAND | wx.ALL, 6)
        layout.Add(hint, 0, wx.ALL, 8)
        panel.SetSizer(layout)
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onOpen)
        self.populate()

    def populate(self):
        self.rows = compute(self.radix, self.solar)
        year = returnslist.solar_year_for_chart(self.radix, self.solar)
        annual_time = returnslist.solar_return(self.radix, year)
        self.list.DeleteAllItems()
        for i, row in enumerate(self.rows):
            # The return function supplies UT, regardless of how the displayed
            # solar chart's time fields are represented.
            stamp = row.utc_tuple if row.utc_tuple is not None else annual_time
            degree = row.target_longitude % 30.0
            sun_at = "%02d\N{DEGREE SIGN}%02d' %s" % (
                int(degree), int((degree % 1.0) * 60), SIGNS[int(row.target_longitude // 30) % 12],
            )
            idx = self.list.InsertItem(i, str(row.month))
            for col, value in enumerate((sun_at, '%04d-%02d-%02d' % stamp[:3],
                                         '%02d:%02d:%02d' % stamp[3:],
                                         'Annual solar return' if i == 0 else 'Monthly solar return'), start=1):
                self.list.SetItem(idx, col, i18n.tr(value))

    def onOpen(self, event):
        # Avoid a module-level import cycle: transitframe owns this popup.
        import transitframe
        row = self.rows[event.GetIndex()]
        chrt = self.solar if row.utc_tuple is None else returnslist.return_chart(
            row.utc_tuple, self.radix, chart.Chart.REVOLUTION, self.solar.place,
        )
        frame = transitframe.TransitFrame(
            self.parent, self.title + ' - Monthly solar %d' % row.month,
            chrt, self.radix, self.options,
        )
        frame.Show(True)
