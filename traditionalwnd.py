"""Tables for the traditional analysis (traditional.py): planetary conditions,
reception/generosity/repulsion and the temperament worksheet."""

import html
import wx
import wx.html
import traditional
from hor_tools import output as hout
from hor_tools.rendering.pretty_report import _relation_rows
from hor_tools.rendering.technical import _position

CONDITIONS, RELATIONSHIPS, TEMPERAMENT = list(range(3))

TITLES = {
    CONDITIONS: 'Planetary conditions',
    RELATIONSHIPS: 'Reception, generosity, repulsion',
    TEMPERAMENT: 'Temperament',
}

GOOD = '#1a7f37'
BAD = '#b42318'
PALE = '#6e7781'


def _e(text):
    return html.escape(str(text))


def _table(headers, rows):
    out = ['<table border="1" cellspacing="0" cellpadding="4" width="100%">', '<tr bgcolor="#e8eaed">']
    out += ['<th align="left">%s</th>' % _e(h) for h in headers]
    out.append('</tr>')
    for row in rows:
        out.append('<tr>' + ''.join('<td valign="top">%s</td>' % cell for cell in row) + '</tr>')
    out.append('</table>')
    return '\n'.join(out)


def _color(text, color):
    return '<font color="%s">%s</font>' % (color, _e(text))


def _header(a, extra):
    ci = a.chart
    local = ci.datetime_utc.replace(tzinfo=None)
    rows = [('Chart', _e(ci.name)), ('UTC', _e(local.strftime('%Y-%m-%d %H:%M:%S')))] + extra
    return _table(['Item', 'Value'], rows)


def conditions_html(a):
    solar = a.technical.solar
    moon = next((r for r in a.reports if r.planet.name == 'Moon'), None)
    voc = moon is not None and moon.is_void_of_course
    head = _header(a, [
        ('Sect', '<b>%s</b>' % ('Day' if solar.is_day else 'Night')),
        ('Sun true altitude', '%+.4f&deg;' % solar.sun_true_altitude),
        ('Apparent sunrise / sunset', '%s / %s' % (solar.sunrise_local.strftime('%H:%M:%S'), solar.sunset_local.strftime('%H:%M:%S'))),
        ('Planetary day / hour ruler', '%s / %s' % (_e(a.technical.day_ruler), _e(a.technical.hour_ruler))),
        ('Moon void of course', _color('yes', BAD) if voc else 'no'),
    ])
    rows = []
    for r in a.reports:
        p = r.planet
        sect = '%s planet, %s' % (_e(r.sect_planet), _color('in sect', GOOD) if r.in_sect else _color('out of sect', PALE))
        hayz = [_color('hayz', GOOD) if r.hayz else '', _color('halb', GOOD) if r.halb else '']
        hayz = ', '.join(x for x in hayz if x) or _color('—', PALE)
        orient = '' if p.name == 'Sun' else ('oriental' if r.oriental else 'occidental')
        phase = _e(hout._format_synodic(r)) or _color('—', PALE)
        station = {'first': 'first station (turning retrograde)', 'second': 'second station (turning direct)'}.get(p.station or '', '')
        motion = '%s, %s, %.2f&deg;/day (%.2f&times; mean)' % ('retrograde' if p.retrograde else 'direct', _e(r.speed_class), abs(p.speed_long), r.speed_ratio)
        if r.speed_class.lower() == 'slow':
            motion = '<font color="%s">%s</font>' % (BAD, motion)
        lat = {'north_strengthening': _color('north: strengthening', GOOD), 'south_weakening': _color('south: weakening', BAD)}.get(r.latitude_condition, _color('on ecliptic', PALE))
        rows.append([
            '<b>%s</b>' % _e(p.name),
            _e(_position(p.longitude)),
            str(p.house),
            sect,
            hayz,
            _e(orient) or _color('—', PALE),
            phase,
            _e(station) or _color('—', PALE),
            motion,
            _color('joy', GOOD) if r.is_in_planetary_joy else _color('—', PALE),
            lat,
            _color('via combusta', BAD) if r.is_in_via_combusta else _color('—', PALE),
        ])
    table = _table(['Planet', 'Position', 'H', 'Sect', 'Hayz / halb', 'Orientation', 'Synodic phase', 'Station', 'Motion', 'Joy', 'Latitude', 'Via Combusta'], rows)
    note = '<p><font size="-1" color="%s">Sect from the Sun\'s true geometric altitude; whole-sign houses; Via Combusta 19&deg; Libra&ndash;3&deg; Scorpio.</font></p>' % PALE
    return head + '<p></p>' + table + note


def relationships_html(a):
    rows = [[_e(c) for c in row] for row in _relation_rows(a.reports)]
    if not rows:
        return _header(a, []) + '<p>No reception, generosity or repulsion in this chart.</p>'
    return _header(a, []) + '<p></p>' + _table(['Type', 'Direction', 'Basis', 'Contact'], rows)


def temperament_html(a):
    t = a.technical.temperament
    tot = t.totals
    head = _header(a, [
        ('Totals', 'K <b>%d</b> &middot; S <b>%d</b> &middot; M <b>%d</b> &middot; F <b>%d</b>' % (tot['K'], tot['S'], tot['M'], tot['F'])),
        ('Highest', '<b>%s</b>' % _e(', '.join(t.dominant))),
    ])
    rows = [[_e(row.factor), _e('; '.join(row.evidence) or '—')] + [str(row.scores[k]) for k in 'KSMF'] for row in t.rows]
    legend = '<p><font size="-1" color="%s">K choleric &middot; S sanguine &middot; M melancholic &middot; F phlegmatic</font></p>' % PALE
    return head + '<p></p>' + _table(['Factor', 'Evidence', 'K', 'S', 'M', 'F'], rows) + legend


RENDER = {CONDITIONS: conditions_html, RELATIONSHIPS: relationships_html, TEMPERAMENT: temperament_html}


def build_html(chrt, kind):
    try:
        body = RENDER[kind](traditional.analyse(chrt))
    except traditional.NotAvailable as e:
        body = '<p>Not available for this chart (%s).</p>' % _e(e)
    return '<html><body bgcolor="#ffffff"><h3>%s</h3>%s</body></html>' % (_e(TITLES[kind]), body)


class TraditionalFrame(wx.Frame):
    XSIZE = 980
    YSIZE = 520

    def __init__(self, parent, title, chrt, kind):
        wx.Frame.__init__(self, parent, -1, title+' - '+TITLES[kind], wx.DefaultPosition, wx.Size(TraditionalFrame.XSIZE, TraditionalFrame.YSIZE))
        self.kind = kind
        self.html = build_html(chrt, kind)
        self.w = wx.html.HtmlWindow(self, -1)
        self.w.SetPage(self.html)
        self.pmenu = wx.Menu()
        self.ID_SaveAsHtml = wx.NewIdRef()
        self.pmenu.Append(self.ID_SaveAsHtml, 'Save as HTML...', 'Save the table as an HTML file')
        self.w.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
        self.Bind(wx.EVT_MENU, self.onSaveAsHtml, id=self.ID_SaveAsHtml)
        self.SetMinSize((300, 200))

    def onPopupMenu(self, event):
        self.w.PopupMenu(self.pmenu, event.GetPosition())

    def onSaveAsHtml(self, event):
        dlg = wx.FileDialog(self, 'Save as HTML', '', TITLES[self.kind].replace(',', '')+'.html', 'HTML files (*.html)|*.html', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if not path.endswith('.html'):
                path += '.html'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.html.replace('<html>', '<html><head><meta charset="utf-8"></head>', 1))
        dlg.Destroy()
