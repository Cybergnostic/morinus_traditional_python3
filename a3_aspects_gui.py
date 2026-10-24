"""A3 wxPython tabs. Calculations remain in testable, wx-free modules."""
import wx
import i18n
import light_perfection
import horary_impediments
from traditional_aspects import PLANETS


def install(frame):
    """Add universal Connections and signifier-specific Horary tabs to A2."""
    connections = wx.Panel(frame.tabs)
    frame.connection_table = frame._make_table(connections, [
        ('Method', 115), ('Mediator', 115), ('From', 110), ('To', 110),
        ('Separating / first', 155), ('Applying / second', 155),
        ('Event check', 185), ('Explanation', 400)],
        'Translation/collection candidates are found in all chart types. Event verification requires Analyze timeline.')
    frame.tabs.InsertPage(2, connections, i18n.tr('Connections'))

    horary = wx.Panel(frame.tabs)
    outer = wx.BoxSizer(wx.VERTICAL)
    controls = wx.BoxSizer(wx.HORIZONTAL)
    for label in ('Significator A', 'Significator B'):
        controls.Add(wx.StaticText(horary, -1, i18n.tr(label) + ':'),
                     0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        choice = wx.Choice(horary, -1, choices=i18n.tr(list(PLANETS)))
        choice.SetSelection(6 if label.endswith('A') else 1)
        if label.endswith('A'):
            frame.sig_first = choice
        else:
            frame.sig_second = choice
        controls.Add(choice, 0, wx.RIGHT, 14)
    controls.Add(wx.StaticText(horary, -1, i18n.tr('Days') + ':'),
                 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
    frame.horizon = wx.SpinCtrl(horary, -1, min=1, max=180, initial=30,
                                size=(78, -1))
    controls.Add(frame.horizon, 0, wx.RIGHT, 10)
    button = wx.Button(horary, -1, i18n.tr('Analyze timeline'))
    button.Bind(wx.EVT_BUTTON, lambda event: analyze_timeline(frame))
    controls.Add(button, 0)
    outer.Add(controls, 0, wx.ALL, 9)
    frame.horary_summary = wx.StaticText(horary, -1,
        i18n.tr('Choose two significators and Analyze timeline to calculate future contacts.'))
    outer.Add(frame.horary_summary, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
    outer.Add(wx.StaticText(horary, -1, i18n.tr('Perfection and impediments')),
              0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
    frame.horary_findings = wx.ListCtrl(horary, -1,
                                      style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    for col, (label, width) in enumerate([
            ('UT date', 165), ('Finding', 180), ('Actor', 120),
            ('Other planet', 130), ('Reason', 520)]):
        frame.horary_findings.InsertColumn(col, i18n.tr(label), width=width)
    frame.horary_findings.SetMinSize((-1, 165))
    outer.Add(frame.horary_findings, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
    outer.Add(wx.StaticText(horary, -1, i18n.tr('Chronological planetary events')),
              0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
    frame.horary_table = wx.ListCtrl(horary, -1,
                                     style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    for col, (label, width) in enumerate([
            ('UT date', 185), ('Event', 140), ('Planet A', 135),
            ('Planet B', 135), ('Aspect', 150), ('Days ahead', 115)]):
        frame.horary_table.InsertColumn(col, i18n.tr(label), width=width)
    outer.Add(frame.horary_table, 2, wx.EXPAND | wx.LEFT | wx.RIGHT, 9)
    note = wx.StaticText(horary, -1, i18n.tr(
        'The findings describe possible traditional impediments, not an automatic yes/no horary judgment. Reception and context must still be assessed.'))
    outer.Add(note, 0, wx.ALL, 9)
    horary.SetSizer(outer)
    frame.tabs.InsertPage(3, horary, i18n.tr('Horary perfection'))
    frame.a3_events = None
    refresh_connections(frame)


def refresh_connections(frame):
    if not hasattr(frame, 'connection_table'):
        return
    current = frame.planet.GetSelection()
    chosen = PLANETS[current - 1] if current > 0 else None
    rows = light_perfection.connections(frame.chart, frame.a3_events)
    table = frame.connection_table
    table.DeleteAllItems()
    for row in rows:
        if chosen is not None and chosen not in (row.actor, row.source, row.target):
            continue
        frame._insert(table, (
            i18n.tr(row.kind), i18n.tr(row.actor), i18n.tr(row.source),
            i18n.tr(row.target), i18n.tr(row.source_aspect),
            i18n.tr(row.target_aspect), i18n.tr(row.status),
            i18n.tr(row.detail)))


def _ut_date(jd, gregorian=True):
    import astrology
    cal = astrology.SE_GREG_CAL if gregorian else astrology.SE_JUL_CAL
    year, month, day, hours = astrology.swe_revjul(jd, cal)
    minutes = round(hours * 60)
    hh, mm = divmod(minutes, 60)
    if hh == 24:
        return f'{year:04d}-{month:02d}-{day:02d} 24:00 UT'
    return f'{year:04d}-{month:02d}-{day:02d} {hh:02d}:{mm:02d} UT'


def analyze_timeline(frame):
    first = PLANETS[frame.sig_first.GetSelection()]
    second = PLANETS[frame.sig_second.GetSelection()]
    if first == second:
        wx.MessageBox(i18n.tr('Choose two different significators.'),
                      i18n.tr('Horary perfection'), wx.OK | wx.ICON_INFORMATION, frame)
        return
    import aspect_event_adapter
    days = frame.horizon.GetValue()
    wx.BeginBusyCursor()
    try:
        events = aspect_event_adapter.search(frame.chart, days)
    except Exception as exc:
        wx.MessageBox(str(exc), i18n.tr('Event search error'),
                      wx.OK | wx.ICON_ERROR, frame)
        return
    finally:
        wx.EndBusyCursor()
    frame.a3_events = events
    # The horary-specific classifier is separate from the universal
    # translation/collection engine: do not impose these verdicts on natal.
    i = PLANETS.index(first)
    j = PLANETS.index(second)
    cell = frame.chart.aspmatrix[max(i, j)][min(i, j)]
    kind = cell.typ if cell.typ in range(5) else None
    initial = dict((name, (float(p.data[0]), float(p.data[3])))
                   for name, p in zip(PLANETS, frame.chart.planets.planets[:7]))
    positions_at = aspect_event_adapter.named_positions(frame.chart)
    review = horary_impediments.assess(
        events, first, second, kind, initial, positions_at, days)
    frame.horary_summary.SetLabel(i18n.tr(review.summary))
    findings = frame.horary_findings
    findings.DeleteAllItems()
    for f in review.findings:
        frame._insert(findings, (
            _ut_date(f.jd, frame.chart.time.cal == 0),
            i18n.tr(f.kind), i18n.tr(f.actor),
            i18n.tr(f.other) if f.other else '—', i18n.tr(f.detail)))
    _, significant = light_perfection.horary_timeline(events, first, second, days)
    table = frame.horary_table
    table.DeleteAllItems()
    start = frame.chart.time.jd
    for e in significant:
        if e.kind == 'aspect':
            asp = light_perfection.ASPECTS[e.aspect_index]
        else:
            asp = '—'
        frame._insert(table, (_ut_date(e.jd, frame.chart.time.cal == 0),
                              i18n.tr(e.kind.title()), i18n.tr(e.first),
                              i18n.tr(e.second) if e.second else '—',
                              i18n.tr(asp), f'{e.jd - start:.3f}'))
    refresh_connections(frame)
