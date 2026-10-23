"""Chart-source and creation-menu rules shared by multiwheel ring pickers.

No wx imports: source identity and menu coverage can be tested separately
from the GUI and without constructing astrological charts.
"""


CREATE_GROUPS = (
    ('New charts', (
        ('New chart...', 'new'),
        ('Here and now (horary)', 'here_now'),
        ('Synastry chart...', 'synastry'),
    )),
    ('Returns', (
        ('Solar return...', 'solar'),
        ('Lunar return...', 'lunar'),
        ('Saturn return...', 'saturn'),
        ('Jupiter return...', 'jupiter'),
        ('Mars return...', 'mars'),
        ('Venus return...', 'venus'),
        ('Mercury return...', 'mercury'),
    )),
    ('Transits and directions', (
        ('Transits...', 'transits'),
        ('Sun transits...', 'sun_transits'),
        ('Secondary directions...', 'secondary'),
        ('Profections...', 'profections'),
        ('Elections...', 'elections'),
    )),
    ('Lunations', (
        ('Prenatal syzygy', 'syzygy'),
        ('Other prenatal syzygy', 'syzygy_other'),
    )),
)


def merge_chart_sources(active, open_charts, retained):
    """Return selectable (label, chart) pairs, once per chart object.

    The active horoscope is always first, followed by retained charts with
    meaningful labels, then charts discovered from other windows.
    Retaining objects lets users close a temporary source window without
    losing the chart they explicitly added to the multiwheel.
    """
    sources = []
    seen = set()
    for label, chrt in ((('Active', active),) + tuple(retained) + tuple(open_charts)):
        if chrt is None or id(chrt) in seen:
            continue
        seen.add(id(chrt))
        sources.append((label, chrt))
    return sources
