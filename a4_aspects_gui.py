"""A4 Hellenistic configurations workspace for all chart types."""
import wx
import i18n
import light_perfection
import hellenistic_aspects
import a3_aspects_gui
from traditional_aspects import PLANETS


def _column_table(parent, columns):
    sizer = wx.BoxSizer(wx.VERTICAL)
    table = wx.ListCtrl(parent, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    for number, (label, width) in enumerate(columns):
        table.InsertColumn(number, i18n.tr(label), width=width)
    sizer.Add(table, 1, wx.EXPAND | wx.ALL, 8)
    parent.SetSizer(sizer)
    return table


def install(frame):
    page = wx.Panel(frame.tabs)
    main = wx.BoxSizer(wx.VERTICAL)
    frame.hellenistic_tabs = wx.Notebook(page)
    aversions = wx.Panel(frame.hellenistic_tabs)
    rays = wx.Panel(frame.hellenistic_tabs)
    frame.aversion_table = _column_table(aversions, [
        ('Scope', 145), ('Planet', 115), ('Related to', 160),
        ('Signs', 190), ('Geometry', 90), ('Condition', 100),
        ('Mitigations', 560)])
    frame.ray_table = _column_table(rays, [
        ('Caster', 110), ('Target', 110), ('Aspect', 105),
        ('Caster sign', 100), ('Target sign', 100),
        ('Direction', 105), ('Overcoming', 105), ('Orb', 90),
        ('Within orb', 95), ('Counter-ray', 100), ('Aktinobolia', 105)])
    frame.hellenistic_tabs.AddPage(aversions, i18n.tr('Aversion & mitigations'))
    frame.hellenistic_tabs.AddPage(rays, i18n.tr('Rays & domination'))
    main.Add(frame.hellenistic_tabs, 1, wx.EXPAND)
    page.SetSizer(main)
    frame.tabs.InsertPage(4, page, i18n.tr('Hellenistic'))
    frame.tabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,
                    lambda event: on_open(frame, event))
    refresh(frame)


def on_open(frame, event):
    event.Skip()
    if frame.tabs.GetSelection() != 4:
        return
    if frame.a3_connection_events is None:
        wx.CallAfter(_first_connection_scan, frame)
    else:
        refresh(frame)


def _first_connection_scan(frame):
    # One A3 chronology is shared, not two competing definitions of
    # light-transfer validity. The A3 tab's 90-day horizon applies.
    if frame.a3_connection_events is None:
        a3_aspects_gui.analyze_connections(frame)
    refresh(frame)


def _methods_text(methods):
    result = []
    for method in methods:
        if method.startswith('Common domicile ruler: '):
            planet = method.split(': ', 1)[1]
            result.append(i18n.tr('Common domicile ruler') + ': ' + i18n.tr(planet))
        elif method.startswith('Translation via ') or method.startswith('Collection via '):
            label, planet = method.split(' via ', 1)
            result.append(i18n.tr(label) + ' ' + i18n.tr('via') + ' ' + i18n.tr(planet))
        elif method.endswith(' (sign)') or method.endswith(' (degree)'):
            label, grade = method.rsplit(' (', 1)
            result.append(i18n.tr(label) + ' (' + i18n.tr(grade[:-1]) + ')')
        else:
            result.append(i18n.tr(method))
    return ', '.join(result) if result else '—'


def refresh(frame):
    if not hasattr(frame, 'aversion_table'):
        return
    target = (PLANETS[frame.planet.GetSelection()-1]
              if frame.planet.GetSelection() > 0 else None)
    light = (light_perfection.connections(frame.chart, frame.a3_connection_events)
             if frame.a3_connection_events is not None else ())
    aversions, rays = hellenistic_aspects.analyze(frame.chart, light)
    frame.aversion_table.DeleteAllItems()
    frame.ray_table.DeleteAllItems()
    for row in aversions:
        if target and target not in (row.source, row.target):
            continue
        frame._insert(frame.aversion_table, (
            i18n.tr(row.scope), i18n.tr(row.source), i18n.tr(row.target),
            i18n.tr(row.source_sign) + ' / ' + i18n.tr(row.target_sign),
            i18n.tr(row.geometry), i18n.tr(row.condition),
            _methods_text(row.mitigations)))
    for row in rays:
        if target and target not in (row.caster, row.target):
            continue
        frame._insert(frame.ray_table, (
            i18n.tr(row.caster), i18n.tr(row.target), i18n.tr(row.aspect),
            i18n.tr(row.caster_sign), i18n.tr(row.target_sign),
            i18n.tr(row.direction), i18n.tr(row.overcoming),
            frame._degrees(row.degree_orb),
            i18n.tr('Yes' if row.in_orb else 'No'),
            i18n.tr('Yes' if row.close_counter_ray else 'No'),
            i18n.tr('Yes' if row.aktinobolia else 'No')))
