import sublime, sublime_plugin
import re

_WINDOW_ID = None

def closeWindowIfNeeded(self):
	global _WINDOW_ID

	if _WINDOW_ID is not None:
		for i,w in enumerate(sublime.windows()):
			if w.id() == _WINDOW_ID:
				w.run_command("close_window")
				_WINDOW_ID = None
				return True
	return False

def getSetting(pref, default):
	return sublime.load_settings('sxs_settings.sublime-settings').get(pref, default)

def openWindow(self, leftPath):
	global _WINDOW_ID

	# Self in this context is the active window
	self.run_command("new_window")
	new_window = sublime.active_window()
	_WINDOW_ID = new_window.id()

	if getSetting('display_using_rows', False) == True:
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

	new_window.run_command("distraction_free_window")

	if getSetting('open_in_distraction_free', False):
		new_window.run_command('toggle_distraction_free')
		new_window.run_command('toggle_tabs')

	lastSlash = leftPath.rfind("/")
	rightPath = leftPath[(lastSlash+1):] # Extract the filename

	# If we're opening a .sublime-keymap file, the right pane should always open
	# to "Default ({platform}).sublime-keymap" since that's where keys should be
	# put.
	if re.search(r"\.sublime-keymap", leftPath):
		platform = "Windows" # Assume this to start (evil, I know)
		plat = sublime.platform()
		if plat == "linux":
			platform = "Linux"
		elif plat == "osx":
			platform = "OSX"

		rightPath = "Default (" + platform + ").sublime-keymap"

	# Test to see if we are opening a platform-specific settings file. If so,
	# strip the platform specific portion of the filename (platform-specific
	# files are ignored in the User directory)
	elif re.search(r" \((?:Linux|OSX|Windows)\).sublime-settings", leftPath):
		rightPath = re.sub(r" \((?:Linux|OSX|Windows)\)", "", rightPath)

	rightContents = "{\n\t$0\n}\n" # Default to object notation for sublime-settings files
	if re.search(r"\.sublime-keymap", leftPath):
		rightContents = "[\n\t$0\n]\n"; # Use array notation for sublime-keymap files

	new_window.run_command("open_file", {'file': "${packages}/" + leftPath})
	new_window.run_command("open_file", {'file': "${packages}/User/" + rightPath, 'contents': rightContents })
	new_window.set_view_index(new_window.active_view(), 1, 0)

class sxsSettingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		if closeWindowIfNeeded(self) == True:
			return
		openWindow(self.window, "Default/Preferences.sublime-settings")

class sxsKeyBindingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		if closeWindowIfNeeded(self) == True:
			return
		openWindow(self.window, "Default/Default ($platform).sublime-keymap")

class sxsSelectFileCommand(sublime_plugin.WindowCommand):
	fileList = []

	def run(self):
		if closeWindowIfNeeded(self) == True:
			return

		self.fileList[:] = [] # Clear our cache

		settingsList = sublime.find_resources("*.sublime-settings")
		keymapList = sublime.find_resources("*.sublime-keymap")

		tempList = settingsList + keymapList

		for i, item in enumerate(tempList):
			tempItem = re.sub(r"^Packages/", "", item)
			if re.match(r"User/", tempItem):
				continue # Ignore anything we find in the User directory (those will get treated as "right pane" files)
			else:
				self.fileList.append(tempItem)

		self.fileList.sort()
		self.window.show_quick_panel(self.fileList, self.onDone)

	def is_enabled(self):
		return (int(sublime.version()) >= 3000)

	def is_visible(self):
		return (int(sublime.version()) >= 3000)

	def onDone(self, index):
		if index == -1:
			return
		openWindow(self.window, self.fileList[index])
