"""On-demand repeated natal configurations in a solar return.

No chart overlays are changed. Aspects are configured as in Tables > Aspects
(the course orbs); an optional limit narrows the list.
"""

import chart
import divisions
import houses
import i18n
import planets
import repeatedconfigs
import returnslist
import tradoptions
import traditional_aspects
import wx


def chart_longitudes(chrt):
    return {
        name: chrt.planets.planets[idx].data[planets.Planet.LON]
        for idx, name in enumerate(repeatedconfigs.PLANETS)
    }


def annual_lord(radix, solar):
    year = returnslist.solar_year_for_chart(radix, solar)
    asc = radix.houses.ascmc[houses.Houses.ASC]
    if radix.options.ayanamsha:
        asc = (asc - radix.ayanamsha) % 360.0
    sign = divisions.annual_sign(asc, radix.time.origyear, year)
    return divisions.SIGN_RULERS[sign]


def add_columns(control, columns):
    for col, (heading, width) in enumerate(columns):
        control.InsertColumn(col, i18n.tr(heading))
        control.SetColumnWidth(col, width)


def fill_rows(control, rows):
    control.DeleteAllItems()
    for row in rows:
        idx = control.InsertItem(control.GetItemCount(), i18n.tr(str(row[0])))
        for col, value in enumerate(row[1:], start=1):
            control.SetItem(idx, col, i18n.tr(str(value)))


class RepeatedConfigsFrame(wx.Frame):
    def __init__(self, parent, title, radix, solar):
        if solar.htype != chart.Chart.SOLAR or radix.htype != chart.Chart.RADIX:
            raise ValueError('This search requires a natal chart and its solar return')
        wx.Frame.__init__(self, parent, -1, i18n.tr(title) + ' - ' +
                          i18n.tr('Repeated natal configurations'), size=(1010, 620))
        self.radix = radix
        self.solar = solar
        self.year_lord = annual_lord(radix, solar)
        panel = wx.Panel(self)

        description = wx.StaticText(panel, label=i18n.tr(
            'Find the same named planets forming the same aspect in both natal and solar charts.'))
        description.Wrap(940)
        controls = wx.BoxSizer(wx.HORIZONTAL)
        controls.Add(wx.StaticText(panel, label=i18n.tr('Only closer than (degrees, optional):')),
                     0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 7)
        self.deviation = wx.TextCtrl(panel, value='', size=(62, -1))
        controls.Add(self.deviation, 0, wx.RIGHT, 14)
        self.placements = wx.CheckBox(panel, label=i18n.tr('Include repeated signs and whole-sign houses'))
        controls.Add(self.placements, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 12)
        self.only_year = wx.CheckBox(panel, label=i18n.tr('Year lord only'))
        controls.Add(self.only_year, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 12)
        search_button = wx.Button(panel, label=i18n.tr('Search'))
        controls.Add(search_button, 0, wx.ALIGN_CENTER_VERTICAL)
        search_button.Bind(wx.EVT_BUTTON, self.onSearch)

        self.year_note = wx.StaticText(panel, label=i18n.tr('Ruler of the year:') + ' ' +
                                       i18n.tr(self.year_lord))
        self.tabs = wx.Notebook(panel)

        self.aspects = wx.ListCtrl(self.tabs, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES)
        add_columns(self.aspects, (('Planet 1', 125), ('Planet 2', 125), ('Aspect', 142),
                                   ('Natal deviation', 160), ('Solar deviation', 160),
                                   ('Year lord', 115)))
        self.tabs.AddPage(self.aspects, i18n.tr('Repeated aspects'))

        self.triples = wx.ListCtrl(self.tabs, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES)
        add_columns(self.triples, (('Three planets', 260), ('Repeated relationships', 490),
                                   ('Year lord', 120)))
        self.tabs.AddPage(self.triples, i18n.tr('Three-planet configurations'))

        self.positions = wx.ListCtrl(self.tabs, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES)
        add_columns(self.positions, (('Planet', 180), ('Repeated placement', 220),
                                     ('Sign / house', 210), ('Year lord', 120)))
        self.tabs.AddPage(self.positions, i18n.tr('Repeated placements'))

        self.summary = wx.StaticText(panel, label='')
        note = wx.StaticText(panel, label=i18n.tr(
            'Aspects as in Tables > Aspects, in both charts: within the larger '
            'planetary orb, and across a sign boundary only within three degrees. '
            'The optional limit applies to both charts.'))
        note.Wrap(940)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(description, 0, wx.ALL, 9)
        layout.Add(controls, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
        layout.Add(self.year_note, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
        layout.Add(self.tabs, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 7)
        layout.Add(self.summary, 0, wx.ALL, 9)
        layout.Add(note, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
        panel.SetSizer(layout)
        self.onSearch(None)

    def onSearch(self, event):
        try:
            text = self.deviation.GetValue().strip().replace(',', '.')
            tolerance = float(text) if text else None
            orbs = dict(zip(repeatedconfigs.PLANETS,
                            traditional_aspects.doctrinal_orbs(tradoptions.values())))
            result = repeatedconfigs.search(
                chart_longitudes(self.radix), chart_longitudes(self.solar),
                max_deviation=tolerance, year_lord=self.year_lord,
                include_placements=self.placements.GetValue(),
                annual_only=self.only_year.GetValue(),
                natal_asc=self.radix.houses.ascmc[houses.Houses.ASC],
                solar_asc=self.solar.houses.ascmc[houses.Houses.ASC],
                natal_ayanamsha=(self.radix.ayanamsha if self.radix.options.ayanamsha else 0.0),
                solar_ayanamsha=(self.solar.ayanamsha if self.solar.options.ayanamsha else 0.0),
                orbs=orbs,
            )
        except (ValueError, OverflowError) as exc:
            wx.MessageBox(str(exc), i18n.tr('Repeated natal configurations'),
                          wx.OK | wx.ICON_WARNING, self)
            return

        fill_rows(self.aspects, [
            (a.planets[0], a.planets[1], a.aspect,
             '%.2f\N{DEGREE SIGN}' % a.natal_orb,
             '%.2f\N{DEGREE SIGN}' % a.solar_orb,
             'Yes' if a.involves_year_lord else '')
            for a in result.aspects
        ])
        fill_rows(self.triples, [
            (', '.join(t.planets), '; '.join(
                '%s-%s %s' % (a.planets[0], a.planets[1], i18n.tr(a.aspect))
                for a in t.relations),
             'Yes' if t.involves_year_lord else '')
            for t in result.triples
        ])
        fill_rows(self.positions, [
            (p.planet, p.kind,
             repeatedconfigs.SIGNS[p.index] if p.kind == 'Sign' else str(p.index),
             'Yes' if p.involves_year_lord else '')
            for p in result.placements
        ])
        self.summary.SetLabel(i18n.tr('%d repeated aspects, %d three-planet groups, %d repeated placements') %
                              (len(result.aspects), len(result.triples), len(result.placements)))
