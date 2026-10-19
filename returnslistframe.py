"""Window listing the lunar returns (or monthly solar returns) of a solar year;
double-click opens a return as a chart with the radix, like Charts > Revolutions."""

import datetime
import wx
import returnslist
import transitframe
import util

SIGNS = ('Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis')
KINDS = ('Lunar returns', 'Monthly solar returns')


def lonstr(lon):
    d, m, s = util.decToDeg(lon % 30.0)
    return "%2d°%02d' %s" % (d, m, SIGNS[int(lon // 30) % 12])


class ReturnsListFrame(wx.Frame):
    def __init__(self, parent, title, radix, options):
        wx.Frame.__init__(self, parent, -1, title+' - Returns of the year', wx.DefaultPosition, wx.Size(860, 520))
        self.parent = parent
        self.title = title
        self.radix = radix
        self.options = options
        self.rows = []

        panel = wx.Panel(self)
        top = wx.BoxSizer(wx.HORIZONTAL)
        top.Add(wx.StaticText(panel, -1, 'Solar year:'), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.year = wx.SpinCtrl(panel, -1, '', size=(100, -1), min=1, max=9999, initial=self.currentSolarYear())
        top.Add(self.year, 0, wx.ALL, 5)
        self.kind = wx.Choice(panel, -1, choices=list(KINDS))
        self.kind.SetSelection(0)
        top.Add(self.kind, 0, wx.ALL, 5)
        btn = wx.Button(panel, -1, 'Compute')
        top.Add(btn, 0, wx.ALL, 5)
        self.info = wx.StaticText(panel, -1, '')
        top.Add(self.info, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.li = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES)
        for col, (text, width) in enumerate((('Return', 170), ('Date (UT)', 100), ('Time (UT)', 85), ('Ascendant', 105), ('Asc in solar house', 125), ('Asc in natal house', 125), ('Note', 190))):
            self.li.InsertColumn(col, text)
            self.li.SetColumnWidth(col, width)

        hint = wx.StaticText(panel, -1, 'Double-click a row to open the chart. Returns are cast for the place of birth; houses are counted by whole signs. '
                             'Lunar returns follow the Moon back to its natal degree (a sidereal month), so a solar year has 13 or 14 of them.')
        hint.Wrap(820)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(top, 0, wx.ALL, 2)
        sizer.Add(self.li, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(hint, 0, wx.ALL, 5)
        panel.SetSizer(sizer)

        btn.Bind(wx.EVT_BUTTON, self.onCompute)
        self.kind.Bind(wx.EVT_CHOICE, self.onCompute)
        self.li.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onOpen)
        self.compute()

    def currentSolarYear(self):
        today = datetime.date.today()
        t = self.radix.time
        birthday_passed = (today.month, today.day) >= (t.origmonth, t.origday)
        return today.year if birthday_passed else today.year-1

    def onCompute(self, event):
        self.compute()

    def compute(self):
        wait = wx.BusyCursor()
        self.rows = returnslist.compute(self.radix, self.year.GetValue(), self.kind.GetSelection())
        self.li.DeleteAllItems()
        if not self.rows:
            self.info.SetLabel('Could not compute the solar return for this year.')
            return
        solar_asc = self.rows[0].chart.houses.ascmc[0]
        natal_asc = self.radix.houses.ascmc[0]
        for i, r in enumerate(self.rows):
            asc = r.chart.houses.ascmc[0]
            idx = self.li.InsertItem(i, r.kind)
            self.li.SetItem(idx, 1, '%04d-%02d-%02d' % r.t[:3])
            self.li.SetItem(idx, 2, '%02d:%02d:%02d' % r.t[3:])
            self.li.SetItem(idx, 3, lonstr(asc))
            self.li.SetItem(idx, 4, str(returnslist.sign_house(asc, solar_asc)))
            self.li.SetItem(idx, 5, str(returnslist.sign_house(asc, natal_asc)))
            self.li.SetItem(idx, 6, r.note)
            if i == 0:
                font = self.li.GetFont()
                font.SetWeight(wx.FONTWEIGHT_BOLD)
                self.li.SetItemFont(idx, font)
        n = len(self.rows)-1-sum(1 for r in self.rows if r.note == returnslist.IN_FORCE)
        what = 'lunar returns' if self.kind.GetSelection() == returnslist.LUNAR else 'monthly solar returns'
        self.info.SetLabel('%d %s after the solar return' % (n, what))

    def onOpen(self, event):
        r = self.rows[event.GetIndex()]
        rw = transitframe.TransitFrame(self.parent, self.title, r.chart, self.radix, self.options)
        rw.Show(True)
