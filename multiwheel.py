"""Traditional bi-, tri- and quad-wheel: a separate renderer and chart window.

This intentionally never calls or changes graphchart.GraphChart for the
concentric wheel. The existing single and comparison views are unchanged.
"""
import i18n
import math
import os
import time as _time
from collections import OrderedDict
from datetime import datetime, timezone
import wx
from PIL import Image, ImageDraw

import chart
import chartstyle
import common
import comparegrid
import houses
import multiwheel_layout
import multiwheel_highlight
import multiwheel_returnnav
import multiwheel_sources
import multiwheel_time
import wheel_primitives
import planets
import returnslist
import util


SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
PLANET_NAMES = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus',
                'Mercury', 'Moon', 'North Node', 'South Node')

# Muted ring colours distinguish charts without replacing the planet colours.
RING_COLOURS = ((45, 96, 143), (150, 100, 44), (111, 80, 130))


def aspect_ring_from_choice(selection):
    """-1 means none, 0 inner chart, 1..3 inner to an outer ring."""
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
    """Draw any inner chart and one to three others as concentric rings."""

    def __init__(self, radix, others, size, options, bw):
        if not 1 <= len(others) <= 3:
            raise ValueError('Expected 1 to 3 outer charts')
        self.radix = radix
        self.others = list(others)
        self.width = max(1, int(size[0]))
        self.height = max(1, int(size[1]))
        self.options = options
        self.bw = bool(bw)
        self.aspect_ring = -1  # -1 = none; 0 = inner; 1..3 = inner to ring
        self.reference_outside = True  # Exterior reference bands are the default.
        self.hits = []
        self.buffer = None
        self._ink_cache = {}
        self._font_cache = {}
        self.highlight_entries = []
        self.highlight_areas = []
        self.highlight_legend = []
        self.show_highlights = False
        self._highlight_lookup = {}

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
        cached = self._ink_cache.get(role)
        if cached is not None:
            return cached
        pen = chartstyle.frame_pen(self.options, self.bw,
                                   min(self.width, self.height), role)
        c = pen.GetColour()
        colour = self.stroke_colour((c.Red(), c.Green(), c.Blue()), role)
        weight = self.LINE_WEIGHTS.get(role, 1.0)
        result = colour, max(1, round(weight * self.scale))
        self._ink_cache[role] = result
        return result

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
        pixels = max(8, int(size)) * self.scale
        key = (path, pixels)
        font = self._font_cache.get(key)
        if font is None:
            font = util.truetype(path, pixels)
            self._font_cache[key] = font
        return font

    def label(self, xy, value, font, colour):
        self.draw.text(self.scaled(xy), value, font=font, anchor='mm',
                       fill=self.colour(colour))

    def longitude(self, chrt, index):
        return zodiac_lon(chrt,
                          chrt.planets.planets[index].data[planets.Planet.LON],
                          self.options)

    def degree_text(self, lon):
        degree, minute = wheel_primitives.position_text(lon, '\N{DEGREE SIGN}')
        return degree + minute

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

    def draw_zodiac_guides(self, chrt, inner, outer, ring_index=None):
        """Faint zodiac dividers within this field; house cusps take priority.

        The exact same zodiac boundaries apply to each chart, but never
        project house cusps from one chart into another. In Whole Sign,
        every sign boundary already has a house line, so skip its guide.
        """
        cusps = ([zodiac_lon(chrt, chrt.houses.cusps[house], self.options)
                  for house in range(1, houses.Houses.HOUSE_NUM + 1)]
                 if self.options.houses else None)
        divisions = wheel_primitives.zodiac_guide_longitudes(cusps)
        background = self.ring_background_colour(ring_index)
        # Zodiac = a neutral, quiet reference; cusps retain the stronger
        # chart-specific ring colour. Mix with actual band tint, not white.
        ink = chartstyle.mix(self.colour(self.options.clrsigns), background, .76)
        width = max(1, round(.55 * self.scale))
        for lon in divisions:
            start, end = self.point(lon, inner + 1.25), self.point(lon, outer - 1.25)
            self.draw.line((self.scaled(start), self.scaled(end)),
                           fill=ink, width=width)

    def draw_house_spokes(self, chrt, inner, outer, colour=None):
        """Only this chart's house cusps, ending inside its own field.

        The shared zodiac/reference strips never inherit these spokes,
        and another chart never receives a projected set of radix cusps.
        """
        if not self.options.houses:
            return
        cusps = [zodiac_lon(chrt, chrt.houses.cusps[house], self.options)
                 for house in range(1, houses.Houses.HOUSE_NUM + 1)]
        ink = colour if colour is not None else self.options.clrhouses
        for lon, start, finish in wheel_primitives.house_spoke_segments(
                cusps, inner, outer):
            self.stroke(self.point(lon, start), self.point(lon, finish),
                        'divider', ink)

    def ring_background_colour(self, ring_index=None):
        """Actual chart-field background, also used behind hollow angle ends."""
        background = (255, 255, 255) if self.bw else tuple(self.options.clrbackground)
        if ring_index is None:
            return background
        i = ring_index - 1
        if self.bw:
            return (249, 249, 249) if i % 2 == 0 else (240, 240, 240)
        return chartstyle.mix(background, RING_COLOURS[i],
                              0.065 + i * 0.015)

    def draw_angle_arrowhead(self, lon, tip_radius, size, colour):
        """An outward triangular end, used only for DESC and MC."""
        theta = self.angle(lon)
        half_base = max(2.0, min(3.3, size * .42))
        bx, by = self.point(lon, tip_radius - size)
        dx, dy = -math.sin(theta) * half_base, math.cos(theta) * half_base
        self.draw.polygon(
            [self.scaled((bx + dx, by + dy)),
             self.scaled((bx - dx, by - dy)),
             self.scaled(self.point(lon, tip_radius))],
            fill=self.stroke_colour(colour, 'major'))

    def draw_angle_open_circle(self, lon, centre_radius, marker_radius,
                               colour, ring_index=None):
        """Hollow ASC end, with the field colour covering any cusp beneath."""
        x, y = self.point(lon, centre_radius)
        rect = (self.scaled((x - marker_radius, y - marker_radius)),
                self.scaled((x + marker_radius, y + marker_radius)))
        self.draw.ellipse(
            rect, fill=self.ring_background_colour(ring_index),
            outline=self.stroke_colour(colour, 'major'),
            width=self.ink('major')[1])

    def draw_angles(self, chrt, inner, outer, colour=None, ring_index=None):
        """Chart-local angle ends: ASC open circle, DESC/MC arrows, IC line.

        All four axes keep their exact ecliptic longitudes and stay inside
        the chart's planetary field. Markers are the same for every wheel.
        """
        asc, mc = (chrt.houses.ascmc[houses.Houses.ASC],
                   chrt.houses.ascmc[houses.Houses.MC])
        colour = colour if colour is not None else self.options.clrAscMC
        size = min(8.5, max(5.5, (outer - inner) * .16))
        tip_radius = outer - 1.8
        for kind, lon in enumerate(wheel_primitives.angle_longitudes(asc, mc)):
            display_lon = zodiac_lon(chrt, lon, self.options)
            if kind == 0:  # ASC: hollow fishing-hook-like beginning
                radius = min(4.0, max(2.8, (outer - inner) * .075))
                centre_radius = tip_radius - radius
                self.stroke(self.point(display_lon, inner),
                            self.point(display_lon, centre_radius - radius),
                            'major', colour)
                self.draw_angle_open_circle(
                    display_lon, centre_radius, radius, colour, ring_index)
            elif kind in (1, 2):  # DESC and MC: triangular arrowheads
                self.stroke(self.point(display_lon, inner),
                            self.point(display_lon, tip_radius - size),
                            'major', colour)
                self.draw_angle_arrowhead(display_lon, tip_radius, size, colour)
            else:  # IC: plain axis line
                self.stroke(self.point(display_lon, inner),
                            self.point(display_lon, tip_radius),
                            'major', colour)

    @staticmethod
    def dial_width(edges):
        inner, outer = edges
        return min(8.5, max(5.5, (outer - inner) * .14))

    @classmethod
    def planet_label_edges(cls, edges, side):
        """Usable planetary text band after reserving a local degree dial."""
        inner, outer = edges
        width = cls.dial_width(edges)
        if side == 'outer':
            return inner + 1.0, outer - width - 2.0
        if side == 'inner':
            return inner + width + 2.0, outer - 2.0
        raise ValueError('Unknown planetary dial orientation')

    def prepare_planet_fonts(self, core, rings):
        """Choose exactly one glyph/degree/minute size for all chart layers."""
        label_widths = []
        core_edges = self.planet_label_edges((core * .67, core), 'outer')
        label_widths.append(core_edges[1] - core_edges[0])
        for edges in rings:
            inner, outer = edges
            chart_start = inner + self.separator_width(edges) + 1
            text_edges = self.planet_label_edges((chart_start, outer), 'inner')
            label_widths.append(text_edges[1] - text_edges[0])
        self.planet_fonts = multiwheel_layout.shared_planet_font_sizes(
            self.rmax, label_widths)

    def adapt_planet_fonts(self, core, rings):
        """Shrink *all* planet glyph/degree pairs when a chart is crowded.

        A glyph-only layout can look clear even though its degree overlaps
        its neighbour. Check the complete fixed-gap pairs before choosing
        one font size for every chart. Never shrink individual planets.
        """
        nominal = self.planet_fonts['glyph']
        minimum = max(12, int(nominal * .68))
        asc = zodiac_lon(self.radix,
                         self.radix.houses.ascmc[houses.Houses.ASC],
                         self.options)
        fields = [(self.radix,
                   self.planet_label_edges((core * .67, core), 'outer'))]
        for chrt, edges in zip(self.others, rings):
            start = edges[0] + self.separator_width(edges) + 1
            fields.append((chrt,
                           self.planet_label_edges((start, edges[1]), 'inner')))
        for size in range(nominal, minimum - 1, -1):
            font = self.font(size, symbol=True)
            boxes = [self.measure(common.common.planets[i], font)
                     for i in range(planets.Planets.BODIES_NUM)]
            self.planet_fonts.update({
                'glyph': size,
                'degree': max(8, int(size * .46)),
                'minute': max(8, int(size * .42)),
                'motion': max(8, int(size * .42)),
            })
            degree_font = self.font(self.planet_fonts['degree'])
            clear = True
            for ring_index, (chrt, edges) in enumerate(fields):
                lons = [self.longitude(chrt, i)
                        for i in range(planets.Planets.BODIES_NUM)]
                cusps = ([zodiac_lon(chrt, chrt.houses.cusps[j], self.options)
                          for j in range(1, houses.Houses.HOUSE_NUM + 1)]
                         if self.options.houses else None)
                if getattr(self, 'label_mode', 0):
                    text_boxes = []
                    for i, lon in enumerate(lons):
                        speed = chrt.planets.planets[i].data[planets.Planet.SPLON]
                        label, marker = self.position_label_parts(
                            lon, speed, self.label_mode)
                        marker_font = self.font(
                            self.planet_fonts['motion'], symbol=(speed < 0))
                        text_boxes.append(self.position_label_size(
                            label, marker, degree_font, marker_font))
                    # Radix dial lies outward; other rings have inner dials.
                    direction = -1 if ring_index == 0 else 1
                    placed, unresolved = multiwheel_layout.place_planet_label_groups(
                        lons, boxes, text_boxes, edges, asc, direction,
                        house_cusps=cusps)
                else:
                    placed, unresolved = multiwheel_layout.place_planet_glyphs(
                        lons, boxes, edges, asc, house_cusps=cusps)
                if unresolved or not multiwheel_layout.glyphs_have_clearance(
                        placed, minimum=max(2.0, size * .16)):
                    clear = False
                    break
            if clear:
                break

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

            direction = -1.0
        elif side == 'inner':
            base, far = inner + 1.0, inner + width

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
        return self.planet_label_edges(edges, side), base

    def draw_houses(self, core):
        """House numbers retain the inner Morinus chart's house-number ring."""
        if not self.options.houses:
            return
        cusps = [zodiac_lon(self.radix, self.radix.houses.cusps[i],
                            self.options) for i in range(1, 13)]
        font = self.font(max(8, core * .06))
        for index, mid in enumerate(multiwheel_layout.house_number_midpoints(cusps), 1):
            point = self.point(mid, core * .61)
            self.label(point, str(index), font, self.options.clrhousenumbers)
            self.planet_occupied.append(multiwheel_layout._rect(
                (point[0] - self.cx, point[1] - self.cy),
                self.measure(str(index), font), margin=1))
            self.drawn_house_numbers.append((0, index, mid))

    def draw_outer_house_numbers(self, chrt, index, inner, outer):
        """Print this ring's own house numbers, separate from radix houses."""
        if not self.options.houses:
            return
        cusps = [zodiac_lon(chrt, chrt.houses.cusps[i], self.options)
                 for i in range(1, 13)]
        radius = outer - min(10.5, (outer - inner) * .19)
        font = self.font(max(8, min(11, (outer - inner) * .16)))
        ink = (self.options.clrhousenumbers if self.bw else
               chartstyle.mix(tuple(self.options.clrhousenumbers),
                              self.ring_background_colour(index), .25))
        for house, midpoint in enumerate(
                multiwheel_layout.house_number_midpoints(cusps), 1):
            point = self.point(midpoint, radius)
            self.label(point, str(house), font, ink)
            self.planet_occupied.append(multiwheel_layout._rect(
                (point[0] - self.cx, point[1] - self.cy),
                self.measure(str(house), font), margin=1))
            self.drawn_house_numbers.append((index, house, midpoint))

    @staticmethod
    def position_label_parts(longitude, speed, mode):
        """Number and motion mark, using the same retro glyph as GraphChart.

        The retrograde marker is a Morinus *symbol-font* glyph ('T'), not
        a literal Latin R in the text font. A stationary S stays text.
        """
        degrees, minutes = wheel_primitives.position_text(longitude, '°')
        text = degrees + (minutes if mode == 2 else '')
        mark = (common.common.retr if speed < 0 else
                'S' if speed == 0 else '')
        return text, mark

    def position_label_size(self, text, marker, text_font, marker_font):
        """Combined ink rectangle for independently fonted number + marker."""
        tw, th = self.measure(text, text_font)
        if not marker:
            return (tw, th)
        mw, mh = self.measure(marker, marker_font)
        return (tw + max(2.0, self.planet_fonts['degree'] * .22) + mw,
                max(th, mh))

    def draw_position_label(self, xy, text, marker, text_font,
                            marker_font, colour):
        """Paint a centred annotation while keeping its motion glyph font."""
        if not marker:
            wheel_primitives.optical_text_center(
                self.draw, self.scaled(xy), text, text_font, colour)
            return
        tw, _ = self.measure(text, text_font)
        mw, _ = self.measure(marker, marker_font)
        gap = max(2.0, self.planet_fonts['degree'] * .22)
        total = tw + gap + mw
        left = xy[0] - total / 2.0
        wheel_primitives.optical_text_center(
            self.draw, self.scaled((left + tw / 2.0, xy[1])),
            text, text_font, colour)
        wheel_primitives.optical_text_center(
            self.draw, self.scaled((left + tw + gap + mw / 2.0, xy[1])),
            marker, marker_font, colour)

    def draw_planet_band(self, chrt, edges, role, dial_side, ring_index=0):
        """Treat each planet, its position and motion as one movable label.

        The degree dial and leaders always preserve the exact longitude.
        """
        (inner, outer), dial_anchor = self.draw_degree_dial(edges, dial_side)
        fonts = self.planet_fonts
        glyph_font = self.font(fonts['glyph'], symbol=True)
        degree_font = self.font(fonts['degree'])
        count = planets.Planets.BODIES_NUM
        lons = [self.longitude(chrt, i) for i in range(count)]
        glyph_boxes = [
            self.measure(common.common.planets[i], glyph_font)
            for i in range(count)]
        # A chart uses its *own* house system, not the radix house spokes
        # appearing beneath it. Sign membership is always tested as well.
        cusps = ([zodiac_lon(chrt, chrt.houses.cusps[j], self.options)
                  for j in range(1, houses.Houses.HOUSE_NUM + 1)]
                 if self.options.houses else None)
        asc = zodiac_lon(
            self.radix, self.radix.houses.ascmc[houses.Houses.ASC],
            self.options)
        # The retrograde character uses the original Morinus symbol font;
        # it is measured as part of the *same* box as the position number.
        label_mode = self.label_mode
        labels = []
        marks = []
        mark_fonts = []
        if label_mode:
            for i, lon in enumerate(lons):
                speed = chrt.planets.planets[i].data[planets.Planet.SPLON]
                text, marker = self.position_label_parts(
                    lon, speed, label_mode)
                labels.append(text)
                marks.append(marker)
                mark_fonts.append(self.font(
                    fonts['motion'], symbol=(speed < 0)))
            text_boxes = [
                self.position_label_size(text, mark, degree_font, mark_font)
                for text, mark, mark_font in
                zip(labels, marks, mark_fonts)
            ]
            direction = -1 if dial_side == 'outer' else 1
            placements, unresolved = multiwheel_layout.place_planet_label_groups(
                lons, glyph_boxes, text_boxes, (inner, outer), asc,
                direction, house_cusps=cusps,
                occupied_rects=self.planet_occupied)
        else:
            placements, unresolved = multiwheel_layout.place_planet_glyphs(
                lons, glyph_boxes, (inner, outer), asc, house_cusps=cusps)
        if unresolved:
            self.layout_issues.append((role, len(unresolved)))

        # Numbers are allowed to cover guide strokes and ring separators,
        # but never another number or a planetary glyph. Prepare their
        # placements now and paint them after the structural rings are done.
        visible_positions = set()
        reserved = list(self.planet_occupied)
        glyph_ink = [placement['rect'] for placement in placements]
        for i, placement in enumerate(placements):
            if not label_mode:
                break
            number = placement['rects'][1]
            obstacles = reserved + glyph_ink
            if any(multiwheel_layout._intersect_area(number, rect) > 0
                   for rect in obstacles):
                if i not in unresolved:
                    self.layout_issues.append((role, 1))
                continue
            visible_positions.add(i)
            reserved.append(number)
        self.planet_occupied.extend(glyph_ink)
        self.planet_occupied.extend(placements[i]['rects'][1]
                                    for i in sorted(visible_positions))

        for i, (exact, placement) in enumerate(zip(lons, placements)):
            gx, gy = placement['glyph']
            glyph_radius = math.hypot(gx, gy)
            theta = math.atan2(gy, gx)
            reach = wheel_primitives.radial_half_extent(
                glyph_boxes[i], theta)
            label_end = (glyph_radius - reach - 1.0
                         if dial_side == 'inner'
                         else glyph_radius + reach + 1.0)
            # A tangentially grouped glyph may not sit precisely on its
            # displayed radius. Aim the leader at the *actual glyph ink*,
            # from its immutable exact-longitude tick on the degree dial.
            glyph_edge = (self.cx + gx * label_end / glyph_radius,
                          self.cy + gy * label_end / glyph_radius)
            role_colours = self.highlight_role_colours(ring_index, i)
            glyph_colour = role_colours[0] if role_colours else self.planet_colour(i)
            self.stroke(self.point(exact, dial_anchor),
                        glyph_edge,
                        'pointer', glyph_colour)
            mark = 2.8 if dial_side == 'inner' else -2.8
            self.stroke(self.point(exact, dial_anchor),
                        self.point(exact, dial_anchor + mark),
                        'major', glyph_colour)
            glyph_xy = (self.cx + gx, self.cy + gy)
            if role_colours:
                # Tiny colored role dots preserve multiple activations without
                # enlarging glyph hitboxes or introducing concentric outlines.
                # Keep the glyph itself in the strongest available role color.
                left = glyph_xy[0] - glyph_boxes[i][0] * .5
                top = glyph_xy[1] - glyph_boxes[i][1] * .5
                for n, role_colour in enumerate(role_colours[:4]):
                    px = left + 2 + n * 4
                    py = top - 3
                    r = 1.6
                    self.draw.ellipse(
                        (self.scaled((px - r, py - r)),
                         self.scaled((px + r, py + r))),
                        fill=(55, 55, 55) if self.bw else role_colour)
            colour = self.colour(glyph_colour)
            wheel_primitives.optical_text_center(
                self.draw, self.scaled(glyph_xy),
                common.common.planets[i], glyph_font, colour)
            if label_mode and i in visible_positions:
                dx, dy = placement['position']
                label_xy = (self.cx + dx, self.cy + dy)
                self.pending_planet_positions.append(
                    (label_xy, labels[i], marks[i], degree_font,
                     mark_fonts[i], colour))
                self.drawn_degree_labels.append((role, i, labels[i]))
                if marks[i] == common.common.retr:
                    self.drawn_retrograde_glyphs.append(
                        (role, i, marks[i]))
            self.hits.append((glyph_xy, max(fonts['glyph'] * .75, 12),
                              chrt, i, exact, role))

    def draw_radix(self, core):
        self.draw_aspects(core)
        self.draw_houses(core)
        self.draw_zodiac_guides(self.radix, core * .67, core)
        self.draw_house_spokes(self.radix, core * .55, core)
        self.draw_angles(self.radix, core * .55, core)
        self.circle(core * .55)
        if self.options.houses:
            self.circle(core * .67, 'divider')
        self.circle(core)
        self.draw_planet_band(self.radix, (core * .67, core), i18n.tr('Inner chart'),
                              'outer')

    def traditional_font(self, edges):
        """Follow the small Morinus-planet glyph size used by GraphChart.

        GraphChart's small traditional ruler is 2/3 of the symbol size
        (typically about 1/18 of the chart radius). Limit it by this band's
        actual height for tri- and quad-wheels.
        """
        inner, outer = edges
        pixels = max(8, int(min((outer - inner) * .62,
                                 self.rmax / 24.0)))
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
                self.stroke_colour(self.options.clrsigns, 'divider'))

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
                self.stroke_colour(self.options.clrsigns, 'divider'))

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

    def highlight_role_colours(self, ring, planet):
        """One glyph can represent two active time-lord roles."""
        roles = self._highlight_lookup.get((ring, planet), ())
        return [multiwheel_highlight.ROLE_COLOURS[r] for r in roles]

    def fill_profection_sector(self, sign, inner, outer, colour):
        """Fill the whole 30-degree profected sign, respecting ring bounds."""
        if inner >= outer:
            return
        start = sign * 30.0
        lons = [start + i * 1.5 for i in range(21)]
        points = [self.scaled(self.point(lon, outer)) for lon in lons]
        points.extend(self.scaled(self.point(lon, inner))
                      for lon in reversed(lons))
        self.draw.polygon(points, fill=colour)

    def paint_highlight_fields(self, core, zodiac, rings):
        """Tint profected *signs*, never the houses occupied by rulers.

        In Whole Sign houses the 30-degree sector equals the entire house.
        Other house systems still follow the course's sign-based method;
        their house cusps remain visible without implying a false match.
        When annual and monthly signs coincide, split the band's radius
        into two broad colored halves rather than painting one over another.
        """
        if not self.show_highlights or not self.highlight_areas:
            return
        by_ring = {}
        for area in self.highlight_areas:
            by_ring.setdefault(area['ring'], {})[area['role']] = area['sign']
        for ring, areas in by_ring.items():
            if ring == 0:
                inner, outer = core * .55, core
            elif 1 <= ring <= len(rings):
                a, b = rings[ring - 1]
                inner = a + self.separator_width((a, b)) + .5
                outer = b
            else:
                continue
            annual, monthly = areas.get('annual'), areas.get('monthly')
            if annual is None:
                continue
            emerald = ((231, 231, 231) if self.bw else
                       multiwheel_highlight.SECTOR_COLOURS['annual'])
            amber = ((211, 211, 211) if self.bw else
                     multiwheel_highlight.SECTOR_COLOURS['monthly'])
            if monthly == annual:
                halfway = (inner + outer) / 2.0
                self.fill_profection_sector(annual, inner, halfway, amber)
                self.fill_profection_sector(annual, halfway, outer, emerald)
            else:
                self.fill_profection_sector(annual, inner, outer, emerald)
                if monthly is not None:
                    self.fill_profection_sector(monthly, inner, outer, amber)
        # The shared zodiac has one extra, unambiguous sign marker. It is
        # painted before sign glyphs and degree ticks (never over them).
        if zodiac:
            first = by_ring.get(0, {})
            annual = first.get('annual')
            month = next((roles['monthly'] for _, roles in sorted(
                by_ring.items()) if 'monthly' in roles), None)
            if annual is not None:
                if month == annual:
                    middle = sum(zodiac) / 2.0
                    self.fill_profection_sector(
                        annual, zodiac[0], middle,
                        (211, 211, 211) if self.bw else
                        multiwheel_highlight.SECTOR_COLOURS['monthly'])
                    self.fill_profection_sector(
                        annual, middle, zodiac[1],
                        (231, 231, 231) if self.bw else
                        multiwheel_highlight.SECTOR_COLOURS['annual'])
                else:
                    self.fill_profection_sector(
                        annual, *zodiac,
                        (231, 231, 231) if self.bw else
                        multiwheel_highlight.SECTOR_COLOURS['annual'])
                    if month is not None:
                        self.fill_profection_sector(
                            month, *zodiac,
                            (211, 211, 211) if self.bw else
                            multiwheel_highlight.SECTOR_COLOURS['monthly'])

    def paint_highlight_legend(self):
        """Compact four-role key outside wheel; inspector always has details."""
        if not self.show_highlights or not self.highlight_legend:
            return
        font_size = max(10, min(16, int(self.rmax * .023)))
        font = self.font(font_size)
        lines = [(item['role'], item['text'])
                 for item in self.highlight_legend]
        line_height = font_size * 1.6
        x, y = 14.0, 14.0
        width = max(self.measure(t, font)[0] for _, t in lines) + 33
        height = 13 + line_height * (len(lines) + 1)
        # Do not cover any portion of the zodiac or planets on a laptop.
        if math.hypot(self.cx - (x + width), self.cy - (y + height)) < self.rmax + 12:
            return
        background = (255, 255, 255) if self.bw else tuple(self.options.clrbackground)
        self.draw.rectangle((self.scaled((x, y)),
                             self.scaled((x + width, y + height))),
                            fill=background, outline=(190, 190, 190),
                            width=max(1, self.scale))
        self.label((x + width / 2, y + line_height * .65),
                   'Profections & Firdaria', self.font(font_size + 1),
                   (45, 45, 45))
        for i, (role, text) in enumerate(lines):
            yy = y + line_height * (i + 1.5)
            ink = ((70, 70, 70) if self.bw else
                   multiwheel_highlight.ROLE_COLOURS[role])
            self.draw.rectangle((self.scaled((x + 8, yy - 4)),
                                 self.scaled((x + 16, yy + 4))), fill=ink)
            self.label((x + 24 + self.measure(text, font)[0] / 2, yy),
                       text, font, (45, 45, 45))

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
        # Original: the reference bands separate radix from outer charts,
        # so erase through the zodiac's outer edge. Exterior: clearing to
        # the zodiac would also ERASE all the planetary rings. Only the
        # core must be restored in that layout.
        inner = self.core_radius if self.reference_outside else zodiac[1]
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
        """Label the selected inner chart in its otherwise empty centre."""
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
        front = self.font(max(10, min(13, (outer - inner) * .20)))
        secondary = self.font(max(9, min(11, (outer - inner) * .17)))
        max_width = min(self.rmax * .44, 180.0)
        while len(detail) > 8 and self.measure(detail, secondary)[0] > max_width:
            detail = detail[:-2] + '…'
        while len(kind) > 8 and self.measure(kind, front)[0] > max_width:
            kind = kind[:-2] + '…'
        w = max(self.measure(kind, front)[0],
                self.measure(detail, secondary)[0]) + 10
        h = 30.0
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
        # Faint zodiac boundaries provide sign context. House cusps are
        # stronger, and coincident divisions are rendered only once.
        self.draw_zodiac_guides(chrt, chart_start, outer, ring_index=index)
        self.draw_house_spokes(chrt, chart_start, outer, border)
        self.draw_angles(chrt, chart_start, outer, border, ring_index=index)
        self.draw_outer_house_numbers(chrt, index, chart_start, outer)
        self.draw_planet_band(chrt, (chart_start, outer),
                              i18n.tr('Ring %d') % index, 'inner', ring_index=index)

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
        # Rendering a chart reuses the same size, style and glyph fonts for
        # thousands of draw calls. Resolve native pens and font files once.
        self._ink_cache.clear()
        self._font_cache.clear()
        self.cx, self.cy = self.width / 2.0, self.height / 2.0
        self.rmax = min(self.width, self.height) * .465
        core, decans, terms, zodiac, rings = multiwheel_layout.allocate_traditional_rings(
            self.rmax, len(self.others), self.options.showterms,
            self.options.showdecans, reference_outside=self.reference_outside)
        self.core_radius = core
        self.prepare_planet_fonts(core, rings)
        self._highlight_lookup = {}
        if self.show_highlights:
            for entry in self.highlight_entries:
                self._highlight_lookup.setdefault(
                    (entry['ring'], entry['planet']), []).append(entry['role'])
        bg = (255, 255, 255) if self.bw else tuple(self.options.clrbackground)
        image = Image.new('RGB', i18n.tr((self.width * self.scale,
                                  self.height * self.scale)), i18n.tr(bg))
        self.draw = ImageDraw.Draw(image)
        self.adapt_planet_fonts(core, rings)
        self.hits = []
        self.layout_issues = []
        self.hidden_positions = []
        self.drawn_degree_labels = []
        self.drawn_retrograde_glyphs = []
        self.drawn_house_numbers = []
        self.pending_planet_positions = []
        self.planet_occupied = []
        self.draw_ring_backgrounds(zodiac, rings)
        self.paint_highlight_fields(core, zodiac, rings)
        self.draw_radix(core)
        if not self.reference_outside:
            self.draw_decans(decans)
            self.draw_terms(terms)
            self.draw_zodiac(zodiac)
        for index, (chrt, edges) in enumerate(zip(self.others, rings), 1):
            self.draw_outer_ring(chrt, index, edges)
        if self.reference_outside:
            # The outer reference bands are not another chart; they have
            # no house lines, angles, planet dials or chart identity.
            self.draw_decans(decans)
            self.draw_terms(terms)
            self.draw_zodiac(zodiac)
        self.draw_separator_gaps(rings)
        # Exterior mode ends with the shared zodiac; the original layout
        # ends at the last coloured planetary chart.
        if self.reference_outside:
            self.circle(zodiac[1] - .6, 'circle')
        else:
            self.circle(rings[-1][1] - .6, 'circle',
                        None if self.bw else RING_COLOURS[len(rings) - 1])
        # Labels are part of the chart image (and therefore its PNG), not
        # only the window's selectors. Add them after separators are clear.
        self.draw_centre_identity()
        for index, (chrt, edges) in enumerate(zip(self.others, rings), 1):
            self.draw_outer_identity(chrt, index, edges)
        # Render metadata above reference lines and separator masks. These
        # annotations are permitted to cross both without being erased.
        for args in self.pending_planet_positions:
            self.draw_position_label(*args)
        self.paint_highlight_legend()
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


class RingChartPicker(comparegrid.ChartPicker):
    """Select or create a chart in any ring, including the inner one."""

    def __init__(self, parent, mainfr, owner, on_change, prefer=0):
        self.owner = owner
        self.ring_index = prefer
        self._inner_override = None
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
        self.update_step_buttons()

    def update_step_buttons(self):
        if hasattr(self.owner, 'return_controls'):
            self.owner.update_return_controls()

    def changed(self, event):
        if self.ring_index == 0:
            index = self.choice.GetSelection()
            if 0 <= index < len(self.sources):
                source = self.sources[index][1]
                if isinstance(source, multiwheel_sources.RecentNatal):
                    loaded = self.mainfr.subLoad(
                        source.path, os.path.dirname(source.path), dontclose=True)
                    if loaded is None or loaded.htype != chart.Chart.RADIX:
                        self.choice.SetSelection(0)
                        return
                    self.owner.register_chart(loaded, i18n.tr('File'), self,
                                              file_path=source.path)
                    return
                if source is not self._inner_override:
                    if self._inner_override is not None:
                        self._inner_override = None
                        self.refresh()
        self.owner.manual_rings.add(self.ring_index)
        self.update_step_buttons()
        super().changed(event)

    def selected(self):
        """A recent path is only opened on explicit selection, not refresh."""
        selected = super().selected()
        if isinstance(selected, multiwheel_sources.RecentNatal):
            return self.mainfr.horoscope
        return selected

    def refresh(self, event=None):
        previous = self.selected()
        opened = []
        for wnd in wx.GetTopLevelWindows():
            if wnd.IsBeingDeleted() or not wnd.IsShown():
                continue
            # TransitFrame subclasses also represent elections, secondary
            # directions and profections. Other top-level chart windows may
            # have a horoscope but no .chart attribute.
            for attribute in ('chart', 'horoscope'):
                chrt = getattr(wnd, attribute, None)
                if isinstance(chrt, chart.Chart):
                    opened.append((i18n.tr('Open'), chrt))
            # Include charts opened in another comparison/multiwheel viewer.
            for picker in getattr(wnd, 'pickers', ()):
                if picker is self:
                    continue
                chrt = picker.selected()
                if isinstance(chrt, chart.Chart):
                    opened.append((i18n.tr('Open'), chrt))
                # Comparison pickers remember explicitly opened .hor files,
                # even when a different chart is currently selected.
                for _, loaded in getattr(picker, 'loaded', ()):
                    opened.append((i18n.tr('File'), loaded))
            for cell in getattr(wnd, 'cells', ()):
                chrt = cell.picker.selected()
                if isinstance(chrt, chart.Chart):
                    opened.append((i18n.tr('Open'), chrt))
                for _, loaded in getattr(cell.picker, 'loaded', ()):
                    opened.append((i18n.tr('File'), loaded))
            for label, chrt in getattr(wnd, 'registered_charts', ()):
                opened.append((label, chrt))
        if self.ring_index == 0:
            sources = multiwheel_sources.inner_chart_sources(
                self.mainfr.horoscope, opened, self.owner.registered_charts,
                chart.Chart.RADIX,
                manual_labels=(i18n.tr('File'), i18n.tr('New chart'),
                               i18n.tr('Here and now')))
            if (self._inner_override is not None and
                    all(chrt is not self._inner_override for _, chrt in sources)):
                sources.append((i18n.tr('Open'), self._inner_override))
            # A recent file is a lightweight selectable reference, not an
            # eagerly computed chart. Skip files already open in this window.
            history = getattr(self.mainfr, 'filehistory', None)
            if history is not None:
                known = set(self.owner.opened_paths)
                current_path = getattr(self.mainfr, 'fpath', '')
                if current_path:
                    known.add(os.path.abspath(current_path))
                for i in range(history.GetCount()):
                    path = history.GetHistoryFile(i)
                    if os.path.abspath(path) in known:
                        continue
                    recent = multiwheel_sources.recent_natal(
                        path, chart.Chart.RADIX)
                    if recent is not None:
                        sources.append((i18n.tr('Recent natal'), recent))
                        known.add(recent.path)
        else:
            sources = multiwheel_sources.merge_chart_sources(
                self.mainfr.horoscope, opened, self.owner.registered_charts)
        self.sources = [(self.chart_caption(label, chrt), chrt)
                        for label, chrt in sources]
        self.choice.Clear()
        for label, _ in self.sources:
            self.choice.Append(label)
        selected = next((i for i, (_, chrt) in enumerate(self.sources)
                         if chrt is previous), 0)
        self.choice.SetSelection(selected)
        self.update_step_buttons()
        if event is not None or self.selected() is not previous:
            self.on_change()

    @staticmethod
    def chart_caption(label, chrt):
        if isinstance(chrt, multiwheel_sources.RecentNatal):
            return label + ': ' + chrt.name + ' - ' + chrt.birth
        kind, _ = MultiWheel.chart_identity(chrt)
        if label in ('Active', i18n.tr('Open'), i18n.tr('File')):
            label = i18n.tr(label) + ' (' + kind.split(': ', 1)[0] + ')'
        return label + ': ' + comparegrid.caption(chrt)

    def select_chart(self, chrt):
        if self.ring_index == 0 and chrt is not self._inner_override:
            if any(source is chrt for _, source in self.sources):
                self._inner_override = None
            else:
                # A chart created expressly in the centre must remain
                # selectable even if its type is normally filtered out.
                self._inner_override = chrt
        self.refresh()
        for index, (_, source) in enumerate(self.sources):
            if source is chrt:
                self.choice.SetSelection(index)
                self.update_step_buttons()
                self.on_change()
                return

    def open_file(self, event):
        dlg = wx.FileDialog(self, i18n.tr('Open chart'),
                            self.mainfr.fpathhors, '',
                            'Morinus charts (*.hor)|*.hor',
                            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        try:
            if dlg.ShowModal() != wx.ID_OK:
                return
            path = dlg.GetPath()
        finally:
            dlg.Destroy()
        chrt = self.mainfr.subLoad(path, os.path.dirname(path), dontclose=True)
        if chrt is not None:
            self.owner.register_chart(chrt, i18n.tr('File'), self,
                                      file_path=path)

    def show_create_menu(self, event):
        menu = wx.Menu()
        for group, actions in multiwheel_sources.CREATE_GROUPS:
            submenu = wx.Menu()
            for label, action in actions:
                item = submenu.Append(wx.ID_ANY, i18n.tr(label))
                menu.Bind(wx.EVT_MENU,
                          lambda e, requested=action: self.create_chart(requested),
                          id=item.GetId())
            menu.AppendSubMenu(submenu, i18n.tr(group))
        try:
            self.PopupMenu(menu)
        finally:
            menu.Destroy()

    def create_new_chart(self):
        import datadlg
        dlg = datadlg.DataDlg(self.owner, self.mainfr.options.langid,
                              self.mainfr.options.netbook)
        try:
            dlg.CenterOnParent()
            dlg.initialize()
            if dlg.ShowModal() != wx.ID_OK:
                return None
            return self.mainfr.chartFromDataDialog(dlg)
        finally:
            dlg.Destroy()

    def create_chart(self, action):
        """Use existing Morinus chart dialogs, then select only this ring.

        A cancelled dialog must leave both its chart and selection untouched.
        New natal and horary charts are constructed independently: they do
        not replace the main horoscope or close any existing windows.
        """
        radix = None
        if action == 'new':
            chrt = self.create_new_chart()
        elif action == 'here_now':
            chrt = self.mainfr.makeHereAndNowChart()
        else:
            before = {id(w) for w in wx.GetTopLevelWindows()}
            returns = {
                'saturn': 0, 'jupiter': 1, 'mars': 2, 'solar': 3,
                'venus': 4, 'mercury': 5, 'lunar': 6}
            if action in returns:
                self.mainfr.onRevolutions(None, planet=returns[action])
            else:
                methods = {
                    'transits': 'onTransits',
                    'sun_transits': 'onSunTransits',
                    'secondary': 'onSecondaryDirs',
                    'profections': 'onProfectionsChart',
                    'elections': 'onElections',
                    'syzygy': 'onSyzygyChart',
                    'syzygy_other': 'onSyzygyChart2',
                    'synastry': 'onSynastry',
                }
                getattr(self.mainfr, methods[action])(None)
            created = [w for w in wx.GetTopLevelWindows()
                       if id(w) not in before and not w.IsBeingDeleted()
                       and isinstance(getattr(w, 'chart', None), chart.Chart)]
            chrt = created[-1].chart if created else None
            radix = getattr(created[-1], 'radix', None) if created else None
        if chrt is not None:
            labels = {
                'new': 'New chart', 'here_now': 'Here and now',
                'synastry': 'Synastry', 'solar': 'Solar return',
                'lunar': 'Lunar return', 'saturn': 'Saturn return',
                'jupiter': 'Jupiter return', 'mars': 'Mars return',
                'venus': 'Venus return', 'mercury': 'Mercury return',
                'transits': 'Transits', 'sun_transits': 'Sun transits',
                'secondary': 'Secondary directions',
                'profections': 'Profections', 'elections': 'Elections',
                'syzygy': 'Prenatal syzygy',
                'syzygy_other': 'Other prenatal syzygy',
            }
            self.owner.register_chart(chrt, i18n.tr(labels[action]), self,
                                      radix=radix)


class MultiWheelFrame(wx.Frame):
    """Independent chart selection for every field of a multi-wheel."""

    def __init__(self, mainfr):
        wx.Frame.__init__(self, mainfr, title=i18n.tr('Multi-wheel'), size=(1250, 900))
        self.mainfr = mainfr
        self.options = mainfr.options
        self.buffer = None
        self.renderer = None
        self.pending = None
        self._alive = True
        self.zoom_factor = None  # None = fit window; 1.0 = natural chart size
        self.sidebar_visible = True
        self.saved_sidebar_width = 350
        self.manual_rings = set()
        self.auto_transit_radix = {}
        self.moving_transits = set()
        self._auto_filling = False
        self.registered_charts = []
        self.opened_paths = set()
        self.return_origins = {}
        self.return_years = {}
        self.lunar_years = {}
        self.return_cache = OrderedDict()
        self._updating_returns = False
        self.bitmap_origin = (0, 0)
        self._last_hover = ''
        self.current_highlights = []
        self.current_profection_areas = []
        self._highlight_span_cache = OrderedDict()
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)
        self.SetMinSize((1060, 600))
        outer = wx.BoxSizer(wx.VERTICAL)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(wx.StaticText(self, label=i18n.tr('Outer rings:')), 0,
                wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.count_choice = wx.Choice(
            self, choices=i18n.tr(['1 (bi-wheel)', '2 (tri-wheel)', '3 (quad-wheel)']))
        self.count_choice.SetSelection(0)
        row.Add(self.count_choice, 0, wx.RIGHT, 15)
        row.Add(wx.StaticText(self, label=i18n.tr('Aspects between:')), 0,
                wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.aspect_choice = wx.Choice(
            self, choices=i18n.tr(['None', 'Inner chart only', 'Inner and ring 1']))
        self.aspect_choice.SetSelection(0)
        row.Add(self.aspect_choice, 0, wx.RIGHT, 15)
        row.Add(wx.StaticText(self, label=i18n.tr('Reference bands:')),
                0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 6)
        self.reference_choice = wx.Choice(
            self, choices=i18n.tr(['Inside (classic)', 'Outside (experimental)']))
        self.reference_choice.SetSelection(1)
        row.Add(self.reference_choice, 0, wx.RIGHT, 8)
        outer.Add(row, 0, wx.LEFT | wx.RIGHT | wx.TOP, 7)
        viewrow = wx.BoxSizer(wx.HORIZONTAL)
        self.fit_button = wx.Button(self, label=i18n.tr('Fit'))
        self.actual_button = wx.Button(self, label='100%')
        self.out_button = wx.Button(self, label='-')
        self.in_button = wx.Button(self, label='+')
        for control in (self.fit_button, self.actual_button,
                        self.out_button, self.in_button):
            viewrow.Add(control, 0, wx.RIGHT, 4)
        self.side_button = wx.Button(self, label=i18n.tr('Hide charts'))
        viewrow.Add(self.side_button, 0, wx.RIGHT, 8)
        self.savebutton = wx.Button(self, label=i18n.tr('Save image (PNG)...'))
        viewrow.Add(self.savebutton, 0, wx.RIGHT, 10)
        viewrow.Add(wx.StaticText(self, label=i18n.tr('Planet labels:')),
                    0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.labels_choice = wx.Choice(
            self, choices=i18n.tr(['Glyphs only', 'Glyphs + degrees',
                                   'Full positions']))
        self.labels_choice.SetSelection(1)
        viewrow.Add(self.labels_choice, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        self.highlight_choice = wx.CheckBox(self, label=i18n.tr('Highlight rulers'))
        self.highlight_choice.SetValue(True)
        viewrow.Add(self.highlight_choice, 0, wx.ALIGN_CENTER_VERTICAL)
        outer.Add(viewrow, 0, wx.ALL, 7)

        # Splitter lets the user give more room to long chart captions and
        # the return lists. Unlike a fixed-width sizer, the sash stays
        # adjustable and retains its width on ordinary window resizing.
        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.splitter.SetMinimumPaneSize(220)
        self.splitter.SetSashGravity(0.0)
        self.sidebar = wx.ScrolledWindow(self.splitter, style=wx.VSCROLL)
        self.sidebar.SetMinSize((230, 250))
        self.sidebar.SetScrollRate(0, 15)
        controls = wx.BoxSizer(wx.VERTICAL)
        self.pickers = []
        self.picker_rows = []
        for i in range(4):
            strip = wx.Panel(self.sidebar)
            line = wx.BoxSizer(wx.VERTICAL)
            tag = wx.StaticText(
                strip, label=(i18n.tr('Inner chart') if i == 0
                              else i18n.tr('Ring %d') % i) + ':')
            if i and not self.options.bw:
                tag.SetForegroundColour(wx.Colour(*RING_COLOURS[i - 1]))
            line.Add(tag, 0, wx.BOTTOM, 4)
            picker = RingChartPicker(strip, mainfr, self,
                                     lambda index=i: self.on_picker_change(index), i)
            line.Add(picker, 0, wx.EXPAND)
            strip.SetSizer(line)
            self.pickers.append(picker)
            self.picker_rows.append(strip)
            controls.Add(strip, 0, wx.EXPAND | wx.BOTTOM, 14)
            if i > 1:
                strip.Hide()
        self.return_panel = wx.Panel(self.sidebar)
        return_controls = wx.BoxSizer(wx.VERTICAL)
        return_controls.Add(wx.StaticText(self.return_panel,
                           label=i18n.tr('Return navigation')), 0, wx.BOTTOM, 8)
        return_controls.Add(wx.StaticText(self.return_panel,
                           label=i18n.tr('Solar ring')), 0, wx.BOTTOM, 3)
        self.solar_ring_choice = wx.Choice(self.return_panel)
        return_controls.Add(self.solar_ring_choice, 0, wx.EXPAND | wx.BOTTOM, 6)
        return_controls.Add(wx.StaticText(self.return_panel,
                           label=i18n.tr('Solar years')), 0, wx.BOTTOM, 3)
        self.solar_year_list = wx.ListBox(self.return_panel, size=(-1, 108))
        return_controls.Add(self.solar_year_list, 0, wx.EXPAND | wx.BOTTOM, 9)
        return_controls.Add(wx.StaticText(self.return_panel,
                           label=i18n.tr('Lunar ring')), 0, wx.BOTTOM, 3)
        self.lunar_ring_choice = wx.Choice(self.return_panel)
        return_controls.Add(self.lunar_ring_choice, 0, wx.EXPAND | wx.BOTTOM, 6)
        return_controls.Add(wx.StaticText(self.return_panel,
                           label=i18n.tr('Lunar returns')), 0, wx.BOTTOM, 3)
        self.lunar_list = wx.ListBox(self.return_panel, size=(-1, 180))
        return_controls.Add(self.lunar_list, 0, wx.EXPAND)
        self.return_panel.SetSizer(return_controls)
        controls.Add(self.return_panel, 0, wx.EXPAND | wx.BOTTOM, 12)
        self._nav_solar_ring = None
        self._nav_lunar_ring = None
        self._nav_solar_slots = []
        self._nav_lunar_slots = []
        self._nav_years = []
        self._nav_lunar_rows = []
        self.selection_note = wx.StaticText(self.sidebar, label='')
        self.selection_note.Wrap(290)
        controls.Add(self.selection_note, 0, wx.EXPAND | wx.BOTTOM, 8)
        self.sidebar.SetSizer(controls)

        # White chart canvas with an OS-themed, independently resizable rail.
        self.view_surface = wx.Panel(self.splitter)
        self.view_surface.SetBackgroundColour(wx.WHITE)
        workspace = wx.BoxSizer(wx.HORIZONTAL)
        self.view_splitter = wx.SplitterWindow(
            self.view_surface, style=wx.SP_LIVE_UPDATE)
        self.view_splitter.SetMinimumPaneSize(220)
        self.view_splitter.SetSashGravity(1.0)
        self.canvas = wx.ScrolledWindow(
            self.view_splitter, style=wx.HSCROLL | wx.VSCROLL)
        self.canvas.SetBackgroundColour(wx.WHITE)
        self.canvas.SetMinSize((380, 390))
        self.canvas.SetScrollRate(20, 20)
        self.canvas.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        # Keep chart identity separate from the time/navigation workspace.
        # Both pages scroll independently on small laptop screens.
        rail_bg = self.sidebar.GetBackgroundColour()
        rail_fg = self.selection_note.GetForegroundColour()
        self.inspector = wx.Notebook(self.view_splitter)
        self.inspector.SetBackgroundColour(rail_bg)
        self.inspector.SetForegroundColour(rail_fg)
        self.inspector.SetMinSize((270, 260))
        self.info_page = wx.ScrolledWindow(self.inspector, style=wx.VSCROLL)
        self.controls_page = wx.ScrolledWindow(self.inspector, style=wx.VSCROLL)
        for page in (self.info_page, self.controls_page):
            page.SetBackgroundColour(rail_bg)
            page.SetForegroundColour(rail_fg)
            page.SetScrollRate(0, 14)
        self.inspector.AddPage(self.info_page, i18n.tr('Charts'))
        self.inspector.AddPage(self.controls_page, i18n.tr('Returns + transits'))

        info_rail = wx.BoxSizer(wx.VERTICAL)
        self.add_rail_heading(info_rail, 'Profections & Firdaria', self.info_page)
        # Each technique can be toggled independently; no extra chart
        # calculations are needed when a highlight is hidden.
        self.highlight_role_choices = {}
        toggle_grid = wx.GridSizer(rows=2, cols=2, vgap=4, hgap=7)
        for role, title in (('annual', 'Annual'),
                            ('monthly', 'Monthly'),
                            ('major', 'Firdaria major'),
                            ('sub', 'Firdaria minor')):
            cb = wx.CheckBox(self.info_page, label=i18n.tr(title))
            cb.SetValue(True)
            self.highlight_role_choices[role] = cb
            toggle_grid.Add(cb, 0, wx.EXPAND)
            cb.Bind(wx.EVT_CHECKBOX, self.queue_draw)
        info_rail.Add(toggle_grid, 0, wx.EXPAND | wx.BOTTOM, 11)
        self.legend_asof = wx.StaticText(self.info_page, label='')
        self.legend_asof.SetForegroundColour(rail_fg)
        info_rail.Add(self.legend_asof, 0, wx.EXPAND | wx.BOTTOM, 5)
        self.legend_labels = []
        for _ in range(5):
            label = wx.StaticText(self.info_page, label='')
            label.SetForegroundColour(rail_fg)
            self.legend_labels.append(label)
            info_rail.Add(label, 0, wx.EXPAND | wx.BOTTOM, 5)
        info_rail.Add(wx.StaticLine(self.info_page), 0,
                      wx.EXPAND | wx.TOP | wx.BOTTOM, 11)
        self.add_rail_heading(info_rail, 'Chart details', self.info_page)
        self.chart_details = []
        for i in range(4):
            label = wx.StaticText(self.info_page, label='')
            label.SetForegroundColour(rail_fg)
            self.chart_details.append(label)
            info_rail.Add(label, 0, wx.EXPAND | wx.BOTTOM, 11)
        self.info_page.SetSizer(info_rail)

        controls_rail = wx.BoxSizer(wx.VERTICAL)
        self.return_section = wx.Panel(self.controls_page)
        self.return_section.SetBackgroundColour(rail_bg)
        self.return_section.SetForegroundColour(rail_fg)
        return_rail = wx.BoxSizer(wx.VERTICAL)
        self.add_rail_heading(return_rail, 'Return controls', self.return_section)
        self.return_controls = []
        for i in range(4):
            line = wx.Panel(self.return_section)
            line.SetBackgroundColour(rail_bg)
            row_controls = wx.BoxSizer(wx.HORIZONTAL)
            caption = wx.StaticText(line, label='')
            caption.SetForegroundColour(rail_fg)
            previous = wx.Button(line, label='◀', size=(33, -1))
            following = wx.Button(line, label='▶', size=(33, -1))
            previous.SetToolTip(i18n.tr('Previous return'))
            following.SetToolTip(i18n.tr('Next return'))
            row_controls.Add(caption, 1, wx.ALIGN_CENTER_VERTICAL)
            row_controls.Add(previous, 0, wx.LEFT, 3)
            row_controls.Add(following, 0, wx.LEFT, 3)
            line.SetSizer(row_controls)
            return_rail.Add(line, 0, wx.EXPAND | wx.BOTTOM, 5)
            self.return_controls.append((line, previous, following, caption))
            previous.Bind(wx.EVT_BUTTON,
                          lambda e, index=i: self.step_return_ring(index, False))
            following.Bind(wx.EVT_BUTTON,
                           lambda e, index=i: self.step_return_ring(index, True))
        self.return_section.SetSizer(return_rail)
        controls_rail.Add(self.return_section, 0, wx.EXPAND | wx.BOTTOM, 12)

        self.transit_section = wx.Panel(self.controls_page)
        self.transit_section.SetBackgroundColour(rail_bg)
        self.transit_section.SetForegroundColour(rail_fg)
        transit_rail = wx.BoxSizer(wx.VERTICAL)
        self.add_rail_heading(transit_rail, 'Transit controller', self.transit_section)
        self.transit_ring_choice = wx.Choice(self.transit_section)
        transit_rail.Add(self.transit_ring_choice, 0, wx.EXPAND | wx.BOTTOM, 6)
        self.transit_slots = []
        self.active_transit_ring = None
        self.transit_buttons = []
        self.transit_inputs = {}
        self._transit_fields_chart = None
        self._transit_fields_ring = None
        for unit in multiwheel_time.UNITS:
            row_controls = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(self.transit_section, label=i18n.tr(unit))
            label.SetForegroundColour(rail_fg)
            plus = wx.Button(self.transit_section, label='++', size=(34, -1))
            minus = wx.Button(self.transit_section, label='--', size=(34, -1))
            row_controls.Add(label, 1, wx.ALIGN_CENTER_VERTICAL)
            if unit != 'Sec':
                entry = wx.TextCtrl(self.transit_section, size=(64, -1),
                                    style=wx.TE_PROCESS_ENTER)
                entry.SetToolTip(i18n.tr('Enter a value, then apply the date and time'))
                entry.Bind(wx.EVT_TEXT_ENTER, self.apply_transit_time)
                row_controls.Add(entry, 0, wx.LEFT, 3)
                self.transit_inputs[unit] = entry
            row_controls.Add(plus, 0, wx.LEFT, 3)
            row_controls.Add(minus, 0, wx.LEFT, 3)
            transit_rail.Add(row_controls, 0, wx.EXPAND | wx.BOTTOM, 4)
            plus.Bind(wx.EVT_BUTTON,
                      lambda e, part=unit: self.step_transit(part, True))
            minus.Bind(wx.EVT_BUTTON,
                       lambda e, part=unit: self.step_transit(part, False))
            self.transit_buttons.extend((plus, minus))
        self.transit_apply = wx.Button(self.transit_section, label=i18n.tr('Apply date/time'))
        transit_rail.Add(self.transit_apply, 0, wx.EXPAND | wx.TOP, 6)
        self.transit_apply.Bind(wx.EVT_BUTTON, self.apply_transit_time)
        self.transit_now = wx.Button(self.transit_section, label=i18n.tr('Now (UTC)'))
        transit_rail.Add(self.transit_now, 0, wx.EXPAND | wx.TOP, 7)
        self.transit_now.Bind(wx.EVT_BUTTON, self.transit_to_now)
        self.transit_section.SetSizer(transit_rail)
        controls_rail.Add(self.transit_section, 0, wx.EXPAND)
        self.controls_page.SetSizer(controls_rail)
        self.view_splitter.SplitVertically(self.canvas, self.inspector, -285)
        workspace.Add(self.view_splitter, 1, wx.EXPAND)
        self.view_surface.SetSizer(workspace)
        self.splitter.SplitVertically(self.sidebar, self.view_surface,
                                      self.saved_sidebar_width)
        outer.Add(self.splitter, 1, wx.EXPAND | wx.ALL, 7)
        self.SetSizer(outer)
        self.CreateStatusBar()
        self.Bind(wx.EVT_CHOICE, self.change_count, self.count_choice)
        self.Bind(wx.EVT_CHOICE, self.queue_draw, self.aspect_choice)
        self.Bind(wx.EVT_CHOICE, self.queue_draw, self.labels_choice)
        self.Bind(wx.EVT_CHOICE, self.queue_draw, self.reference_choice)
        self.Bind(wx.EVT_CHECKBOX, self.queue_draw, self.highlight_choice)
        self.Bind(wx.EVT_BUTTON, self.onSaveAsBitmap, self.savebutton)
        self.Bind(wx.EVT_BUTTON, self.zoom_fit, self.fit_button)
        self.Bind(wx.EVT_BUTTON, self.zoom_actual, self.actual_button)
        self.Bind(wx.EVT_BUTTON, self.zoom_in, self.in_button)
        self.Bind(wx.EVT_BUTTON, self.zoom_out, self.out_button)
        self.Bind(wx.EVT_BUTTON, self.toggle_sidebar, self.side_button)
        self.solar_ring_choice.Bind(wx.EVT_CHOICE, self.on_solar_ring_choice)
        self.lunar_ring_choice.Bind(wx.EVT_CHOICE, self.on_lunar_ring_choice)
        self.solar_year_list.Bind(wx.EVT_LISTBOX, self.on_solar_year_choice)
        self.lunar_list.Bind(wx.EVT_LISTBOX, self.on_lunar_choice)
        self.transit_ring_choice.Bind(wx.EVT_CHOICE, self.on_transit_ring_choice)
        self.splitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED,
                           self.on_sidebar_resized)
        self.view_splitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED,
                                self.on_inspector_resized)
        self.canvas.Bind(wx.EVT_PAINT, self.paint)
        self.canvas.Bind(wx.EVT_SIZE, self.resize)
        self.canvas.Bind(wx.EVT_LEFT_UP, self.on_click)
        self.canvas.Bind(wx.EVT_MOTION, self.on_motion)
        self.canvas.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_ACTIVATE, lambda e: (comparegrid.refresh_pickers(self.pickers) if e.GetActive() else None, e.Skip()))
        self.CentreOnParent()
        # Track actual chart identity, not its name or selected menu index.
        # A file-loaded natal must trigger the same dependent-ring update as
        # choosing an already-open natal from the dropdown.
        self._last_inner_chart = self.pickers[0].selected()
        self.refresh_return_navigation()
        wx.CallAfter(self.queue_draw)

    def add_rail_heading(self, rail, label, parent):
        heading = wx.StaticText(parent, label=i18n.tr(label))
        font = heading.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        heading.SetFont(font)
        heading.SetForegroundColour(parent.GetForegroundColour())
        rail.Add(heading, 0, wx.EXPAND | wx.BOTTOM, 7)
        return heading

    @staticmethod
    def utc_datetime(chrt):
        """UTC-only return/transit timestamps, matching their chart.jd."""
        t = chrt.time
        if t.bc:
            return None
        try:
            return datetime(t.origyear, t.origmonth, t.origday,
                            t.hour, t.minute, t.second, tzinfo=timezone.utc)
        except ValueError:
            return None

    def highlight_reference_time(self, charts):
        """Prefer a selected LR in the solar year, not an unrelated 'now'.

        Lunar return selection is our monthly-navigation controller.
        If no LR exists, prefer a selected transit, then the SR epoch.
        """
        for kind in (chart.Chart.LUNAR, chart.Chart.TRANSIT,
                     chart.Chart.SOLAR):
            for chrt in charts:
                if chrt.htype == kind:
                    instant = self.utc_datetime(chrt)
                    if instant is not None:
                        return instant
        return datetime.now(timezone.utc)

    def time_lord_entries(self, inner, charts):
        """Derive course-defined signs/rulers from the selected SR year.

        Cache the *next* solar-return boundary: redraws and zooms should
        never repeatedly recalculate a year's ephemeris.
        """
        solar = next((chrt for chrt in charts
                      if chrt.htype == chart.Chart.SOLAR and
                      self.return_origin(chrt) is inner), None)
        if solar is None:
            # A separately opened SR may lack provenance; only use it if
            # its name and natal year clearly match the active radix.
            solar = next((chrt for chrt in charts
                          if chrt.htype == chart.Chart.SOLAR and
                          chrt.name == inner.name), None)
        year = self.solar_year(solar) if solar is not None else None
        start_jd, end_jd = None, None
        if solar is not None and 1 <= year <= 9997:
            start_jd = solar.time.jd
            key = (inner, year)
            if key in self._highlight_span_cache:
                end_jd = self._highlight_span_cache[key]
            else:
                following = returnslist.solar_return(inner, year + 1)
                if following is not None:
                    end_jd = returnslist.gmt_time(following, inner).jd
                    self._highlight_span_cache[key] = end_jd
                    if len(self._highlight_span_cache) > 8:
                        self._highlight_span_cache.popitem(last=False)
        when = self.highlight_reference_time(charts)
        reference_jd = None
        if start_jd is not None and end_jd is not None:
            # LR determines the month even when current transits are
            # several years away from the chosen Solar Return.
            lr = next((chrt for chrt in charts
                       if chrt.htype == chart.Chart.LUNAR and
                       self.return_origin(chrt) is inner), None)
            if lr is not None:
                reference_jd = lr.time.jd
                if reference_jd < start_jd:
                    # The LR already in force at the SR belongs to
                    # month one (the course notes this boundary case).
                    reference_jd = start_jd
                elif reference_jd >= end_jd:
                    reference_jd = end_jd - 0.000001
                when = self.utc_datetime(lr) or when
                if lr.time.jd < start_jd:
                    when = self.utc_datetime(solar) or when
            else:
                transit = next((chrt for chrt in charts
                                if chrt.htype == chart.Chart.TRANSIT and
                                start_jd <= chrt.time.jd < end_jd), None)
                reference_jd = transit.time.jd if transit else start_jd
                when = (self.utc_datetime(transit) if transit else
                        self.utc_datetime(solar)) or when

        data = multiwheel_highlight.entries_for(
            inner, charts, when, bool(self.options.ayanamsha),
            solar_year=year, solar_start_jd=start_jd,
            next_solar_jd=end_jd, monthly_date_jd=reference_jd)
        permitted = {role for role, ctrl in self.highlight_role_choices.items()
                     if ctrl.GetValue()}
        for field in ('marks', 'areas', 'legend'):
            data[field] = [entry for entry in data[field]
                           if entry['role'] in permitted]
        return data, when

    def update_highlight_legend(self, summary, instant):
        if not self.highlight_choice.GetValue():
            self.legend_asof.SetLabel(i18n.tr('Highlighting off'))
            for label in self.legend_labels:
                label.Hide()
            self.refresh_inspector()
            return
        self.legend_asof.SetLabel(
            '%s %s UTC' % (i18n.tr('As of'), instant.strftime('%Y-%m-%d')))
        if not summary:
            self.legend_labels[0].SetLabel(i18n.tr('No active profection available'))
            self.legend_labels[0].SetForegroundColour(
                self.info_page.GetForegroundColour())
            self.legend_labels[0].Show()
        for i, label in enumerate(self.legend_labels):
            if i >= len(summary):
                label.Hide()
                continue
            role, label_text = summary[i]['role'], summary[i]['text']
            label.SetLabel(label_text)
            label.SetForegroundColour(
                wx.Colour(*(multiwheel_highlight.ROLE_COLOURS[role]
                            if not self.options.bw else (65, 65, 65))))
            label.Show()
        self.refresh_inspector()

    def refresh_inspector(self):
        for page in (self.info_page, self.controls_page):
            page.Layout()
            page.FitInside()
        self.inspector.Layout()

    def on_sidebar_resized(self, event):
        if self.splitter.IsSplit():
            self.saved_sidebar_width = max(230, self.splitter.GetSashPosition())
        self.queue_draw()
        event.Skip()

    def on_inspector_resized(self, event):
        self.refresh_inspector()
        self.queue_draw()
        event.Skip()

    def update_return_controls(self):
        """Return arrows live on the white workspace, not in the sidebar."""
        if not hasattr(self, 'return_controls'):
            return
        count = self.count_choice.GetSelection() + 1
        has_returns = False
        for i, (line, previous, following, caption) in enumerate(self.return_controls):
            selected = self.pickers[i].selected()
            is_return = (i <= count and
                         selected.htype in (chart.Chart.SOLAR, chart.Chart.LUNAR)
                         and self.return_origin(selected) is not None)
            if is_return:
                kind = ('SR' if selected.htype == chart.Chart.SOLAR else 'LR')
                caption.SetLabel('%s  %s' % (self.ring_label(i), kind))
                has_returns = True
            line.Show(is_return)
            previous.Enable(is_return)
            following.Enable(is_return)
        self.return_section.Show(has_returns)
        self.refresh_inspector()

    def refresh_transit_controls(self):
        """Choose which of the visible transit rings the stepper will move."""
        count = self.count_choice.GetSelection() + 1
        slots = [i for i in range(count + 1)
                 if self.pickers[i].selected().htype == chart.Chart.TRANSIT]
        if self.active_transit_ring not in slots:
            self.active_transit_ring = slots[-1] if slots else None
        self.transit_slots = slots
        self.transit_ring_choice.Clear()
        for i in slots:
            self.transit_ring_choice.Append(self.ring_label(i))
        if self.active_transit_ring is not None:
            self.transit_ring_choice.SetSelection(
                slots.index(self.active_transit_ring))
        self.transit_ring_choice.Enable(bool(slots))
        for button in self.transit_buttons:
            button.Enable(bool(slots))
        self.transit_now.Enable(bool(slots))
        self.transit_apply.Enable(bool(slots))
        selected = (self.pickers[self.active_transit_ring].selected()
                    if self.active_transit_ring is not None else None)
        if (selected is not self._transit_fields_chart or
                self.active_transit_ring != self._transit_fields_ring):
            t = selected.time if selected is not None else None
            values = ((t.origyear, t.origmonth, t.origday, t.hour, t.minute)
                      if t is not None else ('',) * 5)
            for unit, value in zip(multiwheel_time.UNITS, values):
                self.transit_inputs[unit].ChangeValue(str(value))
            self._transit_fields_chart = selected
            self._transit_fields_ring = self.active_transit_ring
        for entry in self.transit_inputs.values():
            entry.Enable(bool(slots))
        self.transit_section.Show(bool(slots))
        self.refresh_inspector()

    def on_transit_ring_choice(self, event):
        index = self.transit_ring_choice.GetSelection()
        if 0 <= index < len(self.transit_slots):
            self.active_transit_ring = self.transit_slots[index]
            self.refresh_transit_controls()

    def create_current_transit(self, radix):
        """An independent transit chart for the present UTC instant."""
        now = datetime.now(timezone.utc)
        location = radix.place
        instant = chart.Time(now.year, now.month, now.day,
                             now.hour, now.minute, now.second, False,
                             chart.Time.GREGORIAN, chart.Time.GREENWICH,
                             True, 0, 0, False, location)
        return chart.Chart(radix.name, radix.male, instant, location,
                           chart.Chart.TRANSIT, '', self.options, False)

    def step_transit(self, unit, forward):
        """Move one transit ring using the same six increments as Elections."""
        index = self.active_transit_ring
        if index is None:
            return
        previous = self.pickers[index].selected()
        if previous.htype != chart.Chart.TRANSIT:
            return
        t = previous.time
        current = (t.origyear, t.origmonth, t.origday,
                   t.hour, t.minute, t.second)
        changed = multiwheel_time.shift(current, unit, forward)
        if changed is None:
            self.SetStatusText(i18n.tr('The requested date is out of range.'))
            return
        self.set_transit_time(index, changed)

    def apply_transit_time(self, event=None):
        """Apply all five entered values at once; preserve transit seconds."""
        index = self.active_transit_ring
        if index is None:
            return
        selected = self.pickers[index].selected()
        if selected.htype != chart.Chart.TRANSIT:
            return
        try:
            fields = [int(self.transit_inputs[unit].GetValue().strip())
                      for unit in multiwheel_time.UNITS[:5]]
            parts = tuple(fields + [selected.time.second])
            multiwheel_time.validate(
                parts, julian=selected.time.cal == chart.Time.JULIAN)
        except (TypeError, ValueError):
            self.SetStatusText(i18n.tr('Please enter a valid date and time.'))
            return
        self.set_transit_time(index, parts)

    def set_transit_time(self, index, changed):
        """Build an independent transit chart at the requested civil time."""
        previous = self.pickers[index].selected()
        if previous.htype != chart.Chart.TRANSIT:
            return
        t = previous.time
        try:
            instant = chart.Time(*changed, t.bc, t.cal, t.zt, t.plus,
                                 t.zh, t.zm, t.daylightsaving, previous.place)
            moving = chart.Chart(previous.name, previous.male, instant,
                                 previous.place, chart.Chart.TRANSIT, '',
                                 self.options, False)
        except (ValueError, OverflowError) as exc:
            self.SetStatusText(str(exc))
            return
        self.replace_moving_transit(index, moving)

    def transit_to_now(self, event=None):
        index = self.active_transit_ring
        if index is None:
            return
        previous = self.pickers[index].selected()
        if previous.htype != chart.Chart.TRANSIT:
            return
        self.replace_moving_transit(index, self.create_current_transit(previous))

    def replace_moving_transit(self, index, new_chart):
        """Keep only the latest remote-controlled transit in the menu.

        An earlier transit remains available if another ring still uses it.
        Manually created or loaded transit charts are never pruned.
        """
        previous = self.pickers[index].selected()
        self.register_chart(new_chart, i18n.tr('Transits'), self.pickers[index])
        self.moving_transits.add(new_chart)
        if (previous in self.moving_transits and
                not any(picker.selected() is previous for picker in self.pickers)):
            self.registered_charts = [item for item in self.registered_charts
                                      if item[1] is not previous]
            self.moving_transits.discard(previous)
            for picker in self.pickers:
                picker.refresh()

    @staticmethod
    def angle_label(longitude):
        lon = longitude % 360
        degrees = int(lon % 30)
        minutes = int((lon % 1) * 60)
        return '%02d°%02d′ %s' % (degrees, minutes,
                                  i18n.tr(SIGNS[int(lon // 30)]))

    def update_chart_details(self):
        """Provide chart identity, place, exact time and both main angles."""
        count = self.count_choice.GetSelection() + 1
        for i, label in enumerate(self.chart_details):
            if i > count:
                label.Hide()
                continue
            chrt = self.pickers[i].selected()
            kind, date = MultiWheel.chart_identity(chrt)
            time_suffix = (' UTC' if chrt.time.zt == chart.Time.GREENWICH
                           else '')
            place = getattr(chrt.place, 'placename', '') or i18n.tr('Unknown place')
            asc = self.angle_label(chrt.houses.ascmc[houses.Houses.ASC])
            mc = self.angle_label(chrt.houses.ascmc[houses.Houses.MC])
            contents = ('%s · %s\n%s%s\n%s\nASC %s\nMC  %s' %
                        (self.ring_label(i), kind, date, time_suffix,
                         place, asc, mc))
            label.SetLabel(contents)
            label.Wrap(238)
            label.Show()
        self.refresh_inspector()

    def maybe_autofill_rings(self):
        """Natal -> SR implies in-force LR and, on a quad-wheel, transits.

        Automatically fill only untouched rings. A manually chosen chart in
        any ring always wins. Linking requires the *same* natal object.
        """
        if self._auto_filling or self._updating_returns:
            return
        count = self.count_choice.GetSelection() + 1
        if count < 2:
            return
        radix = self.pickers[0].selected()
        solar = self.pickers[1].selected()
        if (radix.htype != chart.Chart.RADIX or
                solar.htype != chart.Chart.SOLAR or
                self.return_origin(solar) is not radix):
            return
        self._auto_filling = True
        previous = self._updating_returns
        self._updating_returns = True
        try:
            if 2 not in self.manual_rings:
                year = self.solar_year(solar)
                rows = self.return_rows(radix, year)
                if len(rows) >= 2:
                    current = self.pickers[2].selected()
                    expected = returnslist.gmt_time(rows[1].t, radix).jd
                    if not (current.htype == chart.Chart.LUNAR and
                            self.return_origin(current) is radix and
                            abs(current.time.jd - expected) < .02):
                        lunar = returnslist.return_chart(
                            rows[1].t, radix, chart.Chart.LUNAR, radix.place)
                        self.register_chart(lunar, i18n.tr('Lunar return'),
                                            self.pickers[2], radix=radix)
            if (count >= 3 and 3 not in self.manual_rings
                    and self.auto_transit_radix.get(3) is not radix):
                transit = self.create_current_transit(radix)
                self.register_chart(transit, i18n.tr('Transits'),
                                    self.pickers[3])
                self.auto_transit_radix[3] = radix
                self.moving_transits.add(transit)
        finally:
            self._updating_returns = previous
            self._auto_filling = False
        if not previous:
            self.refresh_return_navigation()
            self.queue_draw()

    def change_count(self, event=None):
        count = self.count_choice.GetSelection() + 1
        for i, strip in enumerate(self.picker_rows):
            strip.Show(i <= count)
        prior = self.aspect_choice.GetSelection()
        self.aspect_choice.Clear()
        self.aspect_choice.Append(i18n.tr('None'))
        self.aspect_choice.Append(i18n.tr('Inner chart only'))
        for i in range(count):
            self.aspect_choice.Append(i18n.tr('Inner and ring %d') % (i + 1))
        self.aspect_choice.SetSelection(min(max(prior, 0), count + 1))
        self.sidebar.Layout()
        self.sidebar.FitInside()
        self.Layout()
        self.maybe_autofill_rings()
        self.refresh_return_navigation()
        self.queue_draw()

    def register_chart(self, chrt, label, picker, radix=None, solar_year=None,
                       file_path=None):
        """Retain a newly created/loaded chart for all ring dropdowns.

        Only the ring whose button was used changes its selection.
        """
        if not self._auto_filling and not self._updating_returns:
            self.manual_rings.add(picker.ring_index)
        if (chrt.htype in (chart.Chart.SOLAR, chart.Chart.LUNAR)
                and isinstance(radix, chart.Chart)
                and radix.htype == chart.Chart.RADIX):
            self.return_origins[chrt] = radix
        if solar_year is not None:
            self.return_years[chrt] = solar_year
        if file_path is not None:
            self.opened_paths.add(os.path.abspath(file_path))
        if not any(source is chrt for _, source in self.registered_charts):
            self.registered_charts.append((label, chrt))
        previous = self._updating_returns
        self._updating_returns = True
        try:
            for item in self.pickers:
                item.refresh()
            picker.select_chart(chrt)
        finally:
            self._updating_returns = previous
        if not previous:
            if picker.ring_index == 0:
                # register_chart deliberately suppresses picker callbacks
                # during refresh; explicitly handle a newly loaded radix now.
                self.on_picker_change(0)
            elif picker.ring_index == 1:
                self.maybe_autofill_rings()
            self.refresh_return_navigation()
            self.queue_draw()

    def return_origin(self, chrt):
        """Only documented natal provenance can link two returns.

        In particular, identical names, birth dates or calculated planets
        are not sufficient to infer that two open charts have one radix.
        """
        if chrt.htype not in (chart.Chart.SOLAR, chart.Chart.LUNAR):
            return None
        radix = self.return_origins.get(chrt)
        if radix is not None:
            return radix
        for wnd in wx.GetTopLevelWindows():
            if wnd.IsBeingDeleted():
                continue
            if getattr(wnd, 'chart', None) is chrt:
                candidate = getattr(wnd, 'radix', None)
                if (isinstance(candidate, chart.Chart)
                        and candidate.htype == chart.Chart.RADIX):
                    self.return_origins[chrt] = candidate
                    return candidate
            others = getattr(wnd, 'return_origins', None)
            if others is not None and chrt in others:
                self.return_origins[chrt] = others[chrt]
                return others[chrt]
        return None

    def sync_radix_dependents(self, previous_radix, radix):
        """Rebase visible/hidden SR, LR and transit rings on a new natal.

        This is an explicit change of the *inner* chart, not the ordinary
        SR/LR stepper. Recompute all currently selected derived ring types,
        even if they were selected manually. Unrelated chart types are left
        untouched. Preserve each SR year and each transit's civil timestamp.
        Do not rename or mutate charts in independently opened windows.
        """
        if (radix is previous_radix or radix.htype != chart.Chart.RADIX or
                self._updating_returns or self._auto_filling):
            return False
        dependents = [(i, picker.selected())
                      for i, picker in enumerate(self.pickers[1:], 1)
                      if picker.selected().htype in (
                          chart.Chart.SOLAR, chart.Chart.LUNAR,
                          chart.Chart.TRANSIT)]
        if not dependents:
            return False

        assignments = self.ring_assignments()
        solar_years = {i: self.solar_year(old)
                       for i, old in dependents
                       if old.htype == chart.Chart.SOLAR}
        lunar_years = {}
        for i, old in dependents:
            if old.htype != chart.Chart.LUNAR:
                continue
            linked = self.selected_solar_for_lunar(i, assignments)
            lunar_years[i] = (solar_years[linked]
                              if linked in solar_years
                              else self.lunar_years.get(old, old.time.year))

        # Calculate all replacement charts before touching any selection.
        # If a return cannot be calculated, retain the old selection and
        # display a clear error instead of partially relabelling the wheel.
        rows_by_year = {}
        replacements = []
        try:
            for year in set(lunar_years.values()):
                rows = self.return_rows(radix, year)
                if len(rows) < 2:
                    raise ValueError('Cannot calculate lunar returns for %s' % year)
                rows_by_year[year] = rows
            for i, old in dependents:
                if old.htype == chart.Chart.SOLAR:
                    year = solar_years[i]
                    t = (rows_by_year[year][0].t if year in rows_by_year
                         else returnslist.solar_return(radix, year))
                    if t is None:
                        raise ValueError('Cannot calculate solar return for %s' % year)
                    new = returnslist.return_chart(
                        t, radix, chart.Chart.SOLAR, radix.place)
                    replacements.append((i, old, new, i18n.tr('Solar return'), year))
                elif old.htype == chart.Chart.LUNAR:
                    year = lunar_years[i]
                    new = returnslist.return_chart(
                        rows_by_year[year][1].t, radix, chart.Chart.LUNAR,
                        radix.place)
                    replacements.append((i, old, new, i18n.tr('Lunar return'), None))
                else:
                    t = old.time
                    instant = chart.Time(
                        t.origyear, t.origmonth, t.origday,
                        t.hour, t.minute, t.second, t.bc, t.cal, t.zt,
                        t.plus, t.zh, t.zm, t.daylightsaving, radix.place)
                    new = chart.Chart(
                        radix.name, radix.male, instant, radix.place,
                        chart.Chart.TRANSIT, '', self.options, False)
                    replacements.append((i, old, new, i18n.tr('Transits'), None))
        except (ValueError, OverflowError, RuntimeError) as exc:
            self.SetStatusText(i18n.tr('Could not update dependent rings: ') +
                               str(exc))
            return False

        # A single batch prevents stale picker selections from triggering
        # another autofill halfway through the rebase.
        self._updating_returns = True
        self._auto_filling = True
        try:
            for i, old, new, label, year in replacements:
                self.register_chart(
                    new, label, self.pickers[i],
                    radix=radix if new.htype in (
                        chart.Chart.SOLAR, chart.Chart.LUNAR) else None,
                    solar_year=year)
                if new.htype == chart.Chart.TRANSIT:
                    self.auto_transit_radix[i] = radix
                    self.moving_transits.add(new)
            # Remove obsolete generated entries from our dropdown menus,
            # but do not erase a separately opened/file-loaded chart.
            replaced = {old for _, old, _, _, _ in replacements}
            selected = {picker.selected() for picker in self.pickers}
            keep_labels = {i18n.tr('File'), i18n.tr('New chart'),
                           i18n.tr('Here and now')}
            self.registered_charts = [
                entry for entry in self.registered_charts
                if entry[1] not in replaced or entry[1] in selected or
                entry[0] in keep_labels]
            for old in replaced - selected:
                self.moving_transits.discard(old)
            for picker in self.pickers:
                picker.refresh()
        finally:
            self._auto_filling = False
            self._updating_returns = False
        self.refresh_return_navigation()
        self.queue_draw()
        return True

    def on_picker_change(self, index):
        self.queue_draw()
        if (index == 0 and not self._updating_returns and
                hasattr(self, '_last_inner_chart')):
            current = self.pickers[0].selected()
            if current is not self._last_inner_chart:
                previous = self._last_inner_chart
                self._last_inner_chart = current
                if self.sync_radix_dependents(previous, current):
                    return
        if not self._updating_returns and hasattr(self, 'solar_ring_choice'):
            if index <= 1:
                self.maybe_autofill_rings()
            self.refresh_return_navigation()

    def ring_assignments(self):
        count = self.count_choice.GetSelection() + 2  # centre + outer fields
        out = []
        for picker in self.pickers[:count]:
            selected = picker.selected()
            kind = ('solar' if selected.htype == chart.Chart.SOLAR else
                    'lunar' if selected.htype == chart.Chart.LUNAR else None)
            out.append((kind, self.return_origin(selected) if kind else None))
        return out

    def return_rows(self, radix, year):
        if radix is None or not 1 <= year <= 9998:
            return []
        key = (radix, year)
        if key in self.return_cache:
            self.return_cache.move_to_end(key)
            return self.return_cache[key]
        try:
            rows = returnslist.compute(radix, year)
        except (ValueError, OverflowError, RuntimeError) as exc:
            self.SetStatusText(str(exc))
            return []
        self.return_cache[key] = rows
        if len(self.return_cache) > 6:
            self.return_cache.popitem(last=False)
        return rows

    def solar_year(self, chrt):
        known = self.return_years.get(chrt)
        if known is not None:
            return known
        # A solar return at the edge of December/January may take place
        # in a different UTC calendar year from the requested return year.
        radix = self.return_origin(chrt)
        if radix is not None:
            for candidate in (chrt.time.year, chrt.time.year - 1,
                              chrt.time.year + 1):
                if not 1 <= candidate <= 9998:
                    continue
                t = returnslist.solar_return(radix, candidate)
                if (t is not None and abs(returnslist.gmt_time(t, radix).jd
                                          - chrt.time.jd) < .03):
                    self.return_years[chrt] = candidate
                    return candidate
        return chrt.time.year

    def lunar_solar_year(self, lunar, radix):
        """Which solar year contains a standalone lunar return?"""
        if lunar in self.lunar_years:
            return self.lunar_years[lunar]
        # A solar return for a named year can occur in the previous
        # December or the next January. Compare Julian-day boundaries,
        # not calendar years, to handle birthdays near New Year's Day.
        calendar_year = lunar.time.year
        for year in range(calendar_year - 1, calendar_year + 2):
            if not 1 <= year <= 9997:
                continue
            start = returnslist.solar_return(radix, year)
            end = returnslist.solar_return(radix, year + 1)
            if (start and end and
                    returnslist.gmt_time(start, radix).jd <= lunar.time.jd
                    < returnslist.gmt_time(end, radix).jd):
                self.lunar_years[lunar] = year
                return year
        return None

    def selected_solar_for_lunar(self, lunar_index, assignments=None):
        assignments = assignments or self.ring_assignments()
        return multiwheel_returnnav.nearest_inner_solar(lunar_index, assignments)

    def select_solar_year(self, ring_index, year, lunar_overrides=None):
        """Step a solar ring and reset matching outer lunar rings to in-force.

        The sole exception is the lunar ring that initiated a chronological
        cross-year step: it displays the actual next/previous lunar event.
        """
        solar = self.pickers[ring_index].selected()
        radix = self.return_origin(solar)
        if solar.htype != chart.Chart.SOLAR or radix is None:
            return False
        assignments = self.ring_assignments()
        linked = multiwheel_returnnav.linked_lunar_indices(ring_index, assignments)
        # Do not calculate a whole year of lunar returns when only the
        # solar chart is present. That is noticeably slower than one SR.
        rows = self.return_rows(radix, year) if linked else []
        solar_t = rows[0].t if rows else returnslist.solar_return(radix, year)
        if solar_t is None or (linked and len(rows) < 2):
            return False
        overrides = lunar_overrides or {}
        prior = self._updating_returns
        self._updating_returns = True
        try:
            new_solar = returnslist.return_chart(
                solar_t, radix, chart.Chart.SOLAR, solar.place)
            self.register_chart(new_solar, i18n.tr('Solar return'),
                                self.pickers[ring_index], radix=radix,
                                solar_year=year)
            for index in linked:
                old_lunar = self.pickers[index].selected()
                row = overrides.get(index, rows[1])
                new_lunar = returnslist.return_chart(
                    row.t, radix, chart.Chart.LUNAR, old_lunar.place)
                self.register_chart(new_lunar, i18n.tr('Lunar return'),
                                    self.pickers[index], radix=radix)
        finally:
            self._updating_returns = prior
        if not prior:
            self.refresh_return_navigation()
            self.queue_draw()
        return True

    def select_lunar_row(self, ring_index, row, radix):
        old = self.pickers[ring_index].selected()
        if old.htype != chart.Chart.LUNAR or self.return_origin(old) is not radix:
            return False
        new_lunar = returnslist.return_chart(
            row.t, radix, chart.Chart.LUNAR, old.place)
        self.register_chart(new_lunar, i18n.tr('Lunar return'),
                            self.pickers[ring_index], radix=radix)
        return True

    def step_return_ring(self, ring_index, forward):
        selected = self.pickers[ring_index].selected()
        radix = self.return_origin(selected)
        if radix is None:
            return
        delta = 1 if forward else -1
        if selected.htype == chart.Chart.SOLAR:
            if not self.select_solar_year(ring_index,
                                          self.solar_year(selected) + delta):
                self.SetStatusText(i18n.tr('The next return could not be computed.'))
            return
        if selected.htype != chart.Chart.LUNAR:
            return
        assignments = self.ring_assignments()
        solar_index = self.selected_solar_for_lunar(ring_index, assignments)
        if solar_index is None:
            # For an unrelated or standalone lunar ring, no other chart is
            # changed. Morinus's ordinary return stepper already handles it.
            new_lunar = returnslist.step_return(radix, selected, forward)
            if new_lunar is not None:
                self.register_chart(new_lunar, i18n.tr('Lunar return'),
                                    self.pickers[ring_index], radix=radix)
            else:
                self.SetStatusText(i18n.tr('The next return could not be computed.'))
            return
        year = self.solar_year(self.pickers[solar_index].selected())
        rows = self.return_rows(radix, year)
        hits = rows[1:]
        target_index = multiwheel_returnnav.next_return_index(
            hits, selected.time.jd, forward)
        if target_index is not None:
            self.select_lunar_row(ring_index, hits[target_index], radix)
            return
        # The same in-force LR can occur at both sides of the year
        # boundary. Choose a strictly different event on the new year's
        # list and move the associated inner SR at the same time.
        next_year = year + delta
        hits = self.return_rows(radix, next_year)[1:]
        target_index = multiwheel_returnnav.next_return_index(
            hits, selected.time.jd, forward)
        if (target_index is None or not self.select_solar_year(
                solar_index, next_year,
                lunar_overrides={ring_index: hits[target_index]})):
            self.SetStatusText(i18n.tr('The next return could not be computed.'))

    def refresh_return_navigation(self):
        """Show just the returns of the active year, without changing rings."""
        if self._updating_returns:
            return
        assignments = self.ring_assignments()
        solar_slots = [i for i, (kind, radix) in enumerate(assignments)
                       if kind == 'solar' and radix is not None]
        lunar_slots = [i for i, (kind, radix) in enumerate(assignments)
                       if kind == 'lunar' and radix is not None]
        self.return_panel.Show(bool(solar_slots or lunar_slots))
        self._nav_solar_slots = solar_slots
        self._nav_lunar_slots = lunar_slots
        if self._nav_solar_ring not in solar_slots:
            self._nav_solar_ring = solar_slots[0] if solar_slots else None
        if self._nav_lunar_ring not in lunar_slots:
            # Prefer a lunar ring that really follows the chosen SR.
            matching = [i for i in lunar_slots if
                        self.selected_solar_for_lunar(i, assignments)
                        == self._nav_solar_ring]
            self._nav_lunar_ring = (matching[0] if matching else
                                    lunar_slots[0] if lunar_slots else None)
        self.solar_ring_choice.Clear()
        for i in solar_slots:
            self.solar_ring_choice.Append(self.ring_label(i))
        if self._nav_solar_ring is not None:
            self.solar_ring_choice.SetSelection(
                solar_slots.index(self._nav_solar_ring))
        self.solar_ring_choice.Enable(bool(solar_slots))
        self.lunar_ring_choice.Clear()
        for i in lunar_slots:
            self.lunar_ring_choice.Append(self.ring_label(i))
        if self._nav_lunar_ring is not None:
            self.lunar_ring_choice.SetSelection(
                lunar_slots.index(self._nav_lunar_ring))
        self.lunar_ring_choice.Enable(bool(lunar_slots))

        self._nav_years = []
        self.solar_year_list.Clear()
        if self._nav_solar_ring is not None:
            year = self.solar_year(self.pickers[self._nav_solar_ring].selected())
            self._nav_years = list(multiwheel_returnnav.solar_year_window(year))
            for choice in self._nav_years:
                self.solar_year_list.Append(str(choice))
            if year in self._nav_years:
                self.solar_year_list.SetSelection(self._nav_years.index(year))
        self.solar_year_list.Enable(bool(self._nav_years))

        self._nav_lunar_rows = []
        self.lunar_list.Clear()
        if self._nav_lunar_ring is not None:
            index = self._nav_lunar_ring
            lunar = self.pickers[index].selected()
            radix = self.return_origin(lunar)
            linked_solar = self.selected_solar_for_lunar(index, assignments)
            if linked_solar is not None:
                year = self.solar_year(self.pickers[linked_solar].selected())
            else:
                year = self.lunar_solar_year(lunar, radix)
            if year is not None:
                self._nav_lunar_rows = self.return_rows(radix, year)[1:]
            for n, row in enumerate(self._nav_lunar_rows, 1):
                date = '%04d-%02d-%02d %02d:%02d UTC' % row.t[:5]
                note = (' (' + i18n.tr('in force') + ')' if
                        row.note == returnslist.IN_FORCE else '')
                self.lunar_list.Append('%02d  %s%s' % (n, date, note))
            hit = multiwheel_returnnav.match_return_index(
                self._nav_lunar_rows, lunar.time.jd)
            if hit is not None:
                self.lunar_list.SetSelection(hit)
        self.lunar_list.Enable(bool(self._nav_lunar_rows))
        self.sidebar.Layout()
        self.sidebar.FitInside()
        self.update_return_controls()
        self.refresh_transit_controls()
        self.update_chart_details()

    @staticmethod
    def ring_label(index):
        return i18n.tr('Inner chart') if index == 0 else i18n.tr('Ring %d') % index

    def on_solar_ring_choice(self, event):
        choice = self.solar_ring_choice.GetSelection()
        if 0 <= choice < len(self._nav_solar_slots):
            self._nav_solar_ring = self._nav_solar_slots[choice]
            matching = [i for i in self._nav_lunar_slots if
                        self.selected_solar_for_lunar(i)
                        == self._nav_solar_ring]
            if matching:
                self._nav_lunar_ring = matching[0]
            self.refresh_return_navigation()

    def on_lunar_ring_choice(self, event):
        choice = self.lunar_ring_choice.GetSelection()
        if 0 <= choice < len(self._nav_lunar_slots):
            self._nav_lunar_ring = self._nav_lunar_slots[choice]
            self.refresh_return_navigation()

    def on_solar_year_choice(self, event):
        choice = self.solar_year_list.GetSelection()
        if (self._nav_solar_ring is not None
                and 0 <= choice < len(self._nav_years)):
            self.select_solar_year(self._nav_solar_ring, self._nav_years[choice])

    def on_lunar_choice(self, event):
        choice = self.lunar_list.GetSelection()
        if (self._nav_lunar_ring is not None
                and 0 <= choice < len(self._nav_lunar_rows)):
            selected = self.pickers[self._nav_lunar_ring].selected()
            self.select_lunar_row(self._nav_lunar_ring,
                                  self._nav_lunar_rows[choice],
                                  self.return_origin(selected))

    def toggle_sidebar(self, event=None):
        self.sidebar_visible = not self.sidebar_visible
        if self.sidebar_visible:
            self.splitter.SplitVertically(self.sidebar, self.view_surface,
                                          self.saved_sidebar_width)
        else:
            self.saved_sidebar_width = max(230, self.splitter.GetSashPosition())
            self.splitter.Unsplit(self.sidebar)
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
        inner = self.pickers[0].selected()
        charts = [picker.selected() for picker in self.pickers[1:count + 1]]
        repeated = []
        seen = {id(inner): i18n.tr('Inner chart')}
        for i, selected in enumerate(charts, 1):
            if id(selected) in seen:
                repeated.append(i18n.tr('Ring %d') % i + ' = ' + seen[id(selected)])
            else:
                seen[id(selected)] = i18n.tr('Ring %d') % i
        self.renderer = MultiWheel(inner, charts,
                                   (w, h), self.options, self.options.bw)
        self.renderer.aspect_ring = aspect_ring_from_choice(
            self.aspect_choice.GetSelection())
        self.renderer.label_mode = self.labels_choice.GetSelection()
        self.renderer.reference_outside = bool(self.reference_choice.GetSelection())
        self.renderer.show_highlights = self.highlight_choice.GetValue()
        data, instant = self.time_lord_entries(inner, charts)
        self.current_highlights = data['marks']
        self.current_profection_areas = data['areas']
        self.renderer.highlight_entries = data['marks']
        self.renderer.highlight_areas = data['areas']
        self.renderer.highlight_legend = data['legend']
        self.buffer = self.renderer.drawChart()
        self.update_highlight_legend(data['legend'], instant)
        notes = []
        if repeated:
            notes.append(i18n.tr('Repeated charts') + ': ' + ', '.join(repeated))
        if self.renderer.layout_issues:
            notes.append(i18n.tr('Crowded planet labels: zoom in for clarity'))
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

    def position_details(self, point):
        if self.renderer is None:
            return ''
        x, y = self.canvas.CalcUnscrolledPosition(point)
        return self.renderer.onClick(
            (x - self.bitmap_origin[0], y - self.bitmap_origin[1]))

    def on_click(self, event):
        self.SetStatusText(self.position_details(event.GetPosition()))

    def on_motion(self, event):
        # Give the complete degree, minute, motion and sign on hover,
        # including for planets whose small visible label could not fit.
        details = self.position_details(event.GetPosition())
        if details != self._last_hover:
            self._last_hover = details
            self.canvas.SetToolTip(details)
        event.Skip()

    def on_leave(self, event):
        self._last_hover = ''
        self.canvas.SetToolTip('')
        event.Skip()

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
            inner = self.pickers[0].selected()
            charts = [p.selected() for p in self.pickers[1:count + 1]]
            exporter = MultiWheel(inner, charts,
                                  (diameter, diameter),
                                  self.options, self.options.bw)
            exporter.aspect_ring = aspect_ring_from_choice(
                self.aspect_choice.GetSelection())
            exporter.label_mode = self.labels_choice.GetSelection()
            exporter.reference_outside = bool(self.reference_choice.GetSelection())
            exporter.show_highlights = self.highlight_choice.GetValue()
            data, _ = self.time_lord_entries(inner, charts)
            exporter.highlight_entries = data['marks']
            exporter.highlight_areas = data['areas']
            exporter.highlight_legend = data['legend']
            bitmap = exporter.drawChart()
            if bitmap.SaveFile(path, wx.BITMAP_TYPE_PNG):
                self.mainfr.fpathimgs = os.path.dirname(path)
        finally:
            dlg.Destroy()


def show(mainfr):
    frame = MultiWheelFrame(mainfr)
    frame.Show(True)
    return frame
