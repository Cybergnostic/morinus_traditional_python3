"""Time-lord highlighting for the multi-wheel (no wx or drawing dependencies).

The Firdaria sequence is Morinus's existing Firdaria object, including its
diurnal/nocturnal selection and Bonatti/Al-Biruni option. The Solar Return
Ascendant uses the seven traditional domicile rulers, not an invented annual
lord calculation.
"""
from datetime import datetime, timedelta
import firdaria


# Planet indices are Morinus's traditional Chaldean order.
NAMES = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus',
         'Mercury', 'Moon', 'North Node', 'South Node')
DOMICILE = (2, 4, 5, 6, 3, 5, 4, 2, 1, 0, 0, 1)

# Different from Morinus's individual ring tint colours.
ROLE_COLOURS = {
    'major': (48, 105, 165),      # Firdaria major: blue
    'sub': (168, 92, 28),         # Firdaria subperiod: amber
    'solar_asc': (126, 74, 145), # SR Ascendant ruler: violet
}
ROLE_LABELS = {
    'major': 'Firdaria major',
    'sub': 'Firdaria sub',
    'solar_asc': 'SR Asc ruler',
}


def at_firdaria(radix, when):
    """Return the Morinus major/sub rulers at a UTC datetime, or None.

    Reuse an already computed natal Firdaria if present. Never recalculate
    chart/planet positions; just inspect the existing period sequence.
    The same seven equal subperiods and nextIndex() rule as firdariawnd
    apply. Node periods have no subperiod ruler in Morinus.
    """
    if getattr(radix.time, 'bc', False):
        return None
    try:
        fird = getattr(radix, 'firdaria', None)
        if fird is None:
            t = radix.time
            fird = firdaria.Firdaria(
                t.origyear, t.origmonth, t.origday, radix.options,
                radix.abovehorizonwithorb)
        current = when.replace(tzinfo=None)
        if current < fird.startdate:
            return None
        periods = (fird.dailyplanetaryyears if fird.isdaily
                   else fird.nightlyplanetaryyearsbonatti
                   if fird.options.isfirbonatti
                   else fird.nightlyplanetaryyearsalbiruni)
        start = fird.startdate
        for period in range(256):
            index = period % len(periods)
            ruler, years = periods[index]
            end = firdaria.addyears(start, years)
            if start <= current < end:
                if fird.isNode(index):
                    return ruler, None
                sub_index = index
                step = (end - start) / 7
                for sub in range(7):
                    next_start = start + step * (sub + 1)
                    if current < next_start or sub == 6:
                        return ruler, periods[sub_index][0]
                    sub_index = fird.nextIndex(sub_index)
            start = end
    except (ValueError, OverflowError, AttributeError):
        pass
    return None


def solar_asc_ruler(solar, sidereal=False):
    """Traditional domicile lord of the displayed SR Ascendant sign."""
    asc = solar.houses.ascmc[0]
    if sidereal:
        asc -= solar.ayanamsha
    return DOMICILE[int((asc % 360) // 30)]


def chart_house(chrt, index, sidereal=False):
    """House containing the selected planet in this chart's cusp system."""
    from multiwheel_layout import house_sector
    longitude = chrt.planets.planets[index].data[0]
    cusps = [chrt.houses.cusps[i] for i in range(1, 13)]
    if sidereal:
        longitude -= chrt.ayanamsha
        cusps = [c - chrt.ayanamsha for c in cusps]
    return house_sector(longitude % 360,
                        [c % 360 for c in cusps]) + 1


def entries_for(radix, others, when, sidereal=False):
    """A list of independent overlay marks, never modifying chart state.

    Each entry has ring (0 for radix), planet index, role, house and a short
    legend line. Solar marks belong to their actual SR ring only.
    """
    marks = []
    rulers = at_firdaria(radix, when) if getattr(radix, 'htype', None) == 0 else None
    if rulers:
        major, sub = rulers
        for role, ruler in (('major', major), ('sub', sub)):
            if ruler is not None:
                marks.append({
                    'ring': 0, 'planet': ruler, 'role': role,
                    'house': chart_house(radix, ruler, sidereal),
                    'text': '%s: %s (H%d)' % (
                        ROLE_LABELS[role], NAMES[ruler],
                        chart_house(radix, ruler, sidereal)),
                })
    for number, solar in enumerate(others, 1):
        # chart.Chart.SOLAR == 1 in Morinus; avoid importing chart and wx.
        if getattr(solar, 'htype', None) != 1:
            continue
        ruler = solar_asc_ruler(solar, sidereal)
        house = chart_house(solar, ruler, sidereal)
        marks.append({
            'ring': number, 'planet': ruler, 'role': 'solar_asc',
            'house': house, 'text': 'SR%d Asc: %s (H%d)' % (
                number, NAMES[ruler], house),
        })
    return marks
