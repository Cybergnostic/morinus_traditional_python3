"""The pens of the chart wheel by the role of each line, so that its weight and
colour come from one place. 'morinus' lines are those of Morinus 6 (the main
circles and the sign boundaries 3 pixels wide on large charts); 'fine' lines
are lighter: the main structure 2 pixels, the ticks and the dividers of terms
and decans 1 pixel in a lighter shade of the frame colour."""

import wx
import tradoptions

SMALL, MEDIUM = 400, 600	# GraphChart.SMALL_SIZE, MEDIUM_SIZE

# frame roles: their widths on small, medium and large charts
WIDTHS = {
	'morinus': {'major': (1, 2, 3), 'circle': (1, 1, 1), 'tick10': (1, 1, 2), 'tick1': (1, 1, 1), 'divider': (1, 1, 1), 'pointer': (1, 1, 2)},
	'fine': {'major': (1, 1, 2), 'circle': (1, 1, 1), 'tick10': (1, 1, 1), 'tick1': (1, 1, 1), 'divider': (1, 1, 1), 'pointer': (1, 1, 1)},
}
# roles drawn in the lighter shade with fine lines
LIGHT = ('tick1', 'tick10', 'divider', 'pointer')


def mix(a, b, t):
	"""Colour a moved towards b by t (0..1)."""
	return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))


def width(role, chartsize, lines=None):
	w = WIDTHS[lines or tradoptions.get('chart_lines')][role]
	return w[0] if chartsize <= SMALL else w[1] if chartsize <= MEDIUM else w[2]


def frame_pen(options, bw, chartsize, role):
	"""The pen of a line of the frame (circles, ticks, sign boundaries,
	dividers, planet pointers)."""
	clr = (0, 0, 0) if bw else options.clrframe
	lines = tradoptions.get('chart_lines')
	if lines == 'fine' and role in LIGHT:
		bkg = (255, 255, 255) if bw else options.clrbackground
		clr = mix(clr, bkg, 0.45)
	return wx.Pen(wx.Colour(*clr), width(role, chartsize, lines))
