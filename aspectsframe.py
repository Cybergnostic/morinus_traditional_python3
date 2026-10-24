"""Readable, native-wx aspects workspace with the Morinus classic matrix retained."""

import wx
import i18n
import aspectswnd
import aspect_workspace


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
            i18n.tr("Double application/separation: both planets individually approach/recede from exactness. Motion does not guarantee future perfection."))
        self.receptions = self._make_table(
            self.reception_page,
            [("Host", 115), ("Receives", 115), ("Classification", 105),
             ("Dignities held", 235), ("Contact", 120),
             ("Mutual", 85), ("Guest position", 155)],
            i18n.tr("The host receives the guest in its dignity when an aspect is within orb."))
        self.receptions.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onReceptionSelected)

        old_matrix = aspectswnd.AspectsWnd(classic_page, chrt, options, parent)
        classic_sizer = wx.BoxSizer(wx.VERTICAL)
        classic_sizer.Add(old_matrix, 1, wx.EXPAND)
        classic_page.SetSizer(classic_sizer)
        self.tabs.AddPage(self.contact_page, i18n.tr("Contacts"))
        self.tabs.AddPage(self.reception_page, i18n.tr("Receptions"))
        self.tabs.AddPage(classic_page, i18n.tr("Classic matrix"))
        root.Add(self.tabs, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
        panel.SetSizer(root)

        self.planet.Bind(wx.EVT_CHOICE, self.populate)
        self.generosity.Bind(wx.EVT_CHECKBOX, self.populate)
        refresh.Bind(wx.EVT_BUTTON, self.populate)
        copy.Bind(wx.EVT_BUTTON, self.copyTable)
        self.populate()

    def _make_table(self, parent, columns, note):
        outer = wx.BoxSizer(wx.VERTICAL)
        table = wx.ListCtrl(parent, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        for index, (heading, width) in enumerate(columns):
            table.InsertColumn(index, i18n.tr(heading), width=width)
        outer.Add(table, 1, wx.EXPAND | wx.ALL, 7)
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
        current = self.tabs.GetSelection()
        if current not in (0, 1):
            wx.MessageBox(i18n.tr("Select Contacts or Receptions to copy."),
                          i18n.tr("Copy table"), wx.OK | wx.ICON_INFORMATION, self)
            return
        table = self.contacts if current == 0 else self.receptions
        rows = []
        for index in range(table.GetItemCount()):
            rows.append("\t".join(table.GetItemText(index, col)
                                  for col in range(table.GetColumnCount())))
        if not rows:
            return
        labels = "\t".join(table.GetColumn(col).GetText()
                           for col in range(table.GetColumnCount()))
        if wx.TheClipboard.Open():
            try:
                wx.TheClipboard.SetData(wx.TextDataObject(labels + "\n" + "\n".join(rows)))
            finally:
                wx.TheClipboard.Close()
