import sublime, sublime_plugin

def openWindow(self, winType):
	# Self in this context is the active window
	self.run_command("new_window")
	new_window = sublime.active_window()
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
	elif winType == "commands":
		caption = "Commands"
		leftFile = "${packages}/Default/Default.sublime-commands"
		rightFile = "${packages}/User/Default.sublime-commands"
		rightContents = "[\n\t$0\n]\n"
	new_window.run_command("open_file", {'file': leftFile, 'caption': caption})
	new_window.run_command("open_file", {'file': rightFile, 'caption': caption, 'contents': rightContents})
	new_window.set_view_index(new_window.active_view(), 1, 0)

class sxsSettingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		openWindow(self.window, "settings")

class sxsKeyBindingsCommand(sublime_plugin.WindowCommand):
	def run(self):
		openWindow(self.window, "keybindings")
class sxsCommandsCommand(sublime_plugin.WindowCommand):
	def run(self):
		openWindow(self.window, "commands")