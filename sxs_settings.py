import re
import sublime
import sublime_plugin


def get_setting(pref, default):
    return sublime.load_settings('sxs_settings.sublime-settings').get(pref, default)


def open_window(self, left_path):
    last_slash = left_path.rfind("/")
    right_path = left_path[(last_slash + 1):]  # Extract the filename

    # If we're opening a .sublime-keymap file, the right pane should always open
    # to "Default ({platform}).sublime-keymap" since that's where keys should be
    # put.
    if re.search(r"\.sublime-keymap", left_path):
        platform = "Windows"  # Assume this to start (evil, I know)
        plat = sublime.platform()
        if plat == "linux":
            platform = "Linux"
        elif plat == "osx":
            platform = "OSX"

        right_path = "Default (" + platform + ").sublime-keymap"

    # Test to see if we are opening a platform-specific settings file. If so,
    # strip the platform specific portion of the filename (platform-specific
    # files are ignored in the User directory)
    elif re.search(r" \((?:Linux|OSX|Windows)\).sublime-settings", left_path):
        right_path = re.sub(r" \((?:Linux|OSX|Windows)\)", "", right_path)

    right_contents = "{\n\t$0\n}\n"  # Default to object notation for sublime-settings files
    if re.search(r"\.sublime-keymap", left_path):
        right_contents = "[\n\t$0\n]\n"  # Use array notation for sublime-keymap files

    sublime.active_window().run_command(
        "edit_settings", {"base_file": "${packages}/" + left_path, "default": right_contents}
    )
    active_window = sublime.active_window()

    if get_setting('hide_minimap', False):
        active_window.set_minimap_visible(False)

    if get_setting('open_in_distraction_free', False):
        active_window.run_command('toggle_distraction_free')
        active_window.run_command('toggle_tabs')


class SxsSettingsCommand(sublime_plugin.WindowCommand):
    def run(self):
        open_window(self.window, "Default/Preferences.sublime-settings")


class SxsKeyBindingsCommand(sublime_plugin.WindowCommand):
    def run(self):
        open_window(self.window, "Default/Default ($platform).sublime-keymap")


class SxsSelectFileCommand(sublime_plugin.WindowCommand):
    file_list = []
    last_index = -1
    platform_filter = {
        'linux': ('OSX', 'Windows'),
        'osx': ('Linux', 'Windows'),
        'windows': ('Linux', 'OSX'),
    }

    def run(self):
        self.file_list[:] = []  # Clear our cache

        platforms_to_filter = self.__class__.platform_filter.get(sublime.platform())
        do_filter = get_setting("filter_platform", True)

        settings_list = sublime.find_resources("*.sublime-settings")
        keymap_list = sublime.find_resources("*.sublime-keymap")

        templist = settings_list + keymap_list

        for i, item in enumerate(templist):
            temp_item = re.sub(r"^Packages/", "", item)
            if re.match(r"User/", temp_item):
                # Ignore anything we find in the User directory
                # (those will get treated as "right pane" files)
                continue
            else:
                # Skip the necessary platforms if we're filtering on platform
                if do_filter:
                    skip = False
                    for p in platforms_to_filter:
                        if(p in str(temp_item)):
                            skip = True
                            break

                    if skip:
                        continue

                self.file_list.append(temp_item)

        self.file_list.sort()
        self.window.show_quick_panel(self.file_list, self.on_done, 0, self.last_index)

    def on_done(self, index):
        self.last_index = index
        if index == -1:
            return
        open_window(self.window, self.file_list[index])
