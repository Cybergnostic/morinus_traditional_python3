# UI checkpoints

Baseline commit: 36cc569e1374bf54ea0523ad70aff901c2ef2019.
Checkpoint branch: checkpoint/ui-2026-10-21.
Integration branch: ui-next. Original ui and main stay untouched.

## A1: Resizable sidebar

Draggable native divider for natal, transit, and return charts.
Preferred width is saved in the separate Opts/traditional.json file when settings are saved.
Spacing and headings are refined using system palette colors.
No astrological calculation or original .opt format changes.

Test with python -m unittest discover -s tests -p 'test_sidebar_width.py'
GUI review: sidebar dragging and minimum window sizes on Linux and Windows.
The GitHub integration cannot execute the GUI, so this remains subject to local review.

## A2: Command palette

- New toolbar-independent Ctrl+K command palette with a keyboard-navigable results list.
- Toolbar button opens the same palette; no popup/focus race or hidden-toolbar dependency.
- Search considers command name, menu path and help text, with name-first ranking.
- Search ranking is independent of wxPython and covered by tests/test_commandindex.py.
- The original menu-command handlers are reused unchanged.
- Feature branch: feature/ui-command-palette (stacked on A1 until CI review).

Run: python -m unittest discover -s tests -p 'test_commandindex.py'
GUI review: Ctrl+K with toolbar on/off, Escape, arrows, Enter, mouse double-click, checkable menu commands and settings dialogs.
