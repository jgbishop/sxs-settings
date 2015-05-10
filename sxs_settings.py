import sublime, sublime_plugin

PREF_USE_ROWS_DEFAULT = False

def getSetting(pref, default):
	return sublime.load_settings('sxs_settings.sublime-settings').get(pref, default)

def openWindow(self, winType, useRows):
	# Self in this context is the active window
	self.run_command("new_window")
	new_window = sublime.active_window()

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

	elif winType == "mousebindings":
		caption = "Mouse Bindings"
		leftFile = "${packages}/Default/Default ($platform).sublime-mousemap"
		rightFile = "${packages}/User/Default ($platforn).sublime-mousemap"
		rightContents = "[\n\t$0\n]\n"

	elif winType == "commands":
		caption = "Commands"
		leftFile = "${packages}/Default/Default.sublime-commands"
		rightFile = "${packages}/User/Default.sublime-commands"
		rightContents = "[\n\t$0\n]\n"

	elif winType == "main_menu":
		caption = "Main Menu"
		leftFile = "${packages}/Default/Main.sublime-menu"
		rightFile = "${packages}/User/Main/sublime-menu"
		rightContents = "[\n\t$0\n]\n"
	
	elif winType == "sidebar_menu":
		caption = "Sidebar Menu"
		leftFile = "${packages}/Default/Side Bar.sublime-menu"
		rightFile = "${packages}/User/Side Bar.sublime-menu"
		rightContents = "[\n\t$0\n]\n"

	if winType != "settings" or "keybindings" or "mousebindings":
		new_window.run_command("open_file", {'file': leftFile, 'caption': caption})
		new_window.run_command("open_file", {'file': rightFile, 'caption': caption, 'contents': rightContents})
	else:
		new_window.run_command("open_file", {'file': leftFile, 'caption': caption + " - Default"})
		new_window.run_command("open_file", {'file': rightFile, 'caption': caption + " - User", 'contents': rightContents})

	new_window.set_view_index(new_window.active_view(), 1, 0)

class sxsSettingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		openWindow(self.window, "settings", getSetting('display_using_rows', PREF_USE_ROWS_DEFAULT))

class sxsKeyBindingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		openWindow(self.window, "keybindings", getSetting('display_using_rows', PREF_USE_ROWS_DEFAULT))

class sxsMouseBindingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		openWindow(self.window, "mousebindings", getSetting("display_using_rows", PREF_USE_ROWS_DEFAULT))

class sxsMainMenuCommand(sublime_plugin.WindowCommand):
	def run(self):
		openWindow(self.window, "main_menu", getSetting("display_using_rows", PREF_USE_ROWS_DEFAULT))

class sxsSidebarMenuCommand(sublime_plugin.WindowCommand):
	def run(self):
		openWindow(self.window, "sidebar_menu", getSetting("display_using_rows", PREF_USE_ROWS_DEFAULT))