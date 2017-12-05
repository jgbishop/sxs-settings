
import re

import sublime
import sublime_plugin


last_accessed_settings_input = 0

def getSetting(pref, default):
	return sublime.load_settings('sxs_settings.sublime-settings').get(pref, default)

def openWindow(self, leftPath):

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

	rightContents = ""

	try:
		import OverrideEditSettingsDefaultContents

	except ImportError:

		rightContents = "{\n\t$0\n}\n" # Default to object notation for sublime-settings files
		if re.search(r"\.sublime-keymap", leftPath):
			rightContents = "[\n\t$0\n]\n"; # Use array notation for sublime-keymap files

	sublime.active_window().run_command("edit_settings", {'base_file': "${packages}/" + leftPath, "default": rightContents})
	active_window = sublime.active_window()

	if getSetting('open_in_distraction_free', False):
		active_window.run_command('toggle_distraction_free')
		active_window.run_command('toggle_tabs')

class sxsSelectFileCommand(sublime_plugin.WindowCommand):
	fileList = []

	def run(self):
		# Clear our cache
		self.fileList[:] = []

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
		self.window.show_quick_panel(self.fileList, self.onDone, 0, last_accessed_settings_input)

	def is_enabled(self):
		return (int(sublime.version()) >= 3000)

	def is_visible(self):
		return (int(sublime.version()) >= 3000)

	def onDone(self, index):
		global last_accessed_settings_input

		if index == -1:
			return

		last_accessed_settings_input = index
		openWindow(self.window, self.fileList[index])
