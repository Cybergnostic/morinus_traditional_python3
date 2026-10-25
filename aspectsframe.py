"""Readable, native-wx aspects workspace with the Morinus classic matrix retained."""

import wx
import i18n
import aspectswnd
import aspect_workspace
import a3_aspects_gui
import a4_aspects_gui
import point_aspects


class AspectsFrame(wx.Frame):
    XSIZE = 1100
    YSIZE = 670

    def __init__(self, parent, title, chrt, options):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition,
                          wx.Size(self.XSIZE, self.YSIZE))
        self.chart = chrt
        self.options = options
        self.SetMinSize((770, 480))
        panel = wx.Panel(self)
        root = wx.BoxSizer(wx.VERTICAL)

        heading = wx.StaticText(panel, -1, i18n.tr("Planetary aspects and receptions"))
        font = heading.GetFont()
        heading.SetFont(font.Bold().Scaled(1.3))
        root.Add(heading, 0, wx.LEFT | wx.TOP | wx.RIGHT, 14)
        self.summary = wx.StaticText(panel, -1, "")
        root.Add(self.summary, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)

        controls = wx.BoxSizer(wx.HORIZONTAL)
        controls.Add(wx.StaticText(panel, -1, i18n.tr("Planet") + ":"),
                     0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 7)
        names = [i18n.tr("All planets")] + list(i18n.tr(aspect_workspace.PLANETS))
        self.planet = wx.Choice(panel, -1, choices=names)
        self.planet.SetSelection(0)
        controls.Add(self.planet, 0, wx.RIGHT, 22)
        self.generosity = wx.CheckBox(panel, -1, i18n.tr("Include generosity"))
        self.generosity.SetValue(True)
        self.generosity.SetToolTip(i18n.tr(
            "Generosity: qualifying dignity without an aspect within orb."))
        controls.Add(self.generosity, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 20)
        controls.AddStretchSpacer()
        refresh = wx.Button(panel, -1, i18n.tr("Refresh"))
        copy = wx.Button(panel, -1, i18n.tr("Copy table"))
        controls.Add(refresh, 0, wx.RIGHT, 7)
        controls.Add(copy, 0)
        root.Add(controls, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)

        self.tabs = wx.Notebook(panel)
        self.contact_page = wx.Panel(self.tabs)
        self.reception_page = wx.Panel(self.tabs)
        classic_page = wx.Panel(self.tabs)

        self.contacts = self._make_table(
            self.contact_page,
            [("Planet A", 105), ("Aspect", 115), ("Planet B", 105),
             ("Orb", 85), ("Motion", 170), ("Sign relation", 115),
             ("A (°/day)", 95), ("B (°/day)", 95), ("Reception", 200)],
            '')
        self.receptions = self._make_table(
            self.reception_page,
            [("Host", 115), ("Receives", 115), ("Classification", 105),
             ("Dignities held", 235), ("Contact", 120),
             ("Mutual", 85), ("Guest position", 155)],
            '')
        self.receptions.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onReceptionSelected)
        self.angle_page = wx.Panel(self.tabs)
        self.lot_page = wx.Panel(self.tabs)
        point_cols = [("Planet", 130), ("Aspect", 145), ("Point", 180),
                      ("Orb", 100), ("Motion", 145), ("Sign relation", 140)]
        self.angle_table = self._make_table(self.angle_page, point_cols, '')
        self.lot_table = self._make_table(self.lot_page, point_cols, '')
        lot_bar = wx.BoxSizer(wx.HORIZONTAL)
        lot_bar.Add(wx.StaticText(self.lot_page, label=i18n.tr('Lot') + ':'),
                    0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 7)
        self.lot_choice = wx.Choice(self.lot_page)
        self.lot_choice.Append(i18n.tr('All Lots'))
        self.lot_choice.SetSelection(0)
        lot_bar.Add(self.lot_choice, 0)
        self.lot_page.GetSizer().Insert(0, lot_bar, 0, wx.ALL, 9)

        old_matrix = aspectswnd.AspectsWnd(classic_page, chrt, options, parent)
        classic_sizer = wx.BoxSizer(wx.VERTICAL)
        classic_sizer.Add(old_matrix, 1, wx.EXPAND)
        classic_page.SetSizer(classic_sizer)
        self.tabs.AddPage(self.contact_page, i18n.tr("Contacts"))
        self.tabs.AddPage(self.reception_page, i18n.tr("Receptions"))
        self.tabs.AddPage(classic_page, i18n.tr("Classic matrix"))
        root.Add(self.tabs, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
        # A3: Universal connections and an on-demand horary event timeline.
        a3_aspects_gui.install(self)
        # A4: sign-based configurations, aversions and directional rays.
        a4_aspects_gui.install(self)
        self.tabs.InsertPage(1, self.angle_page, i18n.tr('Angles'))
        self.tabs.InsertPage(2, self.lot_page, i18n.tr('Lots'))
        panel.SetSizer(root)

        self.planet.Bind(wx.EVT_CHOICE, self.populate)
        self.generosity.Bind(wx.EVT_CHECKBOX, self.populate)
        self.lot_choice.Bind(wx.EVT_CHOICE, self.populate)
        refresh.Bind(wx.EVT_BUTTON, self.populate)
        copy.Bind(wx.EVT_BUTTON, self.copyTable)
        self.populate()

    def _make_table(self, parent, columns, note):
        outer = wx.BoxSizer(wx.VERTICAL)
        table = wx.ListCtrl(parent, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        for index, (heading, width) in enumerate(columns):
            table.InsertColumn(index, i18n.tr(heading), width=width)
        outer.Add(table, 1, wx.EXPAND | wx.ALL, 7)
        if note:
            description = wx.StaticText(parent, -1, i18n.tr(note))
            outer.Add(description, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        parent.SetSizer(outer)
        return table

    def _insert(self, table, values):
        at = table.InsertItem(table.GetItemCount(), str(values[0]))
        for column, value in enumerate(values[1:], 1):
            table.SetItem(at, column, str(value))

    def populate(self, event=None):
        self.all_contacts, self.all_receptions = aspect_workspace.analyze(self.chart)
        target = (None if self.planet.GetSelection() == 0
                  else aspect_workspace.PLANETS[self.planet.GetSelection() - 1])
        self.visible_contacts = [
            a for a in self.all_contacts if target is None or
            target in (a.first, a.second)]
        self.visible_receptions = [
            r for r in self.all_receptions
            if (target is None or target in (r.host, r.guest))
            and (self.generosity.GetValue() or r.status == "Reception")]
        self.contacts.DeleteAllItems()
        self.receptions.DeleteAllItems()
        self.angle_table.DeleteAllItems()
        self.lot_table.DeleteAllItems()
        lot_names = [p.name for p in point_aspects.lots(self.chart, self.options)]
        current_lot = (self.lot_choice.GetStringSelection()
                       if self.lot_choice.GetSelection() > 0 else None)
        self.lot_choice.Set([i18n.tr('All Lots')] + list(dict.fromkeys(lot_names)))
        if current_lot in lot_names:
            self.lot_choice.SetStringSelection(current_lot)
        else:
            self.lot_choice.SetSelection(0)
            current_lot = None
        for row in point_aspects.analyze_single(
                self.chart, "Angles", self.options, planet_filter=target):
            self._point_insert(self.angle_table, row)
        for row in point_aspects.analyze_single(
                self.chart, "Lots", self.options, planet_filter=target,
                point_filter=current_lot):
            self._point_insert(self.lot_table, row)
        reception_pairs = {}
        for r in self.all_receptions:
            if r.status == "Reception":
                key = frozenset((r.host, r.guest))
                reception_pairs.setdefault(key, []).append(r)
        for a in self.visible_contacts:
            rx = reception_pairs.get(frozenset((a.first, a.second)), ())
            if len(rx) == 2:
                relation = i18n.tr("Mutual reception")
            elif rx:
                relation = i18n.tr(rx[0].host) + " → " + i18n.tr(rx[0].guest)
            else:
                relation = "—"
            self._insert(self.contacts, (
                i18n.tr(a.first), i18n.tr(a.kind), i18n.tr(a.second),
                self._degrees(a.deviation), i18n.tr(a.motion),
                i18n.tr("Out of sign" if a.out_of_sign else "By sign"),
                ("%+.4f" % a.first_speed), ("%+.4f" % a.second_speed),
                relation))
        for r in self.visible_receptions:
            dign = " + ".join(i18n.tr(d.title()) for d in r.dignities)
            self._insert(self.receptions, (
                i18n.tr(r.host), i18n.tr(r.guest), i18n.tr(r.status),
                dign, i18n.tr(r.aspect) if r.aspect else "—",
                i18n.tr("Yes") if r.mutual else "—",
                self._degrees(r.guest_degree) + " " + i18n.tr(r.guest_sign)))
        self.summary.SetLabel(
            i18n.tr("%d aspects · %d receptions · %d generosities") % (
                len(self.all_contacts),
                sum(r.status == "Reception" for r in self.all_receptions),
                sum(r.status == "Generosity" for r in self.all_receptions)))
        a3_aspects_gui.refresh_connections(self)
        a4_aspects_gui.refresh(self)

    def _point_insert(self, table, row):
        self._insert(table, (
            i18n.tr(row.planet), i18n.tr(row.aspect), i18n.tr(row.point),
            self._degrees(row.deviation) if row.degree_based else "—",
            i18n.tr(row.motion),
            i18n.tr("Out of sign" if row.out_of_sign else "By sign")))

    @staticmethod
    def _degrees(decimal):
        minutes = round(float(decimal) * 60.0)
        return "%d°%02d′" % divmod(minutes, 60)

    def onReceptionSelected(self, event):
        row = event.GetIndex()
        if 0 <= row < len(self.visible_receptions):
            data = self.visible_receptions[row]
            reason = i18n.tr(data.host) + " → " + i18n.tr(data.guest)
            self.SetStatusText(reason) if self.GetStatusBar() else None

    def copyTable(self, event):
        page = self.tabs.GetPage(self.tabs.GetSelection())
        tables = {
            self.contact_page: self.contacts,
            self.angle_page: self.angle_table,
            self.lot_page: self.lot_table,
            self.reception_page: self.receptions,
            self.tabs.GetPage(4): self.connection_table,
            self.tabs.GetPage(5): self.horary_table,
        }
        if page is self.tabs.GetPage(6):
            table = (self.aversion_table if self.hellenistic_tabs.GetSelection() == 0
                     else self.ray_table)
        else:
            table = tables.get(page)
        if table is None:
            wx.MessageBox(i18n.tr("Select a table tab to copy."),
                          i18n.tr("Copy table"), wx.OK | wx.ICON_INFORMATION, self)
            return
        rows = ["\\t".join(table.GetColumn(i).GetText()
                          for i in range(table.GetColumnCount()))]
        for line in range(table.GetItemCount()):
            rows.append("\\t".join(table.GetItemText(line, i)
                         for i in range(table.GetColumnCount())))
        if wx.TheClipboard.Open():
            try:
                wx.TheClipboard.SetData(wx.TextDataObject("\\n".join(rows)))
            finally:
                wx.TheClipboard.Close()
