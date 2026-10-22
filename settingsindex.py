"""Find individual settings using the same ranking as Morinus command search.

Records contain title, category, group, description and a reference to the
real control. Searching never reads or changes a setting's value.
"""
from commandindex import search as ranked_search


def categories(definitions):
    """Unfiltered navigation records (one for each category)."""
    return [
        {'title': name, 'category': name, 'category_index': index,
         'description': '', 'group': '', 'control': None}
        for index, (name, entries) in enumerate(definitions)
    ]


def label(entry):
    """Helpful result text, distinguishing identically named fields."""
    group = entry.get('group', '')
    title = entry['title'] + (' (' + group + ')' if group else '')
    return title + '  —  ' + entry['category']


def search(records, query, limit=60):
    """Return exact setting results, ranked by name, group and description."""
    commands = [(rec['title'], ' '.join((rec['category'], rec.get('group', ''))),
                 rec.get('description', '') + ' ' + rec.get('english', ''), rec) for rec in records]
    return [item[3] for item in ranked_search(commands, query, limit)]
