"""Native table for the Valens planetary divisions of a solar return."""

from datetime import datetime, timedelta, timezone

import astrology
import chart
import houses
import i18n
import planets
import returnslist
import tablewnd

import divisions


PLANET_IDS = {
    "Saturn": planets.Planets.SATURN,
    "Jupiter": planets.Planets.JUPITER,
    "Mars": planets.Planets.MARS,
    "Sun": planets.Planets.SUN,
    "Venus": planets.Planets.VENUS,
    "Mercury": planets.Planets.MERCURY,
    "Moon": planets.Planets.MOON,
}
SIGNS = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)


def _utc_from_jd(jd):
    year, month, day, hour = astrology.swe_revjul(jd, astrology.SE_GREG_CAL)
    return datetime(year, month, day, tzinfo=timezone.utc) + timedelta(hours=hour)


def _solar_year(radix, solar):
    """Match a return to its actual anniversary, including year-boundary births."""
    return returnslist.solar_year_for_chart(radix, solar)


def _zodiac_longitude(chrt, longitude):
    """Use the same zodiac setting as Morinus's displayed chart."""
    return ((longitude - chrt.ayanamsha) if chrt.options.ayanamsha else longitude) % 360.0


def schedule_for_chart(radix, solar):
    if solar.htype != chart.Chart.SOLAR:
        raise ValueError("Divisions require a solar return chart")
    year = _solar_year(radix, solar)
    next_t = returnslist.solar_return(radix, year + 1)
    if next_t is None:
        raise ValueError("Could not calculate the following solar return")
    positions = {
        name: _zodiac_longitude(solar, solar.planets.planets[pid].data[planets.Planet.LON])
        for name, pid in PLANET_IDS.items()
    }
    return divisions.calculate_divisions(
        _utc_from_jd(solar.time.jd),
        _utc_from_jd(returnslist.gmt_time(next_t, radix).jd),
        _zodiac_longitude(radix, radix.houses.ascmc[houses.Houses.ASC]),
        radix.time.origyear,
        year,
        _zodiac_longitude(solar, solar.houses.ascmc[houses.Houses.ASC]),
        positions,
    )


class DivisionsWnd(tablewnd.TableWnd):
    HEADERS = ('No.', 'Lord', 'Start (UTC)', 'End (UTC)', 'Valens days', 'SR house')

    def __init__(self, parent, radix, solar, options, mainfr):
        tablewnd.TableWnd.__init__(self, parent, solar, options, mainfr)
        schedule = schedule_for_chart(radix, solar)
        summary = [
            ('Annual profection sign', SIGNS[schedule.profected_sign]),
            ('Ruler of the year', schedule.year_ruler),
        ]
        now = datetime.now(timezone.utc)
        rows, colours = [], []
        for period in schedule.periods:
            current = period.start <= now < period.end
            rows.append((
                str(period.number) + (' *' if current else ''),
                period.ruler,
                period.start.strftime('%Y-%m-%d %H:%M'),
                period.end.strftime('%Y-%m-%d %H:%M'),
                str(period.nominal_days),
                str(period.solar_house),
            ))
            colours.append(options.clrplanets[PLANET_IDS[period.ruler]])
        self.sections = [tablewnd.Section(summary), tablewnd.Section(rows, self.HEADERS, colours)]
        self.notes = [
            'Secondary zodiacal order from the ruler of the year; * = current period.',
            'Fixed 365-day Valens cycle; last lord continues until the next solar return.',
        ]
        self.layout()

    def getExt(self):
        return '_Divisions'


class DivisionsFrame(tablewnd.TableFrame):
    def __init__(self, parent, title, radix, solar, options):
        tablewnd.TableFrame.__init__(
            self, parent, title + ' - ' + i18n.tr('Divisions (Valens)'),
            lambda frame: DivisionsWnd(frame, radix, solar, options, parent),
        )
