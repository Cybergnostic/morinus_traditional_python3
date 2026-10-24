"""A5 table: compare any two currently selected multiwheel chart layers.

Separate from the chart painter; a natal/SR/LR/transit pair is not treated
as two simultaneously moving bodies. No automatic horary judgments.
"""
import wx
import i18n

import crosschart_aspects
from traditional_aspects import PLANETS


class CrossChartFrame(wx.Frame):
    def __init__(self, wheel):
        super().__init__(wheel, title=i18n.tr('Cross-chart aspects'),
                         size=(1210, 690))
        self.wheel = wheel
        self.SetMinSize((800, 460))
        root = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)
        selectors = wx.BoxSizer(wx.HORIZONTAL)

        selectors.Add(wx.StaticText(root, label=i18n.tr('Chart A') + ':'),
                      0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.chart_a = wx.Choice(root)
        selectors.Add(self.chart_a, 2, wx.RIGHT, 16)
        selectors.Add(wx.StaticText(root, label=i18n.tr('Chart B') + ':'),
                      0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.chart_b = wx.Choice(root)
        selectors.Add(self.chart_b, 2, wx.RIGHT, 12)
        self.recalculate = wx.Button(root, label=i18n.tr('Recalculate'))
        self.copy = wx.Button(root, label=i18n.tr('Copy table'))
        selectors.Add(self.recalculate, 0, wx.RIGHT, 6)
        selectors.Add(self.copy, 0)
        layout.Add(selectors, 0, wx.EXPAND | wx.ALL, 12)

        filters = wx.BoxSizer(wx.HORIZONTAL)
        filters.Add(wx.StaticText(root, label=i18n.tr('Planet A') + ':'),
                    0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.planet_a = wx.Choice(root, choices=[i18n.tr('All planets')] +
                                                 i18n.tr(list(PLANETS)))
        self.planet_a.SetSelection(0)
        filters.Add(self.planet_a, 0, wx.RIGHT, 18)
        filters.Add(wx.StaticText(root, label=i18n.tr('Planet B') + ':'),
                    0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.planet_b = wx.Choice(root, choices=[i18n.tr('All planets')] +
                                                 i18n.tr(list(PLANETS)))
        self.planet_b.SetSelection(0)
        filters.Add(self.planet_b, 0, wx.RIGHT, 15)
        self.only_receptions = wx.CheckBox(root, label=i18n.tr('Receptions only'))
        filters.Add(self.only_receptions, 0, wx.ALIGN_CENTER_VERTICAL)
        layout.Add(filters, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

        self.summary = wx.StaticText(root, label='')
        layout.Add(self.summary, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)
        self.table = wx.ListCtrl(root, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        for col, (label, width) in enumerate((
                ('Chart A planet', 140), ('Aspect', 115),
                ('Chart B planet', 140), ('Orb', 85),
                ('Sign relation', 115), ('B motion vs fixed A', 180),
                ('A receives B', 200), ('B receives A', 200))):
            self.table.InsertColumn(col, i18n.tr(label), width=width)
        layout.Add(self.table, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        root.SetSizer(layout)

        self.chart_a.Bind(wx.EVT_CHOICE, self.refresh)
        self.chart_b.Bind(wx.EVT_CHOICE, self.refresh)
        self.planet_a.Bind(wx.EVT_CHOICE, self.refresh)
        self.planet_b.Bind(wx.EVT_CHOICE, self.refresh)
        self.only_receptions.Bind(wx.EVT_CHECKBOX, self.refresh)
        self.recalculate.Bind(wx.EVT_BUTTON, self.refresh)
        self.copy.Bind(wx.EVT_BUTTON, self.copy_table)
        self.Bind(wx.EVT_ACTIVATE, self.on_active)
        self.update_slots(preserve=False)
        self.refresh()

    def selected_charts(self):
        count = self.wheel.count_choice.GetSelection() + 2
        return [picker.selected() for picker in self.wheel.pickers[:count]]

    def update_slots(self, preserve=True):
        old_a = self.chart_a.GetSelection() if preserve else 0
        old_b = self.chart_b.GetSelection() if preserve else 1
        charts = self.selected_charts()
        names = []
        for index, chart in enumerate(charts):
            label = i18n.tr('Inner chart') if index == 0 else i18n.tr('Ring %d') % index
            selected_source = self.wheel.pickers[index].choice.GetStringSelection()
            name = selected_source or (getattr(chart, 'name', '') or '')
            names.append(label + ' — ' + name)
        for choice in (self.chart_a, self.chart_b):
            choice.Set(names)
        self.chart_a.SetSelection(min(max(0, old_a), len(names) - 1))
        self.chart_b.SetSelection(min(max(0, old_b), len(names) - 1))

    def on_active(self, event):
        if event.GetActive():
            # Ring assignments and transient charts may have changed while
            # the comparison table was open.
            self.update_slots()
            self.refresh()
        event.Skip()

    def refresh(self, event=None):
        self.table.DeleteAllItems()
        charts = self.selected_charts()
        a_index, b_index = self.chart_a.GetSelection(), self.chart_b.GetSelection()
        if not (0 <= a_index < len(charts) and 0 <= b_index < len(charts)):
            return
        first, second = charts[a_index], charts[b_index]
        if first is second:
            self.summary.SetLabel(i18n.tr('Select two different chart layers'))
            return
        only_first = (PLANETS[self.planet_a.GetSelection() - 1]
                      if self.planet_a.GetSelection() > 0 else None)
        only_second = (PLANETS[self.planet_b.GetSelection() - 1]
                       if self.planet_b.GetSelection() > 0 else None)
        rows = crosschart_aspects.analyze(
            first, second, self.wheel.options,
            only_first=only_first, only_second=only_second)
        if self.only_receptions.GetValue():
            rows = [r for r in rows if r.a_receives_b or r.b_receives_a]
        for r in rows:
            index = self.table.InsertItem(self.table.GetItemCount(), i18n.tr(r.first))
            names = (i18n.tr(r.aspect), i18n.tr(r.second),
                     self._orb(r.deviation),
                     i18n.tr('Out of sign' if r.out_of_sign else 'By sign'),
                     i18n.tr(r.motion_b),
                     self._dignities(r.a_receives_b),
                     self._dignities(r.b_receives_a))
            for col, value in enumerate(names, 1):
                self.table.SetItem(index, col, value)
        self.summary.SetLabel(i18n.tr('%d cross-chart aspects') % len(rows))

    @staticmethod
    def _orb(value):
        minutes = int(round(value * 60.0))
        deg, minute = divmod(minutes, 60)
        return '%d°%02d′' % (deg, minute)

    @staticmethod
    def _dignities(values):
        return ' + '.join(i18n.tr(v.title()) for v in values) if values else '—'

    def copy_table(self, event):
        rows = ['\t'.join(self.table.GetColumn(i).GetText()
                          for i in range(self.table.GetColumnCount()))]
        for line in range(self.table.GetItemCount()):
            rows.append('\t'.join(self.table.GetItemText(line, i)
                         for i in range(self.table.GetColumnCount())))
        if wx.TheClipboard.Open():
            try:
                wx.TheClipboard.SetData(wx.TextDataObject('\n'.join(rows)))
            finally:
                wx.TheClipboard.Close()
