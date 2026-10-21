"""Pure command ranking, independent of wxPython and suitable for unit tests."""
import re
import unicodedata

MAX_RESULTS = 12


def normalise(value):
    """Case/diacritic-insensitive words; punctuation separates words."""
    value = unicodedata.normalize('NFKD', str(value or '')).casefold()
    value = ''.join(ch for ch in value if not unicodedata.combining(ch))
    return ' '.join(re.findall(r'[^\W_]+', value, flags=re.UNICODE))


def search(cmds, query, limit=MAX_RESULTS):
    """Filter all query words, ranking command names before paths and help.

    Commands are tuples (label, menu path, help, callback). Stable ties keep
    their original menu order, and exact/word-start matches lead the results.
    """
    q = normalise(query)
    words = q.split()
    if not words:
        return []
    found = []
    for index, command in enumerate(cmds):
        label, path, help_text = (normalise(x) for x in command[:3])
        combined = ' '.join((label, path, help_text))
        if not all(word in combined for word in words):
            continue
        label_words = label.split()
        if label == q:
            rank = 0
        elif label.startswith(q):
            rank = 1
        elif all(any(part.startswith(word) for part in label_words) for word in words):
            rank = 2
        elif all(word in label for word in words):
            rank = 3
        elif all(word in label + ' ' + path for word in words):
            rank = 4
        else:
            rank = 5
        found.append(((rank, len(label), index), command))
    found.sort(key=lambda x: x[0])
    return [c for _, c in found[:limit]]
