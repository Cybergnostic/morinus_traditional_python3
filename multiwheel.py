"""Traditional bi-, tri- and quad-wheel: a separate renderer and chart window.

This intentionally never calls or changes graphchart.GraphChart for the
concentric wheel. The existing single and comparison views are unchanged.
"""
import math
import os
import time as _time
import wx
from PIL import Image, ImageDraw

import chart
import chartstyle
import common
import comparegrid
import houses
import multiwheel_layout
import planets
import util


SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
PLANET_NAMES = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus',
                'Mercury', 'Moon', 'North Node', 'South Node')


def zodiac_lon(chrt, lon, options):
    """Display-space longitude, consistent with the configured zodiac."""
    return (lon - chrt.ayanamsha) % 360 if options.ayanamsha else lon % 360


def circular_distance(a, b):
    return abs((a - b + 180) % 360 - 180)


def cross_aspects(radix, secondary, options):
    """Radix-to-one-ring Ptolemaic aspects using Morinus planet orbs.

    Uses the same two planets' averaged orbs as Chart.calcPlsAspMatrix,
    without recalculating or replacing any Chart state.
    """
    out = []
    for i in range(planets.Planets.PLANETS_NUM):
        a = zodiac_lon(radix, radix.planets.planets[i].data[planets.Planet.LON], options)
        for j in range(planets.Planets.PLANETS_NUM):
            b = zodiac_lon(secondary, secondary.planets.planets[j].data[planets.Planet.LON], options)
            separation = circular_distance(a, b)
            orb = (options.orbs[i] + options.orbs[j]) / 2.0
            matches = [(abs(separation - angle), kind)
                       for kind, angle in enumerate(chart.Chart.Aspects)
                       if abs(separation - angle) <= orb]
            if matches:
                _, kind = min(matches)
                out.append((i, j, kind, a, b))
    return out


class MultiWheel:
    """Draw a radix and one to three further charts as concentric rings."""

    def __init__(self, radix, others, size, options, bw):
        if not 1 <= len(others) <= 3:
            raise ValueError('Expected 1 to 3 outer charts')
        self.radix = radix
        self.others = list(others)
        self.width = max(1, int(size[0]))
        self.height = max(1, int(size[1]))
        self.options = options
        self.bw = bool(bw)
        self.aspect_ring = 0  # 0 = radix only; otherwise 1..len(others)
        self.hits = []
        self.buffer = None

    def angle(self, lon):
        asc = zodiac_lon(self.radix,
                         self.radix.houses.ascmc[houses.Houses.ASC], self.options)
        return math.pi + math.radians(asc - lon)

    def point(self, lon, radius):
        theta = self.angle(lon)
        return (self.cx + math.cos(theta) * radius,
                self.cy + math.sin(theta) * radius)

    def colour(self, value):
        return (0, 0, 0) if self.bw else tuple(value)

    def ink(self, role):
        pen = chartstyle.frame_pen(self.options, self.bw,
                                   min(self.width, self.height), role)
        c = pen.GetColour()
        return (c.Red(), c.Green(), c.Blue()), max(1, pen.GetWidth() * self.scale)

    def stroke(self, a, b, role='divider', colour=None):
        ink, width = self.ink(role)
        if colour is not None:
            ink = self.colour(colour)
        self.draw.line((self.scaled(a), self.scaled(b)),
                       fill=ink, width=width)

    def scaled(self, xy):
        return (int(round(xy[0] * self.scale)),
                int(round(xy[1] * self.scale)))

    def circle(self, radius, role='circle'):
        ink, width = self.ink(role)
        x, y = self.cx, self.cy
        rect = (int((x - radius) * self.scale),
                int((y - radius) * self.scale),
                int((x + radius) * self.scale),
                int((y + radius) * self.scale))
        self.draw.ellipse(rect, outline=ink, width=width)

    def font(self, size, symbol=False):
        path = common.common.symbols if symbol else common.common.abc
        return util.truetype(path, max(8, int(size)) * self.scale)

    def label(self, xy, value, font, colour):
        self.draw.text(self.scaled(xy), value, font=font, anchor='mm',
                       fill=self.colour(colour))

    def longitude(self, chrt, index):
        return zodiac_lon(chrt,
                          chrt.planets.planets[index].data[planets.Planet.LON],
                          self.options)

    def degree_text(self, lon):
        n = int(lon % 30)
        minute = int(round((lon % 1) * 60))
        if minute == 60:
            n = (n + 1) % 30
            minute = 0
        return '%02d\N{DEGREE SIGN}%02d' % (n, minute)

    def draw_aspects(self, core):
        """Draw within-radix lines; optionally add links to ONE selected ring."""
        r = core * 0.52
        matrix = getattr(self.radix, 'aspmatrix', None)
        if matrix is not None:
            for i in range(planets.Planets.PLANETS_NUM):
                for j in range(i):
                    item = matrix[i][j]
                    kind = item.typ
                    if 0 <= kind < chart.Chart.ASPECT_NUM:
                        a = self.longitude(self.radix, i)
                        b = self.longitude(self.radix, j)
                        self.stroke(self.point(a, r), self.point(b, r), 'divider',
                                    self.options.clraspect[kind])
        if self.aspect_ring:
            other = self.others[self.aspect_ring - 1]
            for i, j, kind, a, b in cross_aspects(self.radix, other, self.options):
                self.stroke(self.point(a, r), self.point(b, r), 'divider',
                            self.options.clraspect[kind])

    def draw_houses(self, core):
        if not self.options.houses:
            return
        cusps = self.radix.houses.cusps
        fnt = self.font(max(8, core * 0.06))
        for index in range(1, 13):
            lon = zodiac_lon(self.radix, cusps[index], self.options)
            nextlon = zodiac_lon(self.radix, cusps[index % 12 + 1], self.options)
            # as in Morinus's wheel: the cusps and the house numbers outside the aspects
            self.stroke(self.point(lon, core * 0.55),
                        self.point(lon, core), 'major' if index in (1, 4, 7, 10) else 'divider')
            mid = (lon + (nextlon - lon) % 360 / 2) % 360
            self.label(self.point(mid, core * 0.61), str(index), fnt,
                       self.options.clrhousenumbers)

    def draw_radix(self, core):
        self.draw_aspects(core)
        self.draw_houses(core)
        self.circle(core * 0.55)
        if self.options.houses:
            self.circle(core * 0.67, 'divider')	# the ring of the house numbers
        self.circle(core)
        lons = [self.longitude(self.radix, i) for i in range(planets.Planets.BODIES_NUM)]
        radius = core * 0.78
        glyph = max(11, core * 0.115)
        spread = multiwheel_layout.spread_longitudes(
            lons, max(7.0, math.degrees((glyph + 3) / max(1, radius))))
        symbol_font = self.font(glyph, symbol=True)
        for i, (exact, displayed) in enumerate(zip(lons, spread)):
            self.stroke(self.point(exact, core * 0.89),
                        self.point(exact, core), 'pointer')
            xy = self.point(displayed, radius)
            clr = self.options.clrplanets[i] if i < len(self.options.clrplanets) else self.options.clrtexts
            self.label(xy, common.common.planets[i], symbol_font, clr)
            self.hits.append((xy, max(10, glyph * .65), self.radix, i, lons[i], 'Radix'))

    def draw_zodiac(self, edges):
        inner, outer = edges
        self.circle(inner, 'major')
        self.circle(outer, 'major')
        font = self.font(max(10, (outer - inner) * 0.58), symbol=True)
        for sign in range(12):
            lon = sign * 30
            self.stroke(self.point(lon, inner), self.point(lon, outer), 'major')
            self.label(self.point(lon + 15, (inner + outer) / 2),
                       common.common.signs[sign], font, self.options.clrsigns)

    def measure(self, text, font):
        """Logical width and height of a label."""
        left, top, right, bottom = self.draw.textbbox((0, 0), text, font=font, anchor='mm')
        return (right - left) / float(self.scale), (bottom - top) / float(self.scale)

    @staticmethod
    def reach(theta, w, h):
        """How far a w x h label centred on the ray at theta reaches along it:
        horizontal text is long across the ray at the top and bottom of the
        wheel, but along it at the sides."""
        return abs(math.cos(theta)) * w / 2.0 + abs(math.sin(theta)) * h / 2.0

    def draw_outer_ring(self, chrt, index, edges):
        """Each planet: a tick at its exact longitude on the inner edge, its glyph
        next to it and its degree (with the retrograde mark) at the outer edge,
        both placed by their real size so that they stay inside the band."""
        inner, outer = edges
        self.circle(inner, 'major')
        self.circle(outer, 'major')
        width = outer - inner
        tick = min(10, width * .15)
        glyph = max(10, min(width * 0.36, self.rmax * 0.05))
        glyph_font = self.font(glyph, symbol=True)
        n = planets.Planets.BODIES_NUM
        sizes = [self.measure(common.common.planets[i], glyph_font) for i in range(n)]
        gw = max(w for w, h in sizes)
        # the degree must fit beside the glyph across the band (at the sides of the wheel)
        dsize = max(7, min(glyph * 0.62, (width - tick - gw - 8) / 3.4))
        degree_font = self.font(dsize)
        retro_font = self.font(dsize, symbol=True)
        lons = [self.longitude(chrt, i) for i in range(n)]
        texts = [self.degree_text(lon) for lon in lons]
        retro = [chrt.planets.planets[i].data[planets.Planet.SPLON] < 0 for i in range(n)]
        rw, rh = self.measure(common.common.retr, retro_font)
        boxes = []
        for i in range(n):
            tw, th = self.measure(texts[i], degree_font)
            boxes.append((tw + (rw + 2 if retro[i] else 0), max(th, rh if retro[i] else 0), tw))
        widest = max(gw, max(b[0] for b in boxes))
        separation = math.degrees((widest + 4) / max(inner + width / 2.0, 1))
        spread = multiwheel_layout.spread_longitudes(lons, min(max(6.0, separation), 359.0 / n))
        for i, (exact, displayed) in enumerate(zip(lons, spread)):
            self.stroke(self.point(exact, inner + 1), self.point(exact, inner + tick), 'pointer')
            theta = self.angle(displayed)
            gw_i, gh_i = sizes[i]
            g_reach = self.reach(theta, gw_i, gh_i)
            cw, ch, tw = boxes[i]
            t_reach = self.reach(theta, cw, ch)
            g_r = inner + tick + 2 + g_reach
            t_r = max(outer - 3 - t_reach, g_r + g_reach + t_reach + 1)
            colour = (self.options.clrplanets[i] if i < len(self.options.clrplanets)
                      else self.options.clrtexts)
            xy = self.point(displayed, g_r)
            self.label(xy, common.common.planets[i], glyph_font, colour)
            cx, cy = self.point(displayed, t_r)
            self.label((cx - (cw - tw) / 2.0, cy), texts[i], degree_font, self.options.clrtexts)
            if retro[i]:
                self.label((cx + cw / 2.0 - rw / 2.0, cy), common.common.retr, retro_font, colour)
            self.hits.append((xy, max(glyph * .7, 12), chrt, i, exact, 'Ring %d' % index))

    def drawChart(self):
        self.scale = 2  # crisp curves and glyphs after Lanczos downsampling
        self.cx, self.cy = self.width / 2.0, self.height / 2.0
        self.rmax = min(self.width, self.height) * .465
        core, zodiac, rings = multiwheel_layout.allocate_rings(
            self.rmax, len(self.others))
        bg = (255, 255, 255) if self.bw else tuple(self.options.clrbackground)
        image = Image.new('RGB', (self.width * self.scale,
                                  self.height * self.scale), bg)
        self.draw = ImageDraw.Draw(image)
        self.hits = []
        self.draw_radix(core)
        self.draw_zodiac(zodiac)
        for index, (chrt, edges) in enumerate(zip(self.others, rings), 1):
            self.draw_outer_ring(chrt, index, edges)
        image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        out = wx.Image(self.width, self.height)
        out.SetData(image.tobytes())
        self.buffer = wx.Bitmap(out)
        return self.buffer

    def onClick(self, position):
        x, y = position
        hits = [(math.hypot(x - xy[0], y - xy[1]), chrt, i, lon, role)
                for xy, extent, chrt, i, lon, role in self.hits
                if math.hypot(x - xy[0], y - xy[1]) <= extent]
        if not hits:
            return ''
        _, chrt, i, lon, role = min(hits, key=lambda item: item[0])
        sign = SIGNS[int((lon + 0.5 / 60) // 30) % 12]	# as degree_text rounds to the minute
        retro = ' (R)' if chrt.planets.planets[i].data[planets.Planet.SPLON] < 0 else ''
        return '%s: %s - %s %s%s  [%s]' % (
            role, PLANET_NAMES[i], self.degree_text(lon), sign, retro, chrt.name)


class MultiWheelFrame(wx.Frame):
    """Chart selection, aspect controls and a resizable multi-wheel canvas."""

    def __init__(self, mainfr):
        wx.Frame.__init__(self, mainfr, title='Multi-wheel', size=(950, 900))
        self.mainfr = mainfr
        self.options = mainfr.options
        self.buffer = None
        self.renderer = None
        self.pending = None
        self._alive = True
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)
        self.SetMinSize((650, 660))
        outer = wx.BoxSizer(wx.VERTICAL)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(wx.StaticText(self, label='Outer charts:'), 0,
                wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.count_choice = wx.Choice(self, choices=['1 (bi-wheel)', '2 (tri-wheel)', '3 (quad-wheel)'])
        self.count_choice.SetSelection(0)
        row.Add(self.count_choice, 0, wx.RIGHT, 20)
        row.Add(wx.StaticText(self, label='Aspects between:'), 0,
                wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.aspect_choice = wx.Choice(self, choices=['Radix only', 'Radix and ring 1'])
        self.aspect_choice.SetSelection(0)
        row.Add(self.aspect_choice, 0, wx.RIGHT, 15)
        self.savebutton = wx.Button(self, label='Save image (PNG)...')
        row.Add(self.savebutton)
        outer.Add(row, 0, wx.ALL, 9)
        self.pickers = []
        for i in range(3):
            picker = comparegrid.ChartPicker(self, mainfr, self.queue_draw, i + 1)
            self.pickers.append(picker)
            outer.Add(picker, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
            if i:
                picker.Hide()
        self.canvas = wx.Panel(self)
        self.canvas.SetMinSize((420, 420))
        self.canvas.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        outer.Add(self.canvas, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        self.SetSizer(outer)
        self.CreateStatusBar()
        self.Bind(wx.EVT_CHOICE, self.change_count, self.count_choice)
        self.Bind(wx.EVT_CHOICE, self.queue_draw, self.aspect_choice)
        self.Bind(wx.EVT_BUTTON, self.onSaveAsBitmap, self.savebutton)
        self.canvas.Bind(wx.EVT_PAINT, self.paint)
        self.canvas.Bind(wx.EVT_SIZE, self.resize)
        self.canvas.Bind(wx.EVT_LEFT_UP, self.on_click)
        self.Bind(wx.EVT_ACTIVATE, lambda e: (comparegrid.refresh_pickers(self.pickers) if e.GetActive() else None, e.Skip()))
        self.CentreOnParent()
        wx.CallAfter(self.queue_draw)

    def change_count(self, event=None):
        count = self.count_choice.GetSelection() + 1
        for i, picker in enumerate(self.pickers):
            picker.Show(i < count)
        prior = self.aspect_choice.GetSelection()
        self.aspect_choice.Clear()
        self.aspect_choice.Append('Radix only')
        for i in range(count):
            self.aspect_choice.Append('Radix and ring %d' % (i + 1))
        self.aspect_choice.SetSelection(min(max(prior, 0), count))
        self.Layout()
        self.queue_draw()

    def resize(self, event):
        self.queue_draw()
        event.Skip()

    def on_destroy(self, event):
        if event.GetEventObject() is self:
            self._alive = False
            if self.pending is not None:
                self.pending.Stop()
                self.pending = None
        event.Skip()

    def queue_draw(self, event=None):
        if self._alive and self.pending is None:
            self.pending = wx.CallLater(100, self.redraw)

    def redraw(self):
        self.pending = None
        if not self._alive:
            return
        try:
            if self.IsBeingDeleted() or not self.IsShown():
                return
        except RuntimeError:
            return
        w, h = self.canvas.GetClientSize()
        if w < 100 or h < 100:
            return
        count = self.count_choice.GetSelection() + 1
        charts = [picker.selected() for picker in self.pickers[:count]]
        self.renderer = MultiWheel(self.mainfr.horoscope, charts,
                                   (w, h), self.options, self.options.bw)
        self.renderer.aspect_ring = max(0, self.aspect_choice.GetSelection())
        self.buffer = self.renderer.drawChart()
        self.canvas.Refresh(False)

    def paint(self, event):
        if self.buffer is None:
            wx.PaintDC(self.canvas)
        else:
            wx.BufferedPaintDC(self.canvas, self.buffer)

    def on_click(self, event):
        if self.renderer is not None:
            self.SetStatusText(self.renderer.onClick(event.GetPosition()))

    def onSaveAsBitmap(self, event):
        if self.buffer is None:
            self.redraw()
        if self.buffer is None:
            return
        folder = self.mainfr.fpathimgs
        dlg = wx.FileDialog(self, 'Save multi-wheel as PNG',
                            folder if os.path.isdir(folder) else '.',
                            'multiwheel.png', 'PNG images (*.png)|*.png',
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        try:
            if dlg.ShowModal() != wx.ID_OK:
                return
            path = dlg.GetPath()
            if not path.lower().endswith('.png'):
                path += '.png'
            if self.buffer.SaveFile(path, wx.BITMAP_TYPE_PNG):
                self.mainfr.fpathimgs = os.path.dirname(path)
        finally:
            dlg.Destroy()


def show(mainfr):
    frame = MultiWheelFrame(mainfr)
    frame.Show(True)
    return frame
