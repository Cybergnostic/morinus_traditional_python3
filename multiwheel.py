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

    # Multiwheel has a denser drawing than a single Morinus chart. Do not
    # change chartstyle's global pens or the ordinary chart's appearance.
    LINE_WEIGHTS = {
        'major': 1.1, 'circle': 1.1, 'divider': .72,
        'pointer': .72, 'tick10': .76, 'tick1': .56,
    }
    LINE_FADE = {
        'major': .18, 'circle': .13, 'divider': .38,
        'pointer': .36, 'tick10': .32, 'tick1': .48,
    }

    def stroke_colour(self, colour, role):
        background = (255, 255, 255) if self.bw else tuple(self.options.clrbackground)
        return chartstyle.mix(self.colour(colour), background,
                              self.LINE_FADE.get(role, 0.0))

    def ink(self, role):
        pen = chartstyle.frame_pen(self.options, self.bw,
                                   min(self.width, self.height), role)
        c = pen.GetColour()
        colour = self.stroke_colour((c.Red(), c.Green(), c.Blue()), role)
        weight = self.LINE_WEIGHTS.get(role, 1.0)
        return colour, max(1, round(weight * self.scale))

    def stroke(self, a, b, role='divider', colour=None):
        ink, width = self.ink(role)
        if colour is not None:
            ink = self.stroke_colour(colour, role)
        self.draw.line((self.scaled(a), self.scaled(b)),
                       fill=ink, width=width)

    def scaled(self, xy):
        return (int(round(xy[0] * self.scale)),
                int(round(xy[1] * self.scale)))

    def circle(self, radius, role='circle', colour=None):
        ink, width = self.ink(role)
        if colour is not None:
            ink = self.stroke_colour(colour, role)
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
        """Draw all four chart-local axes with visible inward-based arrows.

        The normal GraphChart draws triangular ASC/MC arrowheads.  Scale the
        same triangles to multiwheel bands; mark all four axes explicitly so
        ASC, DSC, MC and IC remain readable in a crowded multiwheel.
        """
        asc, mc = (chrt.houses.ascmc[houses.Houses.ASC],
                   chrt.houses.ascmc[houses.Houses.MC])
        colour = colour if colour is not None else self.options.clrAscMC
        ink = self.stroke_colour(colour, 'major')
        size = min(8.5, max(5.5, (outer - inner) * .16))
        half_base = max(2.0, min(3.3, size * .42))
        for lon in wheel_primitives.angle_longitudes(asc, mc):
            display_lon = zodiac_lon(chrt, lon, self.options)
            tip_radius = outer - 1.8
            self.stroke(self.point(display_lon, inner),
                        self.point(display_lon, tip_radius - size),
                        'major', colour)
            theta = self.angle(display_lon)
            bx, by = self.point(display_lon, tip_radius - size)
            dx, dy = -math.sin(theta) * half_base, math.cos(theta) * half_base
            points = [self.scaled((bx + dx, by + dy)),
                      self.scaled((bx - dx, by - dy)),
                      self.scaled(self.point(display_lon, tip_radius))]
            self.draw.polygon(points, fill=ink)

    @staticmethod
    def dial_width(edges):
        inner, outer = edges
        return min(8.5, max(5.5, (outer - inner) * .14))

    def draw_degree_dial(self, edges, side):
        """A chart's own 360-degree dial, with 1/5/10-degree tick hierarchy.

        'outer': radial (inner) chart, with ticks immediately below its
        outer boundary.  'inner': additional charts, where a narrow dial
        sits just beyond the empty separator.  Returns the free label band
        and the true-longitude radius for pointer leaders.
        """
        inner, outer = edges
        width = self.dial_width(edges)
        if side == 'outer':
            base, far = outer - 1.0, outer - width
            label_edges = (inner + 1.0, far - 2.0)
            direction = -1.0
        elif side == 'inner':
            base, far = inner + 1.0, inner + width
            label_edges = (far + 2.0, outer - 2.0)
            direction = 1.0
        else:
            raise ValueError('Unknown planetary dial orientation')
        self.circle(base, 'divider')
        self.circle(far, 'divider')
        for degree in range(360):
            if degree % 30 == 0:
                length, role = width * .85, 'tick10'
            elif degree % 10 == 0:
                length, role = width * .70, 'tick10'
            elif degree % 5 == 0:
                length, role = width * .44, 'tick10'
            else:
                length, role = width * .21, 'tick1'
            self.stroke(self.point(degree, base),
                        self.point(degree, base + direction * length), role)
        return label_edges, base

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

    def draw_planet_band(self, chrt, edges, role, dial_side):
        """Morinus's glyph / degree / minute tiers with measured collision handling.

        Exact-longitude dials and leader lines are separate from displayed
        positions. A conjunction must stay visibly within its zodiac sign.
        """
        (inner, outer), dial_anchor = self.draw_degree_dial(edges, dial_side)
        width = outer - inner
        # Multiwheel uses the same radial hierarchy as GraphChart.  Reduce
        # font sizes only within reasonable bounds; zoom provides extra room.
        glyph_size = max(12, min(width * .26, self.rmax * .055))
        glyph_font = self.font(glyph_size, symbol=True)
        degree_font = self.font(max(9, glyph_size * .67))
        minute_font = self.font(max(9, glyph_size * .62))
        motion_font = self.font(max(9, glyph_size * .58), symbol=True)

        count = planets.Planets.BODIES_NUM
        lons = [self.longitude(chrt, i) for i in range(count)]
        positions = [wheel_primitives.position_text(lon, '°') for lon in lons]
        speeds = [chrt.planets.planets[i].data[planets.Planet.SPLON]
                  for i in range(count)]
        motions = [('S' if speed == 0 else common.common.retr)
                   if speed <= 0 else '' for speed in speeds]
        boxes = [
            (self.measure(common.common.planets[i], glyph_font),
             self.measure(positions[i][0], degree_font),
             self.measure(positions[i][1], minute_font),
             self.measure(motions[i], motion_font) if motions[i] else (0, 0))
            for i in range(count)
        ]
        asc = zodiac_lon(self.radix,
                         self.radix.houses.ascmc[houses.Houses.ASC],
                         self.options)
        placed, unresolved = multiwheel_layout.place_planet_clusters(
            lons, boxes, (inner, outer), asc)
        if unresolved:
            self.layout_issues.append((role, len(unresolved)))

        for i, (exact, location) in enumerate(zip(lons, placed)):
            displayed = location['longitude']
            theta = self.angle(displayed)
            gx, gy = location['glyph']
            dx, dy = location['degree']
            mx, my = location['minute']
            # The pure layout returns Cartesian offsets from the wheel's
            # centre. Keep hit testing in display pixel coordinates.
            glyph_xy = (self.cx + gx, self.cy + gy)
            degree_xy = (self.cx + dx, self.cy + dy)
            minute_xy = (self.cx + mx, self.cy + my)
            g_radius = math.hypot(gx, gy)
            m_radius = math.hypot(mx, my)
            if dial_side == 'inner':
                reach = wheel_primitives.radial_half_extent(boxes[i][2], theta)
                label_end = m_radius - reach - 1.0
            else:
                reach = wheel_primitives.radial_half_extent(boxes[i][0], theta)
                label_end = g_radius + reach + 1.0
            self.stroke(self.point(exact, dial_anchor),
                        self.point(displayed, label_end),
                        'pointer', self.planet_colour(i))
            tick = 2.8 if dial_side == 'inner' else -2.8
            self.stroke(self.point(exact, dial_anchor),
                        self.point(exact, dial_anchor + tick),
                        'major', self.planet_colour(i))
            colour = self.colour(self.planet_colour(i))
            wheel_primitives.optical_text_center(
                self.draw, self.scaled(glyph_xy),
                common.common.planets[i], glyph_font, colour)
            wheel_primitives.optical_text_center(
                self.draw, self.scaled(degree_xy),
                positions[i][0], degree_font, colour)
            wheel_primitives.optical_text_center(
                self.draw, self.scaled(minute_xy),
                positions[i][1], minute_font, colour)
            if motions[i] and location['motion'] is not None:
                motion_xy = (self.cx + location['motion'][0],
                             self.cy + location['motion'][1])
                wheel_primitives.optical_text_center(
                    self.draw, self.scaled(motion_xy),
                    motions[i], motion_font, colour)
            self.hits.append((glyph_xy, max(glyph_size * .7, 12),
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
        self.draw_planet_band(self.radix, (core * .67, core), i18n.tr('Radix'),
                              'outer')

    def traditional_font(self, edges):
        """Follow the small Morinus-planet glyph size used by GraphChart.

        GraphChart's small traditional ruler is 2/3 of the symbol size
        (typically about 1/18 of the chart radius). Limit it by this band's
        actual height for tri- and quad-wheels.
        """
        inner, outer = edges
        pixels = max(8, int(min((outer - inner) * .78,
                                 self.rmax / 18.0)))
        return self.font(pixels, symbol=True), pixels * self.scale

    def draw_decans(self, edges):
        """Shared GraphChart decan rulerships, precise tenth divisions.

        Use exactly the same glyph square-centering as GraphChart.drawDecans,
        rather than PIL's unrelated 'mm' text anchor.
        """
        if edges is None:
            return
        inner, outer = edges
        self.circle(inner, 'circle')
        self.circle(outer, 'circle')
        font, size = self.traditional_font(edges)
        middle = (inner + outer) / 2.0
        rulers = self.options.decans[self.options.seldecan]
        for centre, ruler, start in wheel_primitives.traditional_decan_markers(rulers):
            self.stroke(self.point(start, inner),
                        self.point(start, outer), 'divider')
            wheel_primitives.paint_glyph(
                self.draw, self.scaled(self.point(centre, middle)),
                common.common.planets[ruler], font, size,
                self.colour(self.options.clrsigns))

    def draw_terms(self, edges):
        """Use the *same unequal bounds* and glyph positioning as GraphChart."""
        if edges is None:
            return
        inner, outer = edges
        self.circle(inner, 'circle')
        self.circle(outer, 'circle')
        font, size = self.traditional_font(edges)
        middle = (inner + outer) / 2.0
        bounds = self.options.terms[self.options.selterm]
        for centre, ruler, endpoint in wheel_primitives.traditional_term_markers(bounds):
            self.stroke(self.point(endpoint, inner),
                        self.point(endpoint, outer), 'divider')
            wheel_primitives.paint_glyph(
                self.draw, self.scaled(self.point(centre, middle)),
                common.common.planets[ruler], font, size,
                self.colour(self.options.clrsigns))

    def draw_zodiac(self, edges):
        """One zodiac band for every chart, including Morinus degree ticks."""
        inner, outer = edges
        self.circle(inner, 'major')
        self.circle(outer, 'major')
        width = outer - inner
        # The degree ticks have their own inner lane; this third circle
        # closes it and frames the sign glyphs in a properly centred lane.
        sign_inner, _ = multiwheel_layout.zodiac_sign_lane(edges)
        self.circle(sign_inner, 'circle')
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
        font = self.font(max(10, width * 0.55), symbol=True)
        for sign in range(12):
            lon = sign * 30
            self.stroke(self.point(lon, inner), self.point(lon, outer), 'major')
            self.label(self.point(lon + 15, (sign_inner + outer) / 2.0),
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

    @staticmethod
    def chart_identity(chrt, default_kind=None):
        """Short, unmistakable chart identification for wheel screenshots."""
        kinds = {chart.Chart.RADIX: 'Radix',
                 chart.Chart.SOLAR: 'Solar return',
                 chart.Chart.LUNAR: 'Lunar return',
                 chart.Chart.REVOLUTION: 'Return',
                 chart.Chart.TRANSIT: 'Transits',
                 chart.Chart.HORARY: 'Horary'}
        kind = i18n.tr(kinds.get(chrt.htype, default_kind or 'Chart'))
        t = chrt.time
        date = '%04d-%02d-%02d' % (
            t.origyear, t.origmonth, t.origday)
        if t.bc:
            date += ' BC'
        name = str(chrt.name or '').strip()
        title = kind + (': ' + name if name else '')
        return title, '%s %02d:%02d' % (date, t.hour, t.minute)

    def draw_centre_identity(self):
        """Label the inner radix inside its otherwise empty central disk."""
        kind, detail = self.chart_identity(self.radix, 'Radix')
        title = kind
        title_font = self.font(max(9, min(12, self.rmax * .036)))
        detail_font = self.font(max(8, min(10, self.rmax * .030)))
        # Width must remain within the small centre disk at quad-wheel sizes.
        max_width = self.core_radius * .95
        while len(title) > 8 and self.measure(title, title_font)[0] > max_width:
            title = title[:-2] + '…'
        date_part = detail
        text_colour = (65, 65, 65) if self.bw else self.options.clrtexts
        background = (255, 255, 255) if self.bw else self.options.clrbackground
        # A small backing keeps the name legible even when aspects are on.
        tw = max(self.measure(title, title_font)[0],
                 self.measure(date_part, detail_font)[0])
        x, y = self.cx, self.cy
        rect = (self.scaled((x - tw / 2 - 6, y - 15)),
                self.scaled((x + tw / 2 + 6, y + 15)))
        self.draw.rectangle(rect, fill=self.colour(background))
        wheel_primitives.optical_text_center(
            self.draw, self.scaled((x, y - 7)), title,
            title_font, self.colour(text_colour))
        wheel_primitives.optical_text_center(
            self.draw, self.scaled((x, y + 7)), date_part,
            detail_font, self.colour(text_colour))

    def draw_outer_identity(self, chrt, index, edges):
        """Place each chart's name *inside its band* in a free field.

        Candidate positions near the top/bottom offer a wide horizontal
        chord. Prefer the one farthest from the chart's glyph positions;
        a tiny opaque backing keeps the caption legible over house lines.
        """
        kind, detail = self.chart_identity(chrt)
        inner, outer = edges
        front = self.font(max(8, min(10, (outer - inner) * .20)))
        secondary = self.font(max(8, min(9, (outer - inner) * .18)))
        max_width = min(self.rmax * .38, 118.0)
        while len(detail) > 8 and self.measure(detail, secondary)[0] > max_width:
            detail = detail[:-2] + '…'
        while len(kind) > 8 and self.measure(kind, front)[0] > max_width:
            kind = kind[:-2] + '…'
        w = max(self.measure(kind, front)[0],
                self.measure(detail, secondary)[0]) + 10
        h = 25.0
        radius = (inner + outer) / 2.0
        ring_hits = [xy for xy, extent, obj, *_ in self.hits if obj is chrt]
        candidates = (-math.pi / 2, math.pi / 2,
                      -math.pi * .43, math.pi * .43,
                      -math.pi * .57, math.pi * .57)
        ranked = []
        for theta in candidates:
            cx = self.cx + math.cos(theta) * radius
            cy = self.cy + math.sin(theta) * radius
            corners = ((cx - w / 2, cy - h / 2),
                       (cx + w / 2, cy - h / 2),
                       (cx - w / 2, cy + h / 2),
                       (cx + w / 2, cy + h / 2))
            corner_radii = [math.hypot(x - self.cx, y - self.cy)
                            for x, y in corners]
            if min(corner_radii) < inner + 2 or max(corner_radii) > outer - 2:
                continue
            nearest = min((math.hypot(cx - px, cy - py)
                           for px, py in ring_hits), default=1000.0)
            ranked.append((nearest, cx, cy))
        if not ranked:
            return  # Never spill chart labels outside their own ring.
        _, x, y = max(ranked)
        background = (255, 255, 255) if self.bw else chartstyle.mix(
            tuple(self.options.clrbackground), RING_COLOURS[index - 1],
            .065 + (index - 1) * .015)
        self.draw.rectangle(
            (self.scaled((x - w / 2, y - h / 2)),
             self.scaled((x + w / 2, y + h / 2))),
            fill=background)
        colour = (35, 35, 35) if self.bw else RING_COLOURS[index - 1]
        wheel_primitives.optical_text_center(
            self.draw, self.scaled((x, y - 6)), kind,
            front, self.colour(colour))
        wheel_primitives.optical_text_center(
            self.draw, self.scaled((x, y + 6)), detail,
            secondary, self.colour(colour))

    def draw_outer_ring(self, chrt, index, edges):
        """A chart-specific ring with Morinus notation and its own axes."""
        inner, outer = edges
        border = None if self.bw else RING_COLOURS[index - 1]
        separation = self.separator_width(edges)
        chart_start = inner + separation + 1
        self.draw_sign_spokes(chart_start, outer)
        self.draw_house_spokes(chrt, chart_start, outer, border)
        self.draw_angles(chrt, chart_start, outer, border)
        self.draw_planet_band(chrt, (chart_start, outer),
                              i18n.tr('Ring %d') % index, 'inner')

    @staticmethod
    def separator_width(edges):
        inner, outer = edges
        # Slim but visibly empty at all three wheel counts; the two lines
        # themselves are light single-pixel strokes after downsampling.
        return min(3.2, max(2.4, (outer - inner) * .055))

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
        self.core_radius = core
        bg = (255, 255, 255) if self.bw else tuple(self.options.clrbackground)
        image = Image.new('RGB', i18n.tr((self.width * self.scale,
                                  self.height * self.scale)), i18n.tr(bg))
        self.draw = ImageDraw.Draw(image)
        self.hits = []
        self.layout_issues = []
        self.draw_ring_backgrounds(zodiac, rings)
        self.draw_radix(core)
        self.draw_decans(decans)
        self.draw_terms(terms)
        self.draw_zodiac(zodiac)
        for index, (chrt, edges) in enumerate(zip(self.others, rings), 1):
            self.draw_outer_ring(chrt, index, edges)
        self.draw_separator_gaps(rings)
        # One continuous perimeter closes the entire multiwheel. Draw last
        # so house/angle spokes stop cleanly at the final edge.
        self.circle(rings[-1][1] - .6, 'circle',
                    None if self.bw else RING_COLOURS[len(rings) - 1])
        # Labels are part of the chart image (and therefore its PNG), not
        # only the window's selectors. Add them after separators are clear.
        self.draw_centre_identity()
        for index, (chrt, edges) in enumerate(zip(self.others, rings), 1):
            self.draw_outer_identity(chrt, index, edges)
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
        # Reflow only the multiwheel picker: a full-width chart choice above
        # the two source buttons fits a useful, compact left sidebar.
        old = self.GetSizer()
        old.Clear(delete_windows=False)
        controls = wx.BoxSizer(wx.HORIZONTAL)
        controls.Add(self.openbutton, 1, wx.RIGHT, 4)
        controls.Add(self.create_button, 1)
        column = wx.BoxSizer(wx.VERTICAL)
        column.Add(self.choice, 0, wx.EXPAND | wx.BOTTOM, 4)
        column.Add(controls, 0, wx.EXPAND)
        self.SetSizer(column)
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
        self.zoom_factor = None  # None = fit window; 1.0 = natural chart size
        self.sidebar_visible = True
        self.bitmap_origin = (0, 0)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)
        self.SetMinSize((760, 600))
        outer = wx.BoxSizer(wx.VERTICAL)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(wx.StaticText(self, label=i18n.tr('Outer charts:')), 0,
                wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.count_choice = wx.Choice(
            self, choices=i18n.tr(['1 (bi-wheel)', '2 (tri-wheel)', '3 (quad-wheel)']))
        self.count_choice.SetSelection(0)
        row.Add(self.count_choice, 0, wx.RIGHT, 15)
        row.Add(wx.StaticText(self, label=i18n.tr('Aspects between:')), 0,
                wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.aspect_choice = wx.Choice(
            self, choices=i18n.tr(['None', 'Radix only', 'Radix and ring 1']))
        self.aspect_choice.SetSelection(0)
        row.Add(self.aspect_choice, 0, wx.RIGHT, 15)
        self.fit_button = wx.Button(self, label=i18n.tr('Fit'))
        self.actual_button = wx.Button(self, label='100%')
        self.out_button = wx.Button(self, label='-')
        self.in_button = wx.Button(self, label='+')
        for control in (self.fit_button, self.actual_button,
                        self.out_button, self.in_button):
            row.Add(control, 0, wx.RIGHT, 4)
        self.side_button = wx.Button(self, label=i18n.tr('Hide charts'))
        row.Add(self.side_button, 0, wx.RIGHT, 8)
        self.savebutton = wx.Button(self, label=i18n.tr('Save image (PNG)...'))
        row.Add(self.savebutton)
        outer.Add(row, 0, wx.ALL, 7)

        # Put chart-source controls beside, not above, the drawing. This
        # recovers valuable vertical canvas space for the wheel itself.
        content = wx.BoxSizer(wx.HORIZONTAL)
        self.sidebar = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.sidebar.SetMinSize((302, 250))
        self.sidebar.SetScrollRate(0, 15)
        controls = wx.BoxSizer(wx.VERTICAL)
        self.radix_label = wx.StaticText(
            self.sidebar, label=i18n.tr('Inner radix') + ': ' +
            comparegrid.caption(mainfr.horoscope))
        self.radix_label.Wrap(292)
        controls.Add(self.radix_label, 0, wx.EXPAND | wx.BOTTOM, 12)
        self.pickers = []
        self.picker_rows = []
        for i in range(3):
            strip = wx.Panel(self.sidebar)
            line = wx.BoxSizer(wx.VERTICAL)
            tag = wx.StaticText(
                strip, label=i18n.tr('Ring %d') % (i + 1) + ':')
            if not self.options.bw:
                tag.SetForegroundColour(wx.Colour(*RING_COLOURS[i]))
            line.Add(tag, 0, wx.BOTTOM, 4)
            picker = OuterChartPicker(strip, mainfr, self.queue_draw, i + 1)
            line.Add(picker, 0, wx.EXPAND)
            strip.SetSizer(line)
            self.pickers.append(picker)
            self.picker_rows.append(strip)
            controls.Add(strip, 0, wx.EXPAND | wx.BOTTOM, 14)
            if i:
                strip.Hide()
        self.selection_note = wx.StaticText(self.sidebar, label='')
        self.selection_note.Wrap(290)
        controls.Add(self.selection_note, 0, wx.EXPAND | wx.BOTTOM, 8)
        self.sidebar.SetSizer(controls)
        content.Add(self.sidebar, 0, wx.EXPAND | wx.ALL, 7)

        # Real panning, not a bitmap scaled back into a small panel.
        self.canvas = wx.ScrolledWindow(self, style=wx.HSCROLL | wx.VSCROLL)
        self.canvas.SetMinSize((390, 390))
        self.canvas.SetScrollRate(20, 20)
        self.canvas.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        content.Add(self.canvas, 1, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, 7)
        outer.Add(content, 1, wx.EXPAND)
        self.SetSizer(outer)
        self.CreateStatusBar()
        self.Bind(wx.EVT_CHOICE, self.change_count, self.count_choice)
        self.Bind(wx.EVT_CHOICE, self.queue_draw, self.aspect_choice)
        self.Bind(wx.EVT_BUTTON, self.onSaveAsBitmap, self.savebutton)
        self.Bind(wx.EVT_BUTTON, self.zoom_fit, self.fit_button)
        self.Bind(wx.EVT_BUTTON, self.zoom_actual, self.actual_button)
        self.Bind(wx.EVT_BUTTON, self.zoom_in, self.in_button)
        self.Bind(wx.EVT_BUTTON, self.zoom_out, self.out_button)
        self.Bind(wx.EVT_BUTTON, self.toggle_sidebar, self.side_button)
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
        self.sidebar.Layout()
        self.sidebar.FitInside()
        self.Layout()
        self.queue_draw()

    def toggle_sidebar(self, event=None):
        self.sidebar_visible = not self.sidebar_visible
        self.sidebar.Show(self.sidebar_visible)
        self.side_button.SetLabel(i18n.tr(
            'Hide charts' if self.sidebar_visible else 'Show charts'))
        self.Layout()
        self.queue_draw()

    def zoom_fit(self, event=None):
        self.zoom_factor = None
        self.queue_draw()

    def zoom_actual(self, event=None):
        self.zoom_factor = 1.0
        self.queue_draw()

    def zoom_in(self, event=None):
        self.zoom_factor = min(3.0, (self.zoom_factor or .8) * 1.25)
        self.queue_draw()

    def zoom_out(self, event=None):
        self.zoom_factor = max(.4, (self.zoom_factor or 1.0) / 1.25)
        self.queue_draw()

    @staticmethod
    def natural_diameter(count):
        # Minimum useful pixel diameters for the three density levels.
        return {1: 920, 2: 1080, 3: 1280}[count]

    def canvas_size(self, count):
        w, h = self.canvas.GetClientSize()
        if self.zoom_factor is None:
            return max(100, w), max(100, h)
        diameter = int(self.natural_diameter(count) * self.zoom_factor)
        return diameter, diameter

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
        vw, vh = self.canvas.GetClientSize()
        if vw < 100 or vh < 100:
            return
        count = self.count_choice.GetSelection() + 1
        w, h = self.canvas_size(count)
        charts = [picker.selected() for picker in self.pickers[:count]]
        repeated = []
        seen = {id(self.mainfr.horoscope): i18n.tr('Radix')}
        for i, selected in enumerate(charts, 1):
            if id(selected) in seen:
                repeated.append(i18n.tr('Ring %d') % i + ' = ' + seen[id(selected)])
            else:
                seen[id(selected)] = i18n.tr('Ring %d') % i
        self.renderer = MultiWheel(self.mainfr.horoscope, charts,
                                   (w, h), self.options, self.options.bw)
        self.renderer.aspect_ring = aspect_ring_from_choice(
            self.aspect_choice.GetSelection())
        self.buffer = self.renderer.drawChart()
        notes = []
        if repeated:
            notes.append(i18n.tr('Repeated charts') + ': ' + ', '.join(repeated))
        if self.renderer.layout_issues:
            notes.append(i18n.tr('Crowded planetary labels: use 100% or zoom in'))
        self.selection_note.SetLabel('\n'.join(notes))
        self.selection_note.Wrap(290)
        self.sidebar.Layout()
        self.sidebar.FitInside()
        self.bitmap_origin = (max(0, (vw - w) // 2),
                              max(0, (vh - h) // 2))
        self.canvas.SetVirtualSize((max(vw, w), max(vh, h)))
        self.canvas.Refresh(False)

    def paint(self, event):
        dc = wx.AutoBufferedPaintDC(self.canvas)
        self.canvas.PrepareDC(dc)
        dc.Clear()
        if self.buffer is not None:
            dc.DrawBitmap(self.buffer, *self.bitmap_origin)

    def on_click(self, event):
        if self.renderer is not None:
            x, y = self.canvas.CalcUnscrolledPosition(event.GetPosition())
            x -= self.bitmap_origin[0]
            y -= self.bitmap_origin[1]
            self.SetStatusText(self.renderer.onClick((x, y)))

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
            # Export from a fresh high-resolution render. Never export
            # the reduced Fit-to-window bitmap.
            count = self.count_choice.GetSelection() + 1
            diameter = {1: 1600, 2: 2000, 3: 2400}[count]
            charts = [p.selected() for p in self.pickers[:count]]
            exporter = MultiWheel(self.mainfr.horoscope, charts,
                                  (diameter, diameter),
                                  self.options, self.options.bw)
            exporter.aspect_ring = aspect_ring_from_choice(
                self.aspect_choice.GetSelection())
            bitmap = exporter.drawChart()
            if bitmap.SaveFile(path, wx.BITMAP_TYPE_PNG):
                self.mainfr.fpathimgs = os.path.dirname(path)
        finally:
            dlg.Destroy()


def show(mainfr):
    frame = MultiWheelFrame(mainfr)
    frame.Show(True)
    return frame
