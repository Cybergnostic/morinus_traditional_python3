"""Fixed Stars explorer: original catalogue, aspects and angular techniques."""
import wx
import mtexts
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
    if not mainfr.checkFixedStars():
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
         lambda parent: _needs_stars(parent, mainfr, lambda: fixedstarswnd.FixedStarsWnd(parent, chart, options, mainfr)),
         lambda view: _separate(fixedstarsframe.FixedStarsFrame, mainfr, True)),
        (fixedstarscatalog.TABS[1], fixedstarscatalog.DESCRIPTIONS[1],
         lambda parent: _needs_stars(parent, mainfr, lambda: fixedstarsaspectswnd.FixedStarsAspectsWnd(parent, chart, options, mainfr)),
         lambda view: _separate(fixedstarsaspectsframe.FixedStarsAspectsFrame, mainfr, True)),
        (fixedstarscatalog.TABS[2], fixedstarscatalog.DESCRIPTIONS[2],
         lambda parent: fixedstaranglewnd.FixedStarAnglesWnd(parent, chart, options, mainfr),
         lambda view: _separate(fixedstaranglewnd.FixedStarAnglesFrame, mainfr)),
    )
    wnd = legacytabworkspace.TableWorkspace(
        mainfr, 'Fixed Stars — ' + chart.name, specs, tab,
        size=(1150, 730), attribute='fixed_stars_workspace')
    mainfr.fixed_stars_workspace = wnd
    wnd.Show()
    wnd.Raise()
    return wnd


def _needs_stars(parent, mainfr, build):
    """The table, or a note when no fixed stars are selected (Settings > Fixed stars)."""
    if fixedstarscatalog.is_selected(mainfr.options.fixedstars):
        return build()
    return wx.StaticText(parent, -1, '\n  ' + mtexts.txtscommon['NoSelFixedStars'] +
                         '\n  Choose them in Settings > Fixed stars and visibility.')


def _separate(frameclass, mainfr, needs_stars=False):
    if needs_stars and not fixedstarscatalog.is_selected(mainfr.options.fixedstars):
        wx.MessageBox(mtexts.txtscommon['NoSelFixedStars'], '', wx.OK | wx.ICON_INFORMATION, parent=mainfr)
        return None
    wnd = frameclass(mainfr, mainfr.title, mainfr.horoscope, mainfr.options)
    wnd.Show()
    return wnd
