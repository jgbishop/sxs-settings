
import re
import sublime
import sublime_plugin


def plugin_loaded():
    global g_settings

    g_settings = sublime.load_settings('sxs_settings.sublime-settings')
    g_settings.clear_on_change('sxs_settings')

    update_settings()
    g_settings.add_on_change('sxs_settings', update_settings)


def update_settings():
    global g_hide_minimap
    global g_open_in_distraction_free

    g_hide_minimap = g_settings.get('hide_minimap', False)
    g_open_in_distraction_free = g_settings.get('open_in_distraction_free', False)


def plugin_unloaded():
    g_settings.clear_on_change('sxs_settings')


def open_window(self, left_path):
    last_slash = left_path.rfind("/")
    right_path = left_path[(last_slash+1):] # Extract the filename

    # If we're opening a .sublime-keymap file, the right pane should always open
    # to "Default ({platform}).sublime-keymap" since that's where keys should be
    # put.
    if re.search(r"\.sublime-keymap", left_path):
        platform = sublime.platform()

        if platform == "linux":
            platform = "Linux"

        elif platform == "osx":
            platform = "OSX"

        else:
            platform = "Windows"

        right_path = "Default (" + platform + ").sublime-keymap"

    # Test to see if we are opening a platform-specific settings file. If so,
    # strip the platform specific portion of the filename (platform-specific
    # files are ignored in the User directory)
    elif re.search(r" \((?:Linux|OSX|Windows)\).sublime-settings", left_path):
        right_path = re.sub(r" \((?:Linux|OSX|Windows)\)", "", right_path)

    # Default to object notation for sublime-settings files
    right_contents = "{\n\t$0\n}\n"

    if re.search(r"\.sublime-keymap", left_path):
        # Use array notation for sublime-keymap files
        right_contents = "[\n\t$0\n]\n"

    active_window = sublime.active_window()
    active_window.run_command("edit_settings", {'base_file': "${packages}/" + left_path, "default": right_contents})

    new_window = sublime.active_window()

    if g_hide_minimap:
        new_window.set_minimap_visible(False)

    if g_open_in_distraction_free:
        new_window.run_command('toggle_distraction_free')
        new_window.run_command('toggle_tabs')


class SxsSelectFileCommand(sublime_plugin.WindowCommand):

    def __init__(self, window):
        super(SxsSelectFileCommand, self).__init__(window)

        self.file_list = []
        self.last_index = -1

    def run(self):
        # Clear our cache
        del self.file_list[:]

        settings_list = sublime.find_resources("*.sublime-settings")
        keymap_list = sublime.find_resources("*.sublime-keymap")

        temp_list = settings_list + keymap_list

        for i, item in enumerate(temp_list):
            temp_item = re.sub(r"^Packages/", "", item)

            # Ignore anything we find in the User directory
            # (those will get treated as "right pane" files)
            if re.match(r"User/", temp_item):
                continue

            else:
                self.file_list.append(temp_item)

        self.file_list.sort()
        self.window.show_quick_panel(self.file_list, self.on_done, 0, self.last_index)

    def on_done(self, index):

        if index == -1:
            return

        self.last_index = index
        open_window(self.window, self.file_list[index])

