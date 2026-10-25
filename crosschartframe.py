"""A5 cross-chart planetary, angle and Lot comparison tables."""
import wx
import i18n
import crosschart_aspects
import point_aspects
from traditional_aspects import PLANETS


class CrossChartFrame(wx.Frame):
    def __init__(self, wheel):
        super().__init__(wheel, title=i18n.tr('Cross-chart aspects'),
                         size=(1230, 710))
        self.wheel = wheel
        self.SetMinSize((850, 460))
        root = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)

        selectors = wx.BoxSizer(wx.HORIZONTAL)
        selectors.Add(wx.StaticText(root, label=i18n.tr('Chart A') + ':'),
                      0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.chart_a = wx.Choice(root)
        selectors.Add(self.chart_a, 2, wx.RIGHT, 14)
        selectors.Add(wx.StaticText(root, label=i18n.tr('Chart B') + ':'),
                      0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.chart_b = wx.Choice(root)
        selectors.Add(self.chart_b, 2, wx.RIGHT, 10)
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
        layout.Add(filters, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        self.tabs = wx.Notebook(root)
        self.planet_page = wx.Panel(self.tabs)
        self.angle_page = wx.Panel(self.tabs)
        self.lot_page = wx.Panel(self.tabs)
        self.table = self._table(self.planet_page, (
            ('Chart A planet', 140), ('Aspect', 115),
            ('Chart B planet', 140), ('Orb', 85),
            ('Sign relation', 115), ('B motion vs fixed A', 175),
            ('A receives B', 195), ('B receives A', 195)))
        point_cols = (
            ('Planet chart', 105), ('Planet', 105), ('Aspect', 135),
            ('Point chart', 105), ('Point', 210), ('Orb', 105),
            ('Sign relation', 125))
        self.angle_table = self._table(self.angle_page, point_cols)
        self.lot_table = self._table(self.lot_page, point_cols)
        bar = wx.BoxSizer(wx.HORIZONTAL)
        bar.Add(wx.StaticText(self.lot_page, label=i18n.tr('Lot') + ':'),
                0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.lot_choice = wx.Choice(self.lot_page)
        self.lot_choice.Append(i18n.tr('All Lots'))
        self.lot_choice.SetSelection(0)
        bar.Add(self.lot_choice, 0)
        self.lot_page.GetSizer().Insert(0, bar, 0, wx.ALL, 8)
        self.tabs.AddPage(self.planet_page, i18n.tr('Planets'))
        self.tabs.AddPage(self.angle_page, i18n.tr('Angles'))
        self.tabs.AddPage(self.lot_page, i18n.tr('Lots'))
        layout.Add(self.tabs, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        self.summary = wx.StaticText(root, label='')
        layout.Add(self.summary, 0, wx.LEFT | wx.TOP | wx.BOTTOM, 12)
        root.SetSizer(layout)

        for ctrl in (self.chart_a, self.chart_b, self.planet_a,
                     self.planet_b, self.lot_choice):
            ctrl.Bind(wx.EVT_CHOICE, self.refresh)
        self.only_receptions.Bind(wx.EVT_CHECKBOX, self.refresh)
        self.recalculate.Bind(wx.EVT_BUTTON, self.refresh)
        self.copy.Bind(wx.EVT_BUTTON, self.copy_table)
        self.tabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab)
        self.Bind(wx.EVT_ACTIVATE, self.on_active)
        self.update_slots(preserve=False)
        self.refresh()

    @staticmethod
    def _table(parent, columns):
        sizer = wx.BoxSizer(wx.VERTICAL)
        table = wx.ListCtrl(parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        for col, (label, width) in enumerate(columns):
            table.InsertColumn(col, i18n.tr(label), width=width)
        sizer.Add(table, 1, wx.EXPAND | wx.ALL, 7)
        parent.SetSizer(sizer)
        return table

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
            self.update_slots()
            self.refresh()
        event.Skip()

    def on_tab(self, event):
        event.Skip()
        self.refresh()

    @staticmethod
    def _orb(value):
        if value is None:
            return '—'
        minutes = int(round(value * 60.0))
        deg, minute = divmod(minutes, 60)
        return '%d°%02d′' % (deg, minute)

    @staticmethod
    def _dignities(values):
        return ' + '.join(i18n.tr(v.title()) for v in values) if values else '—'

    @staticmethod
    def _add_row(table, values):
        index = table.InsertItem(table.GetItemCount(), str(values[0]))
        for col, value in enumerate(values[1:], 1):
            table.SetItem(index, col, str(value))

    def refresh(self, event=None):
        for table in (self.table, self.angle_table, self.lot_table):
            table.DeleteAllItems()
        charts = self.selected_charts()
        a_index, b_index = self.chart_a.GetSelection(), self.chart_b.GetSelection()
        if not (0 <= a_index < len(charts) and 0 <= b_index < len(charts)):
            return
        first, second = charts[a_index], charts[b_index]
        lot_names = tuple(dict.fromkeys(
            [p.name for chrt in (first, second)
             for p in point_aspects.lots(chrt, self.wheel.options)]))
        selected_lot = (self.lot_choice.GetStringSelection()
                        if self.lot_choice.GetSelection() > 0 else None)
        self.lot_choice.Set([i18n.tr('All Lots')] + list(lot_names))
        if selected_lot in lot_names:
            self.lot_choice.SetStringSelection(selected_lot)
        else:
            self.lot_choice.SetSelection(0)
            selected_lot = None
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
            self._add_row(self.table, (
                i18n.tr(r.first), i18n.tr(r.aspect), i18n.tr(r.second),
                self._orb(r.deviation),
                i18n.tr('Out of sign' if r.out_of_sign else 'By sign'),
                i18n.tr(r.motion_b), self._dignities(r.a_receives_b),
                self._dignities(r.b_receives_a)))

        for kind, table in (('Angles', self.angle_table), ('Lots', self.lot_table)):
            found = point_aspects.analyze_cross(
                first, second, kind, self.wheel.options,
                point_filter=selected_lot if kind == 'Lots' else None)
            for r in found:
                if ((r.chart_of_planet == 'A' and only_first is not None
                     and r.planet != only_first) or
                    (r.chart_of_planet == 'B' and only_second is not None
                     and r.planet != only_second)):
                    continue
                self._add_row(table, (
                    r.chart_of_planet, i18n.tr(r.planet), i18n.tr(r.aspect),
                    r.chart_of_point, i18n.tr(r.point), self._orb(r.deviation),
                    i18n.tr('Out of sign' if r.out_of_sign else 'By sign')))
        self.update_summary()

    def update_summary(self):
        current = self.tabs.GetSelection()
        table = (self.table, self.angle_table, self.lot_table)[max(0, current)]
        label = ('%d cross-chart aspects', '%d angle aspects', '%d Lot aspects')[max(0, current)]
        self.summary.SetLabel(i18n.tr(label) % table.GetItemCount())
        self.only_receptions.Enable(current == 0)

    def copy_table(self, event):
        table = (self.table, self.angle_table, self.lot_table)[self.tabs.GetSelection()]
        rows = ['\t'.join(table.GetColumn(i).GetText()
                          for i in range(table.GetColumnCount()))]
        for line in range(table.GetItemCount()):
            rows.append('\t'.join(table.GetItemText(line, i)
                         for i in range(table.GetColumnCount())))
        if wx.TheClipboard.Open():
            try:
                wx.TheClipboard.SetData(wx.TextDataObject('\n'.join(rows)))
            finally:
                wx.TheClipboard.Close()
