# -*- coding: utf-8 -*-


#   Edited by Wei-Chih, Huang <noctildon2@gmail.com> 2018
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.


def setup(commands, name='Caja PyExtension', label='customized extension', tip='', icon='terminal'):
    from gi.repository import Caja, GObject, Gtk, GdkPixbuf
    import urllib
    import os
    import subprocess
    import locale
    import gettext

    APP_NAME = "caja-pyextensions"
    LOCALE_PATH = "/usr/share/locale/"
    ICONPATH = "/usr/share/icons/gnome/48x48/apps/terminal.png"
    # internationalization
    locale.setlocale(locale.LC_ALL, '')
    gettext.bindtextdomain(APP_NAME, LOCALE_PATH)
    gettext.textdomain(APP_NAME)
    _ = gettext.gettext
    # post internationalization code starts here

    class OpenTerminalHere(GObject.GObject, Caja.MenuProvider):
        def __init__(self):
            """Caja crashes if a plugin doesn't implement the __init__ method"""
            try:
                factory = Gtk.IconFactory()
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(ICONPATH)
                iconset = Gtk.IconSet.new_from_pixbuf(pixbuf)
                factory.add("terminal", iconset)
                factory.add_default()
            except:
                pass

        def run(self, menu, selected):
            """Runs the customized commands on the given Directory"""
            uri_raw = selected.get_uri()
            if len(uri_raw) < 7:
                return
            curr_dir = urllib.unquote(uri_raw[7:])
            if os.path.isfile(curr_dir):
                curr_dir = os.path.dirname(curr_dir)

            to_be_exec = "global bash_string;" + "bash_string=" + str(commands)
            exec(to_be_exec)

            subprocess.call(bash_string, shell=True)

        def get_file_items(self, window, sel_items):
            if len(sel_items) != 1 or sel_items[0].get_uri_scheme() != 'file':
                return
            item = Caja.MenuItem(name=name,
                                 label=_(label),
                                 tip=_(tip),
                                 icon=icon)
            item.connect('activate', self.run, sel_items[0])
            return [item]

        def get_background_items(self, window, current_directory):
            item = Caja.MenuItem(name=name,
                                 label=_(label),
                                 tip=_(tip),
                                 icon=icon)
            item.connect('activate', self.run, current_directory)
            return [item]


# test function : open terminal in the current folder in caja
# you can change the line below with any legal python commands in string type
mystr = '"cd \"" + curr_dir + "\" && x-terminal-emulator &"'
setup(mystr)
