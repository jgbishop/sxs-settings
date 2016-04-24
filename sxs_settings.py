import sublime
import sublime_plugin
import re

_WINDOW_ID = None

def closeWindowIfNeeded(self):
    global _WINDOW_ID

    if get_setting('display_using_panes', True):
        if sxsLayoutManager.is_pane_maxed(self.window):
            do_restore(self)
            return True
    else:
        if _WINDOW_ID is not None:
            for i,w in enumerate(sublime.windows()):
                if w.id() == _WINDOW_ID:
                    w.run_command("close_window")
                    _WINDOW_ID = None
                    return True
    return False

def get_setting(pref, default):
    return (sublime.load_settings('sxs_settings.sublime-settings')
            .get(pref, default))

def maximizePane(self):
    w = self.window
    if sxsLayoutManager.is_pane_maxed(w):
        do_restore(self)
    elif w.num_groups() > 1:
        do_maximize(self)

def do_maximize(self):
    win = self.window
    group = win.active_group()
    layout = win.get_layout()
    sxsLayoutManager.save_layout(win)

    current_col = int(layout['cells'][group][2])
    current_row = int(layout['cells'][group][3])
    new_rows = []
    new_cols = []

    for index, row in enumerate(layout['rows']):
        new_rows.append(0.0 if index < current_row else 1.0)

    for index, col in enumerate(layout['cols']):
        new_cols.append(0.0 if index < current_col else 1.0)

    layout['rows'] = new_rows
    layout['cols'] = new_cols

    for view in win.views():
        view.set_status('0_maxpane', 'MAX')
    win.set_layout(layout)

def do_restore(self):
    win = self.window
    if sxsLayoutManager.has_layout(win):
        win.set_layout(sxsLayoutManager.pop_layout(win))
    elif sxsLayoutManager.looks_maxed(win):
        layout = win.get_layout()
        row_length = len(layout['rows'])
        r = range(0,1)
        layout['rows'] = [n / float(row_length - 1) for n in r]

        col_length = len(layout['cols'])
        r = range(0,1)
        layout['cols'] = [n / float(col_length - 1) for n in r]

        win.set_layout(layout)

    for view in win.views():
        view.erase_status('0_maxpane')

def open_window(self, left_path):
    global _WINDOW_ID

    # Note that self in this context is the active window
    the_window = self.window
    if get_setting('display_using_panes', True):
        maximizePane(self)
    else:
        self.window.run_command("new_window")
        the_window = sublime.active_window()
        _WINDOW_ID = the_window.id()

    if get_setting('display_using_rows', False):
        the_window.set_layout({
            "cols": [0, 1],
            "rows": [0, 0.5, 1],
            "cells": [[0, 0, 1, 1], [0, 1, 1, 2]]
        })
    else:
        the_window.set_layout({
            "cols": [0, 0.5, 1],
            "rows": [0, 1],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
        })

    if get_setting('open_in_distraction_free', False):
        the_window.run_command('toggle_distraction_free')
        the_window.run_command('toggle_tabs')

    last_slash = left_path.rfind("/")
    right_path = left_path[(last_slash + 1):] # Extract the filename

    # If we're opening a .sublime-keymap file, the right pane should always open
    # to "Default ({platform}).sublime-keymap" since that's where keys should be
    # put.
    if re.search(r"\.sublime-keymap", left_path):
        platform = "Windows" # Assume this to start (evil, I know)
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

    rightContents = "{\n\t$0\n}\n" # Default to object notation for sublime-settings files
    if re.search(r"\.sublime-keymap", left_path):
        rightContents = "[\n\t$0\n]\n"; # Use array notation for sublime-keymap files

    the_window.run_command("open_file", {
                                'file': "${packages}/" + left_path
                            })
    the_window.run_command("open_file", {
                                'file': "${packages}/User/" + right_path,
                                'contents': rightContents
                            })
    the_window.set_view_index(the_window.active_view(), 1, 0)

class sxsLayoutManager:
    previous = {}
    maxed = {}

    @staticmethod
    def is_pane_maxed(window):
        if sxsLayoutManager.has_layout(window):
            return True
        elif sxsLayoutManager.looks_maxed(window):
            return True
        return False

    @staticmethod
    def looks_maxed(window):
        layout = window.get_layout()
        cols = layout['cols']
        rows = layout['rows']
        if window.num_groups() > 1:
            if set(cols + rows) == set([0.0, 1.0]):
                return True
        return False

    @staticmethod
    def save_layout(window):
        wid = window.id()
        sxsLayoutManager.previous[wid] = window.get_layout()
        sxsLayoutManager.maxed[wid] = window.active_group()

    @staticmethod
    def maxed_group(window):
        wid = window.id()
        if wid in sxsLayoutManager.maxed:
            return sxsLayoutManager.maxed[wid]
        else:
            return None

    @staticmethod
    def pop_layout(window):
        wid = window.id()
        layout = sxsLayoutManager.previous[wid]
        del sxsLayoutManager.previous[wid]
        del sxsLayoutManager.maxed[wid]
        return layout

    @staticmethod
    def has_layout(window):
        return window.id() in sxsLayoutManager.previous

class sxsSettingsCommand(sublime_plugin.WindowCommand):
    """
    Handler for the Sublime settings side-by-side command."
    """
    def run(self):
        if closeWindowIfNeeded(self):
            return
        open_window(self, "Default/Preferences.sublime-settings")

class sxsKeyBindingsCommand(sublime_plugin.WindowCommand):
    """
    Handler for the Sublime key bindings side-by-side command.
    """
    def run(self):
        if closeWindowIfNeeded(self):
            return
        open_window(self, "Default/Default ($platform).sublime-keymap")

class sxsTestCommand(sublime_plugin.WindowCommand):
    def run(self):
        maximizePane(self)

class sxsSelectFileCommand(sublime_plugin.WindowCommand):
    """
    Handler for the "select a file" side-by-side command.
    """
    fileList = []

    def run(self):
        # sxsLayoutManager.getLayout(self.window)

        if closeWindowIfNeeded(self):
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
        open_window(self, self.fileList[index])
