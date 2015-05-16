# Side-by-Side Settings

A Sublime Text plugin for viewing both default and user settings side by side in
a new window. Also works for viewing default and user key bindings. Support for
additional settings (namely for installed plugins) is planned, but not currently
implemented.

## Installation
There are two options for installing this package:

#### [Package Control](https://sublime.wbond.net/) (Recommended)
Side-by-Side Settings is available on Package Control. If you do not have the
Package Control plug-in installed in Sublime Text, you should (it's super cool)!
Simply follow [these instructions](https://sublime.wbond.net/installation) to
install it. Once it has been installed, search for and select  **Side-by-Side
Settings** in the `Install Package` command window.

#### Git Clone
You can also clone this repository into your Sublime Text Packages directory
using Git, if you feel so inclined.

## Usage

Side-by-Side Settings currently adds two commands to the command palette:

* **Side-by-Side Settings** - Opens both default and user Sublime Text settings side by side in a new window
* **Side-by-Side Key Bindings** - Opens both default and user Sublime Text key bindings side by side in a new window

If you want to bind these commands to a shortcut key, the internal command names
to use in the binding are:

* sxs_settings
* sxs_key_bindings

Here's an example key binding:

`{ "keys": ["ctrl+k", "ctrl+p"], "command": "sxs_settings" }`

## Future Development
At the moment, this plugin is pretty bare-bones. I have a number of items I'd
like to implement, each of which are listed on the GitHub issues list for this
project. Pull requests are welcome! Though I'm a fairly seasoned programmer, I'm
new to Python development, so if you see room for improvement, let me know.

## Acknowledgements
Thanks to Jeremy Bolding for providing several plug-in suggestions.
