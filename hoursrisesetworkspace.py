"""Planetary Hours / Rise-Set workspace, using the existing Morinus tables.

Planetary-hour sunrise/sunset boundaries, astronomical rising/setting
calculations, and their native time conventions are not changed here.
"""
import hourswnd
import hoursframe
import risesetwnd
import risesetframe
import legacytabworkspace


def _open_original(cls, mainfr):
    frame = cls(mainfr, mainfr.title, mainfr.horoscope, mainfr.options)
    frame.Show()
    return frame


def show(mainfr, tab=0):
    if mainfr.splash:
        return None
    existing = getattr(mainfr, 'hours_riseset_workspace', None)
    if existing:
        existing.selectTab(tab)
        existing.Show()
        existing.Raise()
        return existing
    chart, options = mainfr.horoscope, mainfr.options
    specs = (
        ('Planetary hours',
         'Planetary day, Sun rise and set, and planetary hours in chart-local time.',
         lambda page: hourswnd.HoursWnd(page, chart, options, mainfr),
         lambda: _open_original(hoursframe.HoursFrame, mainfr)),
        ('Rise, set and culmination',
         'Existing planet rise/MC/set/IC times and rising times of zodiacal signs.',
         lambda page: risesetwnd.RiseSetWnd(page, chart, options, mainfr),
         lambda: _open_original(risesetframe.RiseSetFrame, mainfr)),
    )
    wnd = legacytabworkspace.TableWorkspace(mainfr,
        'Planetary Hours and Rise/Set — ' + chart.name, specs, tab,
        size=(850, 650), attribute='hours_riseset_workspace')
    mainfr.hours_riseset_workspace = wnd
    wnd.Show()
    wnd.Raise()
    return wnd
