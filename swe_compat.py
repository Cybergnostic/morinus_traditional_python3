"""The part of the pyswisseph API that hor_tools uses, implemented on top of
Morinus's own Swiss Ephemeris module (astrology/sweastrology), so the
traditional-analysis code runs without an extra library.

install() registers it as the "swisseph" module unless pyswisseph is
installed, in which case the real one is used.
"""

import sys

import astrology

SUN = astrology.SE_SUN
MOON = astrology.SE_MOON
MERCURY = astrology.SE_MERCURY
VENUS = astrology.SE_VENUS
MARS = astrology.SE_MARS
JUPITER = astrology.SE_JUPITER
SATURN = astrology.SE_SATURN
TRUE_NODE = astrology.SE_TRUE_NODE
MEAN_NODE = astrology.SE_MEAN_NODE

FLG_SWIEPH = astrology.SEFLG_SWIEPH
FLG_SPEED = astrology.SEFLG_SPEED
FLG_EQUATORIAL = astrology.SEFLG_EQUATORIAL

GREG_CAL = astrology.SE_GREG_CAL
JUL_CAL = astrology.SE_JUL_CAL

CALC_RISE = astrology.SE_CALC_RISE
CALC_SET = astrology.SE_CALC_SET
BIT_DISC_CENTER = astrology.SE_BIT_DISC_CENTER

ECL2HOR = astrology.SE_ECL2HOR
EQU2HOR = astrology.SE_EQU2HOR
ECL = 0
EQU = 1


class Error(Exception):
    pass


def set_ephe_path(path):
    astrology.swe_set_ephe_path(path)


def julday(year, month, day, hour=12.0, cal=GREG_CAL):
    return astrology.swe_julday(int(year), int(month), int(day), float(hour), int(cal))


def revjul(jd, cal=GREG_CAL):
    return astrology.swe_revjul(float(jd), int(cal))


def sidtime(jd_ut):
    return astrology.swe_sidtime(float(jd_ut))


def calc_ut(jd_ut, body, flags=FLG_SWIEPH | FLG_SPEED):
    (ret,), xx, (serr,) = astrology.swe_calc_ut(float(jd_ut), int(body), int(flags))
    if ret < 0:
        raise Error(serr)
    return tuple(xx), ret


def houses_ex(jd_ut, lat, lon, hsys=b'P', flags=0):
    if isinstance(hsys, (bytes, bytearray)):
        hsys = hsys.decode('ascii')
    (ret,), cusps, ascmc = astrology.swe_houses_ex(float(jd_ut), int(flags), float(lat), float(lon), ord(hsys))
    # pyswisseph returns the 12 cusps without the unused element 0, and 8 ascmc values
    return tuple(cusps[1:13]), tuple(ascmc[:8])


def azalt(jd_ut, flag, geopos, atpress, attemp, xin):
    lon, lat, height = geopos
    x0, x1, x2 = (tuple(xin) + (1.0,))[:3]
    return astrology.swe_azalt(float(jd_ut), int(flag), float(lon), float(lat), float(height), float(atpress), float(attemp), float(x0), float(x1), float(x2))


def rise_trans(tjdut, body, rsmi=0, geopos=(0.0, 0.0, 0.0), atpress=0.0, attemp=0.0, flags=FLG_SWIEPH):
    lon, lat, height = geopos
    ret, tret, serr = astrology.swe_rise_trans(float(tjdut), int(body), '', int(flags), int(rsmi), float(lon), float(lat), float(height), float(atpress), float(attemp))
    if ret < 0:
        raise Error(serr)
    return ret, (tret,)+(0.0,)*9


def _traditional(star):
    """A star name of the old catalogue (starnames.TRADITIONAL) as its designation,
    e.g. Deneb Okab, which Swiss Ephemeris 2.10 calls Delta Aquilae."""
    import starnames
    for nom, name in starnames.TRADITIONAL.items():
        if name.lower() == star.strip().lower():
            return ',' + nom
    return None


def fixstar_ut(star, jd_ut, flags=FLG_SWIEPH):
    (ret,), (name,), xx, (serr,) = astrology.swe_fixstar_ut(star, float(jd_ut), int(flags))
    if ret < 0 and _traditional(star):
        (ret,), (name,), xx, (serr,) = astrology.swe_fixstar_ut(_traditional(star), float(jd_ut), int(flags))
    if ret < 0:
        raise Error(serr)
    return tuple(xx), name, ret


def fixstar_mag(star):
    (ret,), (name,), (mag,), (serr,) = astrology.swe_fixstar_mag(star)
    if ret < 0 and _traditional(star):
        (ret,), (name,), (mag,), (serr,) = astrology.swe_fixstar_mag(_traditional(star))
    if ret < 0:
        raise Error(serr)
    return mag, name


def install():
    """Make "import swisseph" work, preferring a real pyswisseph if installed."""
    if 'swisseph' in sys.modules:
        return
    try:
        import swisseph	# noqa: F401
    except ImportError:
        sys.modules['swisseph'] = sys.modules[__name__]
