"""Unexpected errors: shown in a message and appended to morinus-error.log in the
program folder, instead of being lost (wxPython only prints them to a console,
which a desktop launcher or the Windows program does not have)."""

import os
import sys
import datetime
import platform
import threading
import traceback

LOGFILE = 'morinus-error.log'
MAXLOG = 1000000	# the log is started again when it grows beyond this many bytes

_shown = set()
_lock = threading.Lock()


def _write(text):
	path = os.path.abspath(LOGFILE)
	try:
		mode = 'w' if os.path.exists(path) and os.path.getsize(path) > MAXLOG else 'a'
		with open(path, mode, encoding='utf-8') as f:
			f.write(text)
	except OSError:
		path = None
	return path


def _versions():
	try:
		import wx
		wxver = wx.version()
	except Exception:
		wxver = '?'
	return 'Python %s, wxPython %s, %s' % (platform.python_version(), wxver, platform.platform())


def report(exc_type, exc, tb, where=''):
	if issubclass(exc_type, KeyboardInterrupt):
		sys.__excepthook__(exc_type, exc, tb)
		return
	details = ''.join(traceback.format_exception(exc_type, exc, tb))
	if sys.stderr is not None:	# None in the Windows program, which has no console
		sys.stderr.write(details)
	stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	path = _write('==== %s%s\n%s\n%s\n' % (stamp, (' (%s)' % where) if where else '', _versions(), details))
	# the same error (e.g. while painting) is shown once per session
	key = traceback.format_exception_only(exc_type, exc)[-1] + ''.join(traceback.format_tb(tb)[-1:])
	with _lock:
		if key in _shown:
			return
		_shown.add(key)
	try:
		import wx
		import tradoptions
		if wx.GetApp() is None or not tradoptions.get('err_show'):
			return
		message = 'Something went wrong:\n\n%s\n' % traceback.format_exception_only(exc_type, exc)[-1].strip()
		if path:
			message += '\nThe details were saved to %s. Please send this file when reporting the problem.' % path
		wx.CallAfter(wx.MessageBox, message, 'Morinus', wx.OK | wx.ICON_ERROR)
	except Exception:
		pass


def _thread_hook(args):
	report(args.exc_type, args.exc_value, args.exc_traceback, 'thread')


def _unraisable_hook(u):
	# errors in threads started with _thread (e.g. primary directions) end up here
	if u.exc_type is not None:
		report(u.exc_type, u.exc_value, u.exc_traceback, 'thread')


def install():
	sys.excepthook = report
	threading.excepthook = _thread_hook
	sys.unraisablehook = _unraisable_hook
