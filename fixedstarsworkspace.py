"""Fixed Stars explorer: original catalogue, aspects and angular techniques."""
import wx
import fixedstarswnd
import fixedstarsframe
import fixedstarsaspectswnd
import fixedstarsaspectsframe
import fixedstaranglewnd
import legacytabworkspace
import fixedstarscatalog


def show(mainfr, tab=0):
    if mainfr.splash:
        return None
    if tab in (0, 1):
        if not mainfr.checkFixedStars():
            return None
        if not fixedstarscatalog.is_selected(mainfr.options.fixedstars):
            import mtexts
            wx.MessageBox(mtexts.txtscommon['NoSelFixedStars'], '',
                          wx.OK | wx.ICON_INFORMATION, parent=mainfr)
            return None

    existing = getattr(mainfr, 'fixed_stars_workspace', None)
    if existing:
        existing.selectTab(tab)
        existing.Show()
        existing.Raise()
        return existing

    chart = mainfr.horoscope
    options = mainfr.options
    specs = (
        (fixedstarscatalog.TABS[0], fixedstarscatalog.DESCRIPTIONS[0],
         lambda parent: fixedstarswnd.FixedStarsWnd(parent, chart, options, mainfr),
         lambda: _separate(fixedstarsframe.FixedStarsFrame, mainfr)),
        (fixedstarscatalog.TABS[1], fixedstarscatalog.DESCRIPTIONS[1],
         lambda parent: fixedstarsaspectswnd.FixedStarsAspectsWnd(parent, chart, options, mainfr),
         lambda: _separate(fixedstarsaspectsframe.FixedStarsAspectsFrame, mainfr)),
        (fixedstarscatalog.TABS[2], fixedstarscatalog.DESCRIPTIONS[2],
         lambda parent: fixedstaranglewnd.FixedStarAnglesWnd(parent, chart, options, mainfr),
         lambda: _separate(fixedstaranglewnd.FixedStarAnglesFrame, mainfr)),
    )
    wnd = legacytabworkspace.TableWorkspace(
        mainfr, 'Fixed Stars — ' + chart.name, specs, tab,
        size=(1150, 730), attribute='fixed_stars_workspace')
    mainfr.fixed_stars_workspace = wnd
    wnd.Show()
    wnd.Raise()
    return wnd


def _separate(frameclass, mainfr):
    wnd = frameclass(mainfr, mainfr.title, mainfr.horoscope, mainfr.options)
    wnd.Show()
    return wnd
