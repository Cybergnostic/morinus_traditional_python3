"""Windows open with the size and position they had when last closed, per kind of
window (main window, each table, chart windows), kept in Opts/windows.json."""

import os
import json
import wx
import tradoptions

FILENAME = os.path.join('Opts', 'windows.json')

_saved = None


def _load():
	global _saved
	if _saved is None:
		try:
			with open(FILENAME, encoding='utf-8') as f:
				_saved = json.load(f)
		except (OSError, ValueError):
			_saved = {}
	return _saved


def _store(frame):
	if not tradoptions.get('win_remember'):
		return
	if frame.IsMaximized() or frame.IsIconized() or frame.IsFullScreen():
		return
	saved = _load()
	saved[type(frame).__name__] = list(frame.GetPosition()) + list(frame.GetSize())
	try:
		with open(FILENAME, 'w', encoding='utf-8') as f:
			json.dump(saved, f, indent=1, sort_keys=True)
	except OSError:
		pass


def _restore(frame):
	if not tradoptions.get('win_remember'):
		return
	geometry = _load().get(type(frame).__name__)
	if not geometry or len(geometry) != 4:
		return
	x, y, w, h = geometry
	minw, minh = frame.GetMinSize()
	frame.SetSize((max(w, minw), max(h, minh)))
	# only where a screen is now (a second monitor may be gone)
	if wx.Display.GetFromPoint(wx.Point(x + 40, y + 20)) != wx.NOT_FOUND:
		frame.SetPosition((x, y))


def _onDestroy(event):
	frame = event.GetEventObject()
	if isinstance(frame, wx.Frame) and event.GetWindow() is frame:
		try:
			_store(frame)
		except Exception:
			pass
	event.Skip()


_show = None


def _showRemembered(self, show=True):
	if show and not getattr(self, '_windowmemory', False):
		self._windowmemory = True
		_restore(self)
		self.Bind(wx.EVT_WINDOW_DESTROY, _onDestroy)
	return _show(self, show)


def install():
	global _show
	_show = wx.Frame.Show	# as it is now (gtkfit may have replaced it)
	wx.Frame.Show = _showRemembered
