"""Course-based annual and monthly profection highlighting for multiwheel.

No wxPython dependency. Annual whole-sign profections are anchored to the
natal Ascendant; monthly profections take twelve *equal time divisions*
between exact successive Solar Returns. This deliberately does not implement
the optional thirteen-period method.

Doctrine: Natalna 25, 26, 27 + original lecture transcripts, cw_api/astrology.
Firdaria follows Morinus's existing day/night and Bonatti/Biruni settings.
"""
from datetime import datetime

import firdaria

NAMES = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus',
         'Mercury', 'Moon', 'North Node', 'South Node')
SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
# Morinus's Chaldean planet indices; never use modern co-rulers.
DOMICILE = (2, 4, 5, 6, 3, 5, 4, 2, 1, 0, 0, 1)
ROLE_COLOURS = {
    'annual': (22, 135, 107),  # strong emerald: annual lord
    'monthly': (181, 121, 9),  # strong amber: monthly lord
    'major': (119, 64, 163),   # strong violet: major Firdaria lord
    'sub': (183, 55, 102),     # strong rose: minor Firdaria lord
}
# Areas intentionally much paler and brighter than lord glyphs.
SECTOR_COLOURS = {
    'annual': (220, 246, 235),
    'monthly': (255, 241, 205),
}
ROLE_LABELS = {
    'annual': 'Annual profection',
    'monthly': 'Monthly profection',
    'major': 'Firdaria major',
    'sub': 'Firdaria minor',
}


def at_firdaria(radix, when):
    """Morinus's existing day/night period sequence and seven subperiods."""
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
                    if current < start + step * (sub + 1) or sub == 6:
                        return ruler, periods[sub_index][0]
                    sub_index = fird.nextIndex(sub_index)
            start = end
    except (ValueError, OverflowError, AttributeError):
        return None
    return None


def asc_sign(radix, sidereal=False):
    longitude = radix.houses.ascmc[0]
    if sidereal:
        longitude -= radix.ayanamsha
    return int(longitude % 360 // 30)


def annual_profection(radix, solar_year, sidereal=False):
    """Return (activated sign, domicile ruler, annual house, attained age)."""
    if solar_year is None or getattr(radix.time, 'bc', False):
        return None
    age = int(solar_year) - int(radix.time.origyear)
    if age < 0:
        return None
    sign = (asc_sign(radix, sidereal) + age) % 12
    return sign, DOMICILE[sign], age % 12 + 1, age


def monthly_index(start_jd, end_jd, reference_jd):
    """0..11, twelve equal intervals of an actual solar-return year.

    Month zero begins *exactly* at the SR instant, not the civil month
    anniversary. An in-force LR preceding that instant is clamped to
    month zero. A reference after the year is clamped to month eleven.
    """
    if end_jd is None or start_jd is None or end_jd <= start_jd:
        return None
    fraction = (reference_jd - start_jd) / (end_jd - start_jd)
    return max(0, min(11, int(fraction * 12)))


def whole_sign_house(chrt, sign, sidereal=False):
    """House represented by this sign in a whole-sign reading."""
    return (sign - asc_sign(chrt, sidereal)) % 12 + 1


def entries_for(radix, others, when, sidereal=False,
                solar_year=None, solar_start_jd=None,
                next_solar_jd=None, monthly_date_jd=None):
    """Return dict: glyph marks, sign areas and compact legend lines.

    - Annual sign is shown in every chart ring, including transits.
    - Monthly sign is shown in SR and LR rings, NOT radix or transit.
    - Annual, major and minor ruler glyphs are emphasized in all rings.
    - Monthly lord glyphs are emphasized in SR and LR.
    - Firdaria planets do NOT color their occupied houses.
    - All roles are independent, so a planet may show multiple roles.
    """
    result = {'marks': [], 'areas': [], 'legend': [], 'month_index': None,
              'annual_sign': None, 'monthly_sign': None}
    if getattr(radix, 'htype', None) != 0:
        return result
    if solar_year is None:
        solar_year = when.year
        birthday = (radix.time.origmonth, radix.time.origday)
        if (when.month, when.day) < birthday:
            solar_year -= 1
    annual = annual_profection(radix, solar_year, sidereal)
    if annual is None:
        return result
    sign, ruler, annual_house, age = annual
    result['annual_sign'] = sign
    annual_text = 'Annual: %s · H%d · %s' % (
        SIGNS[sign], annual_house, NAMES[ruler])
    result['legend'].append({'role': 'annual', 'text': annual_text})

    month = None
    if (solar_start_jd is not None and next_solar_jd is not None
            and monthly_date_jd is not None):
        month = monthly_index(solar_start_jd, next_solar_jd, monthly_date_jd)
    result['month_index'] = month
    monthly_sign = (sign + month) % 12 if month is not None else None
    result['monthly_sign'] = monthly_sign
    if month is not None:
        result['legend'].append({
            'role': 'monthly',
            'text': 'Month %d: %s · %s' % (
                month + 1, SIGNS[monthly_sign], NAMES[DOMICILE[monthly_sign]]),
        })

    fird = at_firdaria(radix, when)
    if fird:
        for role, pl in (('major', fird[0]), ('sub', fird[1])):
            if pl is not None:
                result['legend'].append({
                    'role': role,
                    'text': '%s: %s' % (ROLE_LABELS[role], NAMES[pl]),
                })

    for ring, chrt in enumerate([radix] + list(others)):
        result['areas'].append({
            'ring': ring, 'role': 'annual', 'sign': sign,
            'house': whole_sign_house(chrt, sign, sidereal),
        })
        for role, planet in [('annual', ruler)]:
            result['marks'].append({'ring': ring, 'role': role, 'planet': planet})
        if month is not None and getattr(chrt, 'htype', None) in (1, 2):
            result['areas'].append({
                'ring': ring, 'role': 'monthly', 'sign': monthly_sign,
                'house': whole_sign_house(chrt, monthly_sign, sidereal),
            })
            result['marks'].append({
                'ring': ring, 'role': 'monthly',
                'planet': DOMICILE[monthly_sign],
            })
        if fird:
            for role, planet in (('major', fird[0]), ('sub', fird[1])):
                if planet is not None:
                    result['marks'].append({
                        'ring': ring, 'role': role, 'planet': planet,
                    })
    return result
