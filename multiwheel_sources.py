"""Chart-source and creation-menu rules shared by multiwheel ring pickers.

No wx imports: source identity and menu coverage can be tested separately
from the GUI and without constructing astrological charts.
"""

import os
import pickle
from dataclasses import dataclass


@dataclass(frozen=True)
class RecentNatal:
    """A recent .hor file shown without constructing a chart until selected."""

    path: str
    name: str
    birth: str


class _HeaderUnpickler(pickle.Unpickler):
    """Inspect primitive .hor headers without allowing pickle class imports."""

    def find_class(self, module, name):
        raise pickle.UnpicklingError('Class lookup is not allowed in chart headers')


def recent_natal(path, radix_type):
    """Return a lazy recent natal entry, or None for other/invalid charts.

    Only the first three primitive .hor fields are inspected. The complete
    chart is loaded by Morinus if the user actually selects this entry.
    """
    try:
        with open(path, 'rb') as stream:
            header = _HeaderUnpickler(stream)
            name, male, kind = (header.load(), header.load(), header.load())
            bc, year, month, day, hour, minute = (header.load() for _ in range(6))
    except (OSError, EOFError, pickle.UnpicklingError, ValueError, TypeError):
        return None
    if not isinstance(name, str) or not isinstance(male, bool) or type(kind) is not int:
        return None
    if (not isinstance(bc, bool) or any(type(item) is not int
            for item in (year, month, day, hour, minute))):
        return None
    if kind != radix_type:
        return None
    year_text = '%d BC' % year if bc else '%04d' % year
    birth = '%s-%02d-%02d %02d:%02d' % (year_text, month, day, hour, minute)
    return RecentNatal(os.path.abspath(path), name, birth)


def inner_chart_sources(active, open_charts, retained, radix_type,
                        manual_labels=()):
    """The centre picker omits derived charts from other rings and windows.

    Explicit file loads and newly entered charts remain selectable regardless
    of type. The active chart is always retained even if it is not natal.
    """
    deliberate = {'File', 'New chart', 'Here and now', *manual_labels}

    def allowed(source):
        label, chrt = source
        return (chrt is not None and
                (getattr(chrt, 'htype', None) == radix_type or label in deliberate))
    return merge_chart_sources(active, filter(allowed, open_charts),
                               filter(allowed, retained))


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


def keep_selected(sources, selected, label):
    """Append the current selection if it is no longer among the sources.

    Only real charts (objects with an htype) are kept; a lazy recent-file
    entry or nothing at all is not.
    """
    if (selected is None or not hasattr(selected, 'htype') or
            any(chrt is selected for _, chrt in sources)):
        return list(sources)
    return list(sources) + [(label, selected)]


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
