"""Run a main-window chart command for another natal chart.

The Charts menu handlers of Morinus (returns, transits, directions, ...)
compute from MFrame.horoscope and keep dialogs initialised from it. A window
that shows a different natal (the multi-wheel's centre) lends its chart for
the duration of one command, so the new chart and its window's radix belong
to that natal, not to the chart open in the main window.
"""

from contextlib import contextmanager

# MFrame's dialogs initialised from its horoscope (see MFrame.destroyDlgs).
CACHED_DIALOGS = ('trdatedlg', 'trmondlg', 'suntrdlg', 'revdlg', 'secdirdlg',
                  'pdrangedlg')


@contextmanager
def lend(mainfr, radix):
	if radix is None or radix is mainfr.horoscope:
		yield
		return
	saved = mainfr.horoscope
	stashed = {name: getattr(mainfr, name, None) for name in CACHED_DIALOGS}
	for name in CACHED_DIALOGS:
		setattr(mainfr, name, None)
	mainfr.horoscope = radix
	try:
		yield
	finally:
		# Dialogs made for the lent chart must not be reused for the main one.
		for name in CACHED_DIALOGS:
			made = getattr(mainfr, name, None)
			if made is not None and made is not stashed[name]:
				made.Destroy()
			setattr(mainfr, name, stashed[name])
		mainfr.horoscope = saved
		# A resize while the chart was lent would have drawn the lent chart.
		if not mainfr.splash:
			mainfr.drawBkg()
			mainfr.Refresh()
