"""Translation of the texts added to Morinus after 6.2, which are written in
English in the code (Morinus's own texts are in mtexts). tr(text) is the
Serbian text when Serbian is chosen, otherwise the text itself; texts it does
not know (chart names, numbers, Morinus's own translated texts) pass unchanged,
and so do lists and tuples of texts, element by element. A menu text keeps its
keyboard shortcut after the tab."""

import mtexts

SERBIAN = 3	# index of Srpski in mtexts.langtexts


def tr(text):
	if mtexts.current != SERBIAN:
		return text
	if isinstance(text, (list, tuple)):
		return type(text)(tr(t) for t in text)
	if not isinstance(text, str):
		return text
	label, tab, keys = text.partition('\t')
	return _serbian(label) + tab + keys


def _serbian(text):
	import i18n_sr
	if text in i18n_sr.TEXTS:
		return i18n_sr.TEXTS[text]
	for end in ('...', ':'):	# 'Settings...', 'Theme:'
		if text.endswith(end) and text[:-len(end)] in i18n_sr.TEXTS:
			return i18n_sr.TEXTS[text[:-len(end)]] + end
	return text
