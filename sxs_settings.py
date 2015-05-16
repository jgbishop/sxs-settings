import sublime, sublime_plugin

_WINDOW_ID = None
PREF_USE_ROWS_DEFAULT = False

def getSetting(pref, default):
	return sublime.load_settings('sxs_settings.sublime-settings').get(pref, default)

def openWindow(self, winType, useRows):
	global _WINDOW_ID

	if _WINDOW_ID is not None:
		windowList = sublime.windows()
		for i,w in enumerate(windowList):
			if w.id() == _WINDOW_ID:
				w.run_command("close_window")
				_WINDOW_ID = None
				return

	# Self in this context is the active window
	self.run_command("new_window")
	new_window = sublime.active_window()
	_WINDOW_ID = new_window.id()

	if useRows == True:
		new_window.set_layout({
		    "cols": [0, 1],
		    "rows": [0, 0.5, 1],
		    "cells": [[0, 0, 1, 1], [0, 1, 1, 2]]
		})
	else:
		new_window.set_layout({
		    "cols": [0, 0.5, 1],
		    "rows": [0, 1],
		    "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
		})

	if winType == "settings":
		caption = "Settings"
		leftFile = "${packages}/Default/Preferences.sublime-settings"
		rightFile = "${packages}/User/Preferences.sublime-settings"
		rightContents = "// Settings in here override those in \"Default/Preferences.sublime-settings\",\n// and are overridden in turn by file type specific settings.\n{\n\t$0\n}\n"
	elif winType == "keybindings":
		caption = "Key Bindings"
		leftFile = "${packages}/Default/Default ($platform).sublime-keymap"
		rightFile = "${packages}/User/Default ($platform).sublime-keymap"
		rightContents = "[\n\t$0\n]\n"

	new_window.run_command("open_file", {'file': leftFile, 'caption': caption + " - Default"})
	new_window.run_command("open_file", {'file': rightFile, 'caption': caption + " - User", 'contents': rightContents})
	new_window.set_view_index(new_window.active_view(), 1, 0)

class sxsSettingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		openWindow(self.window, "settings", getSetting('display_using_rows', PREF_USE_ROWS_DEFAULT))

class sxsKeyBindingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		openWindow(self.window, "keybindings", getSetting('display_using_rows', PREF_USE_ROWS_DEFAULT))
