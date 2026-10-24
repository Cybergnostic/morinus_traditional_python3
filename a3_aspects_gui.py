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
        ('Method', 125), ('Mediator', 115), ('From', 120), ('To', 120),
        ('Separating aspect', 165), ('Applying aspect', 165),
        ('Exact contact (UT)', 345)], '')
    layout = connections.GetSizer()
    controls = wx.BoxSizer(wx.HORIZONTAL)
    controls.Add(wx.StaticText(connections, -1, i18n.tr('Search days') + ':'),
                 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 7)
    frame.connection_days = wx.SpinCtrl(connections, -1, min=1, max=180,
                                         initial=90, size=(80, -1))
    controls.Add(frame.connection_days, 0, wx.RIGHT, 12)
    scan_button = wx.Button(connections, -1, i18n.tr('Analyze connections'))
    scan_button.Bind(wx.EVT_BUTTON, lambda event: analyze_connections(frame))
    controls.Add(scan_button, 0)
    frame.connection_summary = wx.StaticText(connections, -1, '')
    layout.Insert(0, controls, 0, wx.EXPAND | wx.ALL, 9)
    layout.Insert(1, frame.connection_summary, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
    frame.tabs.InsertPage(2, connections, i18n.tr('Connections'))
    # Recompute when this tab is first selected rather than displaying
    # unverified natal translation/collection candidates.
    frame.tabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,
                    lambda event: on_tab_changed(frame, event))

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
    frame.horary_summary = wx.StaticText(horary, -1, i18n.tr('Select significators and analyze'))
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
    horary.SetSizer(outer)
    frame.tabs.InsertPage(3, horary, i18n.tr('Horary perfection'))
    frame.a3_connection_events = None
    frame.a3_connection_days = 0
    refresh_connections(frame)


def on_tab_changed(frame, event):
    event.Skip()
    if frame.tabs.GetSelection() == 2 and frame.a3_connection_events is None:
        wx.CallAfter(analyze_connections, frame)


def analyze_connections(frame):
    import aspect_event_adapter
    days = frame.connection_days.GetValue()
    wx.BeginBusyCursor()
    try:
        events = aspect_event_adapter.search(frame.chart, days)
    except Exception as exc:
        wx.MessageBox(str(exc), i18n.tr('Event search error'),
                      wx.OK | wx.ICON_ERROR, frame)
        return
    finally:
        wx.EndBusyCursor()
    frame.a3_connection_events = events
    frame.a3_connection_days = days
    refresh_connections(frame)


def refresh_connections(frame):
    if not hasattr(frame, 'connection_table'):
        return
    table = frame.connection_table
    table.DeleteAllItems()
    if frame.a3_connection_events is None:
        frame.connection_summary.SetLabel('')
        return
    current = frame.planet.GetSelection()
    chosen = PLANETS[current - 1] if current > 0 else None
    rows = light_perfection.connections(frame.chart, frame.a3_connection_events)
    visible = [row for row in rows if chosen is None or
               chosen in (row.actor, row.source, row.target)]
    for row in visible:
        times = ' / '.join(_ut_date(jd, frame.chart.time.cal == 0)
                           for jd in row.exact_times)
        frame._insert(table, (
            i18n.tr(row.kind), i18n.tr(row.actor), i18n.tr(row.source),
            i18n.tr(row.target), i18n.tr(row.source_aspect),
            i18n.tr(row.target_aspect), times))
    frame.connection_summary.SetLabel(
        i18n.tr('%d connections · %d days') %
        (len(visible), frame.a3_connection_days))
    if hasattr(frame, 'aversion_table'):
        import a4_aspects_gui
        a4_aspects_gui.refresh(frame)


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
    # Horary chronology is separate from the Connections search horizon.
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

