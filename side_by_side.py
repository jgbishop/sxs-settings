import sublime
import sublime_plugin as plugin

_WINDOW_ID = None

def Settings(k,v):
	return sublime.load_settings('side_by_side.sublime-settings').get(k,v)

def openWindow(self,winType,useRows,openDistFree):
	global _WINDOW_ID

	if _WINDOW_ID is not None:
		windowList = sublime.windows()
		for i,w in enumerate(windowList):
			if w.id() == _WINDOW_ID:
				w.run_command("close_window")
				_WINDOW_ID = None
				return
	
	self.run_command('new_window')
	new_window = sublime.active_window()
	_WINDOW_ID = new_window.id()
	
	if useRows == True:
		new_window.set_layout({
			'cols':[0,1],
			'rows':[0,0.5,1],
			'cells':[[0,0,1,1],[0,1,1,2]]
		})
	else:
		new_window.set_layout({
			'cols':[0,0.5,1],
			'rows':[0,1],
			'cells':[[0,0,1,1],[1,0,2,1]]
		})

	if openDistFree == True:
		new_window.run_command('toggle_distraction_free')
		new_window.run_command('toggle_menu')

	if winType == 'settings':
		caption = 'Settings'
		leftFile = '${packages}/Default/Preferences.sublime-settings'
		rightFile = '${packages}/User/Preferences.sublime-settings'
		rightContents = '// Settings in here override those in \"Default/Preferences.sublime-settings\",\n// and are overridden in turn by file type specific settings.\n{\n\t$0\n}\n'
	
	if winType == 'keymaps':
		caption = 'Key Bindings'
		leftFile = '${packages}/Default/Default ($platform).sublime-keymap'
		rightFile = '${packages}/User/Default ($platform).sublime-keymap'
		rightContents = '[\n\t$0\n]\n'
	
	if winType == 'mousemaps':
		caption = 'Mouse Bindings'
		leftFile = '${packages}/Default/Default ($platform).sublime-mousemap'
		rightFile = '${packages}/User/Default ($platform).sublime-mousemap'
		rightContents = '[\n\t$0\n]\n'
	
	if winType == 'commands':
		caption = 'Commands'
		leftFile = '${packages}/Default/Default.sublime-commands'
		rightFile = '${packages}/User/Default.sublime-commands'
		rightContents = '[\n\t$0\n]\n'
	
	new_window.run_command('open_file',{'file': leftFile,'caption':caption})
	new_window.run_command('open_file',{'file': rightFile,'caption':caption,'contents':rightContents})
	new_window.set_view_index(new_window.active_view(),1,0)

class sideBySideSettingsCommand(plugin.WindowCommand):
	def run(self):
		openWindow(self.window,'settings',Settings('display_as_rows',False),Settings('open_in_distraction_free',False))
class sideBySideKeyMapsCommand(plugin.WindowCommand):
	def run(self):
		openWindow(self.window,'keymaps',Settings('display_as_rows',False),Settings('open_in_distraction_free',False))
class sideBySideMouseMapsCommand(plugin.WindowCommand):
	def run(self):
		openWindow(self.window,'mousemaps',Settings('display_as_rows',False),Settings('open_in_distraction_free',False))
class sideBySideCommandsCommand(plugin.WindowCommand):
	def run(self):
		openWindow(self.window,'commands',Settings('display_as_rows',False),Settings('open_in_distraction_free',False))
