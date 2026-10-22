"""Traditional bi-, tri- and quad-wheel: a separate renderer and chart window.

This intentionally never calls or changes graphchart.GraphChart for the
concentric wheel. The existing single and comparison views are unchanged.
"""
import i18n
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
import wheel_primitives
import planets
import util


SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
PLANET_NAMES = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus',
                'Mercury', 'Moon', 'North Node', 'South Node')

# Muted ring colours distinguish charts without replacing the planet colours.
RING_COLOURS = ((45, 96, 143), (150, 100, 44), (111, 80, 130))


def aspect_ring_from_choice(selection):
    """-1 means no aspect lines, 0 radix only, 1..3 radix to outer ring."""
    return selection - 1



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
        self.aspect_ring = -1  # -1 = none; 0 = radix only; 1..3 = radix to ring
        self.hits = []
        self.buffer = None

    def angle(self, lon):
        asc = zodiac_lon(self.radix,
                         self.radix.houses.ascmc[houses.Houses.ASC], self.options)
        return math.pi + math.radians(asc - lon)

    def point(self, lon, radius):
        asc = zodiac_lon(self.radix,
                         self.radix.houses.ascmc[houses.Houses.ASC], self.options)
        return wheel_primitives.polar_point(self.cx, self.cy, asc, lon, radius)

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

    def circle(self, radius, role='circle', colour=None):
        ink, width = self.ink(role)
        if colour is not None:
            ink = self.colour(colour)
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
        degree, minute = wheel_primitives.position_text(lon, '\N{DEGREE SIGN}')
        return degree + minute[:-1]

    def planet_colour(self, index):
        """Match GraphChart's planet colours, including its node fallback."""
        colors = self.options.clrplanets
        colour_index = min(index, planets.Planets.BODIES_NUM - 2)
        return colors[colour_index] if colour_index < len(colors) else self.options.clrtexts

    def draw_aspects(self, core):
        """Draw no aspects by default; optionally radix or one selected ring."""
        if self.aspect_ring < 0:
            return
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
        if self.aspect_ring > 0:
            other = self.others[self.aspect_ring - 1]
            for i, j, kind, a, b in cross_aspects(self.radix, other, self.options):
                self.stroke(self.point(a, r), self.point(b, r), 'divider',
                            self.options.clraspect[kind])

    def draw_house_spokes(self, chrt, inner, outer, colour=None):
        """The same twelve cusp longitudes used by GraphChart.drawHouses."""
        if not self.options.houses:
            return
        for house in range(1, houses.Houses.HOUSE_NUM + 1):
            lon = zodiac_lon(chrt, chrt.houses.cusps[house], self.options)
            self.stroke(self.point(lon, inner), self.point(lon, outer),
                        'divider', colour if colour is not None else self.options.clrhouses)

    def draw_angles(self, chrt, inner, outer, colour=None):
        """ASC/DSC/MC/IC for this chart, in the radix's shared orientation."""
        asc, mc = (chrt.houses.ascmc[houses.Houses.ASC],
                   chrt.houses.ascmc[houses.Houses.MC])
        colour = colour if colour is not None else self.options.clrAscMC
        for i, lon in enumerate(wheel_primitives.angle_longitudes(asc, mc)):
            display_lon = zodiac_lon(chrt, lon, self.options)
            a, b = self.point(display_lon, inner), self.point(display_lon, outer)
            self.stroke(a, b, 'major', colour)
            # Like GraphChart.drawAscMC, arrowheads mark ASC and MC only.
            if i in (0, 2):
                theta = self.angle(display_lon)
                delta = math.pi / 360.0
                x, y = self.cx, self.cy
                left = (x + math.cos(theta + delta) * (outer - 3),
                        y + math.sin(theta + delta) * (outer - 3))
                right = (x + math.cos(theta - delta) * (outer - 3),
                         y + math.sin(theta - delta) * (outer - 3))
                tip = self.point(display_lon, outer - 1)
                self.stroke(left, tip, 'pointer', colour)
                self.stroke(right, tip, 'pointer', colour)

    def draw_sign_spokes(self, inner, outer):
        """Continue sign divisions inside a planetary ring, never the zodiac."""
        for sign in range(12):
            lon = sign * 30.0
            self.stroke(self.point(lon, inner),
                        self.point(lon, outer), 'major')

    def draw_houses(self, core):
        """House numbers retain the inner Morinus chart's house-number ring."""
        if not self.options.houses:
            return
        cusps = self.radix.houses.cusps
        font = self.font(max(8, core * .06))
        for index in range(1, 13):
            lon = zodiac_lon(self.radix, cusps[index], self.options)
            next_lon = zodiac_lon(self.radix, cusps[index % 12 + 1], self.options)
            mid = (lon + (next_lon - lon) % 360 / 2) % 360
            self.label(self.point(mid, core * .61), str(index),
                       font, self.options.clrhousenumbers)

    def draw_planet_band(self, chrt, edges, role):
        """Draw all planets using the same glyph / degree / minute hierarchy.

        The one-line degree-minute label of the first prototype is replaced
        with Morinus's two inward text lines, including station and retrograde.
        """
        inner, outer = edges
        width = outer - inner
        positions = wheel_primitives.planet_band_radii(inner, outer)
        glyph_size = max(10, min(width * .27, self.rmax * .052))
        glyph_font = self.font(glyph_size, symbol=True)
        degree_font = self.font(max(8, glyph_size * .72))
        minute_font = self.font(max(8, glyph_size * .61))
        motion_font = self.font(max(8, glyph_size * .55), symbol=True)
        lons = [self.longitude(chrt, i) for i in range(planets.Planets.BODIES_NUM)]
        labels = [wheel_primitives.position_text(lon, '\N{DEGREE SIGN}') for lon in lons]

        # All three label rows participate in angular collision avoidance.
        tier_widths = (
            (positions['glyph'], glyph_font,
             [common.common.planets[i] for i in range(len(lons))]),
            (positions['degree'], degree_font, [p[0] for p in labels]),
            (positions['minute'], minute_font, [p[1] for p in labels]),
        )
        gap = max(
            math.degrees((max(self.measure(s, font)[0] for s in texts) + 4)
                         / max(radius, 1))
            for radius, font, texts in tier_widths)
        minimum = min(max(6.0, gap), 359.0 / len(lons))
        spread = multiwheel_layout.spread_longitudes(lons, minimum)
        for i, (exact, displayed) in enumerate(zip(lons, spread)):
            colour = self.planet_colour(i)
            self.stroke(self.point(exact, positions['tick']),
                        self.point(exact, outer - 1), 'pointer')
            xy = self.point(displayed, positions['glyph'])
            wheel_primitives.paint_glyph(
                self.draw, self.scaled(xy), common.common.planets[i],
                glyph_font, int(glyph_size * self.scale), self.colour(colour))
            wheel_primitives.paint_position_text(
                self.draw, self.scaled(self.point(displayed, positions['degree'])),
                labels[i][0], degree_font, self.colour(colour))
            wheel_primitives.paint_position_text(
                self.draw, self.scaled(self.point(displayed, positions['minute'])),
                labels[i][1], minute_font, self.colour(colour))
            speed = chrt.planets.planets[i].data[planets.Planet.SPLON]
            if speed <= 0:
                if speed == 0:
                    wheel_primitives.paint_position_text(
                        self.draw, self.scaled(self.point(displayed, positions['motion'])),
                        'S', minute_font, self.colour(colour))
                else:
                    wheel_primitives.paint_position_text(
                        self.draw, self.scaled(self.point(displayed, positions['motion'])),
                        common.common.retr, motion_font, self.colour(colour))
            self.hits.append((xy, max(glyph_size * .7, 12),
                              chrt, i, exact, role))

    def draw_radix(self, core):
        self.draw_aspects(core)
        self.draw_houses(core)
        self.draw_house_spokes(self.radix, core * .55, core)
        self.draw_angles(self.radix, core * .55, core)
        self.circle(core * .55)
        if self.options.houses:
            self.circle(core * .67, 'divider')
        self.circle(core)
        self.draw_planet_band(self.radix, (core * .67, core), i18n.tr('Radix'))

    def draw_decans(self, edges):
        """The one shared decan band, using Morinus's selected rulers."""
        if edges is None:
            return
        inner, outer = edges
        self.circle(inner, 'divider')
        self.circle(outer, 'divider')
        font = self.font(max(8, (outer - inner) * .72), symbol=True)
        for sign, rulers in enumerate(self.options.decans[self.options.seldecan]):
            for part, ruler in enumerate(rulers):
                start = sign * 30 + part * 10
                self.stroke(self.point(start, inner), self.point(start, outer), 'divider')
                self.label(self.point(start + 5, (inner + outer) / 2),
                           common.common.planets[ruler], font, self.options.clrsigns)

    def draw_terms(self, edges):
        """The one shared term band, using the existing selected terms."""
        if edges is None:
            return
        inner, outer = edges
        self.circle(inner, 'divider')
        self.circle(outer, 'divider')
        font = self.font(max(8, (outer - inner) * .72), symbol=True)
        for sign, divisions in enumerate(self.options.terms[self.options.selterm]):
            cursor = sign * 30.0
            for ruler, width in divisions:
                span = float(width)
                self.stroke(self.point(cursor, inner),
                            self.point(cursor, outer), 'divider')
                self.label(self.point(cursor + span / 2, (inner + outer) / 2),
                           common.common.planets[ruler], font, self.options.clrsigns)
                cursor += span

    def draw_zodiac(self, edges):
        """One zodiac band for every chart, including Morinus degree ticks."""
        inner, outer = edges
        self.circle(inner, 'major')
        self.circle(outer, 'major')
        width = outer - inner
        for degree in range(360):
            if degree % 30 == 0:
                continue
            if degree % 10 == 0:
                length, role = .28, 'tick10'
            elif degree % 5 == 0:
                length, role = .17, 'tick10'
            else:
                length, role = .09, 'tick1'
            self.stroke(self.point(degree, inner),
                        self.point(degree, inner + width * length), role)
        font = self.font(max(10, width * 0.58), symbol=True)
        for sign in range(12):
            lon = sign * 30
            self.stroke(self.point(lon, inner), self.point(lon, outer), 'major')
            self.label(self.point(lon + 15, inner + width * 0.65),
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

    def draw_ring_backgrounds(self, zodiac, rings):
        """Tint only planetary bands; keep the single shared zodiac untouched.

        Draw circles outside-in before all labels and ticks, avoiding masks
        or per-pixel image operations even when the canvas is resized.
        """
        background = (255, 255, 255) if self.bw else tuple(self.options.clrbackground)
        for i in reversed(range(len(rings))):
            outer = rings[i][1]
            if self.bw:
                shade = (249, 249, 249) if i % 2 == 0 else (240, 240, 240)
            else:
                accent = RING_COLOURS[i]
                shade = chartstyle.mix(background, accent, 0.065 + i * 0.015)
            xy = (int((self.cx - outer) * self.scale),
                  int((self.cy - outer) * self.scale),
                  int((self.cx + outer) * self.scale),
                  int((self.cy + outer) * self.scale))
            self.draw.ellipse(xy, fill=shade)
        inner = zodiac[1]
        xy = (int((self.cx - inner) * self.scale),
              int((self.cy - inner) * self.scale),
              int((self.cx + inner) * self.scale),
              int((self.cy + inner) * self.scale))
        self.draw.ellipse(xy, fill=background)

    def draw_outer_ring(self, chrt, index, edges):
        """A chart-specific ring with Morinus notation and its own axes."""
        inner, outer = edges
        border = None if self.bw else RING_COLOURS[index - 1]
        separation = self.separator_width(edges)
        chart_start = inner + separation + 1
        self.draw_sign_spokes(chart_start, outer)
        self.draw_house_spokes(chrt, chart_start, outer, border)
        self.draw_angles(chrt, chart_start, outer, border)
        self.draw_planet_band(chrt, edges, i18n.tr('Ring %d') % index)

    @staticmethod
    def separator_width(edges):
        inner, outer = edges
        return min(4.0, (outer - inner) * .075)

    def draw_separator_gaps(self, rings):
        """Erase the entire separator annulus, then draw its two borders.

        Painting last means *no* sign, house, or angle line can cross the gap.
        """
        background = (255, 255, 255) if self.bw else tuple(self.options.clrbackground)
        for index, edges in enumerate(rings):
            inner, _ = edges
            width = self.separator_width(edges)
            mid = inner + width * .5
            rect = (int((self.cx - mid) * self.scale),
                    int((self.cy - mid) * self.scale),
                    int((self.cx + mid) * self.scale),
                    int((self.cy + mid) * self.scale))
            self.draw.ellipse(rect, outline=background,
                              width=max(1, int(math.ceil(width * self.scale))))
            border = None if self.bw else RING_COLOURS[index]
            self.circle(inner, 'major', border)
            self.circle(inner + width, 'major', border)

    def drawChart(self):
        self.scale = 2  # crisp curves and glyphs after Lanczos downsampling
        self.cx, self.cy = self.width / 2.0, self.height / 2.0
        self.rmax = min(self.width, self.height) * .465
        core, decans, terms, zodiac, rings = multiwheel_layout.allocate_traditional_rings(
            self.rmax, len(self.others), self.options.showterms, self.options.showdecans)
        bg = (255, 255, 255) if self.bw else tuple(self.options.clrbackground)
        image = Image.new('RGB', i18n.tr((self.width * self.scale,
                                  self.height * self.scale)), i18n.tr(bg))
        self.draw = ImageDraw.Draw(image)
        self.hits = []
        self.draw_ring_backgrounds(zodiac, rings)
        self.draw_radix(core)
        self.draw_decans(decans)
        self.draw_terms(terms)
        self.draw_zodiac(zodiac)
        for index, (chrt, edges) in enumerate(zip(self.others, rings), 1):
            self.draw_outer_ring(chrt, index, edges)
        self.draw_separator_gaps(rings)
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
        sign = SIGNS[int(lon // 30) % 12]	# the Morinus degree label truncates minutes
        retro = ' (R)' if chrt.planets.planets[i].data[planets.Planet.SPLON] < 0 else ''
        return '%s: %s - %s %s%s  [%s]' % (
            role, i18n.tr(PLANET_NAMES[i]), self.degree_text(lon), i18n.tr(sign), retro, chrt.name)


class OuterChartPicker(comparegrid.ChartPicker):
    """Multi-wheel picker with Morinus's own return/transit creation dialogs."""

    def __init__(self, parent, mainfr, on_change, prefer=0):
        self.generated_labels = {}
        super().__init__(parent, mainfr, on_change, prefer)
        self.create_button = wx.Button(self, label=i18n.tr('Create chart...'))
        self.GetSizer().Add(self.create_button, 0, wx.LEFT, 5)
        self.create_button.Bind(wx.EVT_BUTTON, self.show_create_menu)

    def refresh(self, event=None):
        super().refresh(event)
        # Preserve generated chart identities in the list, even when their
        # independent transit/revolution windows are later closed.
        for i, (_, chrt) in enumerate(self.sources):
            label = self.generated_labels.get(id(chrt))
            if label:
                title = label + ': ' + comparegrid.caption(chrt)
                self.sources[i] = (title, chrt)
                self.choice.SetString(i, title)

    def show_create_menu(self, event):
        menu = wx.Menu()
        for label, kind in ((i18n.tr('Solar return...'), 3),
                            (i18n.tr('Lunar return...'), 6),
                            (i18n.tr('Transits...'), None)):
            item = menu.Append(wx.ID_ANY, label)
            menu.Bind(wx.EVT_MENU,
                      lambda e, requested=kind: self.create_chart(requested),
                      id=item.GetId())
        try:
            self.PopupMenu(menu)
        finally:
            menu.Destroy()

    def create_chart(self, kind):
        """Attach a chart returned by the existing Morinus dialogs.

        If the user cancels either dialog, no chart is created or selected.
        """
        import transitframe
        before = {id(w) for w in wx.GetTopLevelWindows()
                  if isinstance(w, transitframe.TransitFrame)}
        if kind is None:
            self.mainfr.onTransits(None)
        else:
            self.mainfr.onRevolutions(None, planet=kind)
        new = [w for w in wx.GetTopLevelWindows()
               if isinstance(w, transitframe.TransitFrame)
               and not w.IsBeingDeleted() and id(w) not in before]
        if not new:
            return
        chrt = new[-1].chart
        labels = {chart.Chart.SOLAR: i18n.tr('Solar return'),
                  chart.Chart.LUNAR: i18n.tr('Lunar return'),
                  chart.Chart.TRANSIT: i18n.tr('Transits')}
        label = labels.get(chrt.htype, i18n.tr('Return'))
        self.generated_labels[id(chrt)] = label
        self.loaded.append((label, chrt))
        self.refresh()
        self.choice.SetSelection(len(self.sources) - 1)
        self.on_change()


class MultiWheelFrame(wx.Frame):
    """Chart selection, aspect controls and a resizable multi-wheel canvas."""

    def __init__(self, mainfr):
        wx.Frame.__init__(self, mainfr, title=i18n.tr('Multi-wheel'), size=(950, 900))
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
        row.Add(wx.StaticText(self, label=i18n.tr('Outer charts:')), 0,
                wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.count_choice = wx.Choice(self, choices=i18n.tr(['1 (bi-wheel)', '2 (tri-wheel)', '3 (quad-wheel)']))
        self.count_choice.SetSelection(0)
        row.Add(self.count_choice, 0, wx.RIGHT, 20)
        row.Add(wx.StaticText(self, label=i18n.tr('Aspects between:')), 0,
                wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.aspect_choice = wx.Choice(
            self, choices=i18n.tr(['None', 'Radix only', 'Radix and ring 1']))
        self.aspect_choice.SetSelection(0)
        row.Add(self.aspect_choice, 0, wx.RIGHT, 15)
        self.savebutton = wx.Button(self, label=i18n.tr('Save image (PNG)...'))
        row.Add(self.savebutton)
        outer.Add(row, 0, wx.ALL, 9)
        self.radix_label = wx.StaticText(
            self, label=i18n.tr('Inner radix') + ': ' + comparegrid.caption(mainfr.horoscope))
        outer.Add(self.radix_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
        self.pickers = []
        self.picker_rows = []
        for i in range(3):
            strip = wx.Panel(self)
            line = wx.BoxSizer(wx.HORIZONTAL)
            tag = wx.StaticText(strip, label=i18n.tr('Ring %d') % (i + 1) + ':')
            tag.SetMinSize((75, -1))
            if not self.options.bw:
                tag.SetForegroundColour(wx.Colour(*RING_COLOURS[i]))
            line.Add(tag, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
            picker = OuterChartPicker(strip, mainfr, self.queue_draw, i + 1)
            line.Add(picker, 1, wx.EXPAND)
            strip.SetSizer(line)
            self.pickers.append(picker)
            self.picker_rows.append(strip)
            outer.Add(strip, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
            if i:
                strip.Hide()
        self.selection_note = wx.StaticText(self, label='')
        outer.Add(self.selection_note, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 9)
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
        for i, strip in enumerate(self.picker_rows):
            strip.Show(i < count)
        prior = self.aspect_choice.GetSelection()
        self.aspect_choice.Clear()
        self.aspect_choice.Append(i18n.tr('None'))
        self.aspect_choice.Append(i18n.tr('Radix only'))
        for i in range(count):
            self.aspect_choice.Append(i18n.tr('Radix and ring %d') % (i + 1))
        self.aspect_choice.SetSelection(min(max(prior, 0), count + 1))
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
        repeated = []
        seen = {id(self.mainfr.horoscope): i18n.tr('Radix')}
        for i, selected in enumerate(charts, 1):
            if id(selected) in seen:
                repeated.append(i18n.tr('Ring %d') % i + ' = ' + seen[id(selected)])
            else:
                seen[id(selected)] = i18n.tr('Ring %d') % i
        self.selection_note.SetLabel(
            i18n.tr('Repeated charts') + ': ' + ', '.join(repeated) if repeated else '')
        self.renderer = MultiWheel(self.mainfr.horoscope, charts,
                                   (w, h), self.options, self.options.bw)
        self.renderer.aspect_ring = aspect_ring_from_choice(self.aspect_choice.GetSelection())
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
        dlg = wx.FileDialog(self, i18n.tr('Save multi-wheel as PNG'),
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
