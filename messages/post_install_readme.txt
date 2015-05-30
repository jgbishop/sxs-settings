Thanks for installing the Side-by-Side Settings plug-in for Sublime Text! This
plug-in adds three new commands to the command palette (only two are added in
Sublime Text 2):

  1. Side-by-Side: Select a File (Ctrl+K, Ctrl+S)
     Note that this command is only available in Sublime Text 3. Opens a panel
     displaying all of the .sublime-settings and .sublime-keymap files in the
     Sublime Text environment. For more on how to use this command, see the
     corresponding section below.

  2. Side-by-Side: Sublime Settings
     Opens both default and user Sublime Text settings side by side in a new
     window

  3. Side-by-Side: Sublime Key Bindings
     Opens both default and user Sublime Text key bindings side by side in a new
     window

================================================================================
Using the Select a File Command (Sublime Text 3 Only)
================================================================================
The "select a file" command opens a quick panel that displays all of the 
.sublime-settings and .sublime-keymap files that Sublime Text knows about
(note that files located in the Packages/User directory are filtered out of
this list; more on why it does this in a second). When a file in the quick panel
is selected, it becomes the "left" (or "top", depending on your settings) panel
in the comparison window. The "right" (or "bottom") panel will contain the
corresponding user settings file, typically located in the Packages/User
directory (hence why files in Packages/User are filtered out of the list).

Side-by-Side Settings tries to do the correct thing depending on the file you
select in the quick panel. If the file you select is a platform-specific
settings file (e.g. Default/Preferences (Windows).sublime-settings), the
corresponding user file that gets opened will be Preferences.sublime-settings
(in the Packages/User directory). This is due to the fact that platform-
specific files in the User directory are ignored by Sublime Text. Likewise, if
you select a .sublime-keymap file, the appropriate platform-specific
.sublime-keymap file in the User directory will be opened.

Note that this command is bound to the Ctrl+K, Ctrl+S key chord by default, and
is only available for users of Sublime Text 3.

================================================================================
Easily Closing a Side-by-Side Window
================================================================================
To close the window that opens up when a Side-by-Side Settings command is
issued, simply issue the same command a second time. The window that opened up
will be closed for you! This is a particularly helpful feature when a command is
bound to a keyboard shortcut.

================================================================================
Customizing the Key Binding
================================================================================
By default, the key-chord Ctrl+K, Ctrl+S is bound to the "select a file"
command. If you wish to bind any of the commands to a different key, here are
the internal command names to use:

* sxs_select_file
* sxs_settings
* sxs_key_bindings

Here's an example key binding:

{ "keys": ["ctrl+k", "ctrl+p"], "command": "sxs_settings" }

================================================================================
Plug-in Settings
================================================================================
Side-by-Side Settings currently supports the following plug-in specific 
settings:

  display_using_rows
  This option specifies whether or not to arrange the side-by-side views
  vertically instead of horizontally. The default value for this option is
  false.

  open_in_distraction_free
  This option allows the side-by-side window to open in distraction free mode,
  essentially resulting in a full-screen window. This option defaults to false.

================================================================================
Reporting Bugs & Suggesting Features
================================================================================
If you spot a bug in this plug-in, or you have a feature request, please open an
issue over on the project issues page at GitHub:

https://github.com/jgbishop/sxs-settings/issues
