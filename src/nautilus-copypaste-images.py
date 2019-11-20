#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of nautilus-copypaste-images
#
# Copyright (C) 2016 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import datetime
import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Nautilus', '3.0')
except Exception as e:
    print(e)
    exit(-1)

import os
from urllib import unquote_plus
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Nautilus as FileManager
from gi.repository import Gdk
from gi.repository import GdkPixbuf

APPNAME = 'nautilus-copypaste-images'
ICON = 'nautilus-copypaste-images'
VERSION = '0.2.0-0extras16.04.1'


def get_files(files_in):
    files = []
    for file_in in files_in:
        file_in = unquote_plus(file_in.get_uri()[7:])
        if os.path.isfile(file_in):
            files.append(file_in)
    return files


class CopyPasteImagesMenuProvider(GObject.GObject, FileManager.MenuProvider):
    """Implements the 'Replace in Filenames' extension to the FileManager
    right-click menu"""

    def __init__(self):
        """FileManager crashes if a plugin doesn't implement the __init__
        method"""
        atom = Gdk.atom_intern('CLIPBOARD', True)
        self.clipboard = Gtk.Clipboard.get(atom)
        super(CopyPasteImagesMenuProvider, self).__init__()

    def get_background_items(self, window, folder):
        paste_item = FileManager.MenuItem(name='CopyPasteImagesMenuProvider::Gtk-cpim-paste-image',
                                          label='Вставить как изображение')
        location = folder.get_location()
        paste_item.connect('activate', self.paste_image, location.get_path())
        return paste_item,

    def get_file_items(self, window, items):
        files = get_files(items)
        copy_item = FileManager.MenuItem(name='CopyPasteImagesMenuProvider::Gtk-cpim-copy-image',
                                         label='Копировать как изображение', sensitive=False)
        if len(files) > 0:
            chosen_file = files[0]
            info, _, _ = GdkPixbuf.Pixbuf.get_file_info(chosen_file)
            if info is not None:
                copy_item.set_property('sensitive', True)
                copy_item.connect('activate', self.copy_image, chosen_file)
        return copy_item,

    def paste_image(self, menu, dirname):
        pixbuf = self.clipboard.wait_for_image()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        filename = os.path.join(dirname, 'from_clipboard_{0}.png'.format(current_time))
        if pixbuf is not None:
            pixbuf.savev(filename, 'png', (), ())

    def copy_image(self, menu, file):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(file)
        if pixbuf:
            self.clipboard.set_image(pixbuf)
            self.clipboard.store()

    def about(self, widget, window):
        ad = Gtk.AboutDialog(parent=window)
        ad.set_name(APPNAME)
        ad.set_version(VERSION)
        ad.set_copyright('Copyrignt (c) 2016\nLorenzo Carbonell')
        ad.set_comments(APPNAME)
        ad.set_license('''
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
''')
        ad.set_website('http://www.atareao.es')
        ad.set_website_label('http://www.atareao.es')
        ad.set_authors([
            'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_documenters([
            'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_icon_name(ICON)
        ad.set_logo_icon_name(APPNAME)
        ad.run()
        ad.destroy()


if __name__ == '__main__':
    '''
    atom = Gdk.atom_intern('CLIPBOARD', True)
    clipboard = Gtk.Clipboard.get(atom)
    print(clipboard.wait_is_image_available())
    afile = '/home/lorenzo/Escritorio/ejemplo/5647177212_30a527c038_b.jpg'
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(afile)
    # atom = Gdk.atom_intern('CLIPBOARD', True)
    # clipboard = Gtk.Clipboard.get(atom)
    clipboard.set_image(pixbuf)
    clipboard.store()
    print(clipboard.wait_is_image_available())
    '''
