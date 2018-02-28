import re
import sublime
import sublime_plugin

_WINDOW_ID = None


def close_window_if_needed(self):
    global _WINDOW_ID

    if _WINDOW_ID is not None:
        for i, w in enumerate(sublime.windows()):
            if w.id() == _WINDOW_ID:
                w.run_command("close_window")
                _WINDOW_ID = None
                return True
    return False


def get_setting(pref, default):
    return sublime.load_settings('sxs_settings.sublime-settings').get(pref, default)


def open_window(self, left_path):
    global _WINDOW_ID

    # Self in this context is the active window
    self.run_command("new_window")
    new_window = sublime.active_window()
    _WINDOW_ID = new_window.id()

    if get_setting('display_using_rows', False):
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

    if get_setting('hide_minimap', False):
        new_window.set_minimap_visible(False)

    if get_setting('open_in_distraction_free', False):
        new_window.run_command('toggle_distraction_free')
        new_window.run_command('toggle_tabs')

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

    new_window.run_command("open_file", {'file': "${packages}/" + left_path})
    new_window.run_command(
        "open_file", {
            'file': "${packages}/User/" + right_path,
            'contents': right_contents
        }
    )
    new_window.set_view_index(new_window.active_view(), 1, 0)


class SxsSettingsCommand(sublime_plugin.WindowCommand):
    def run(self):
        if close_window_if_needed(self):
            return
        open_window(self.window, "Default/Preferences.sublime-settings")


class SxsKeyBindingsCommand(sublime_plugin.WindowCommand):
    def run(self):
        if close_window_if_needed(self):
            return
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
        if close_window_if_needed(self):
            return

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
