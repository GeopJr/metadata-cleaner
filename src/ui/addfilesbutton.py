# SPDX-FileCopyrightText: Metadata Cleaner contributors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Button allowing to add files."""

from gi.repository import Adw, Gtk, GObject

@Gtk.Template(
    resource_path="/dev/geopjr/MetadataCleaner/ui/AddFilesButton.ui"
)
class AddFilesButton(Adw.Bin):
    """Button allowing to add files."""

    __gtype_name__ = "AddFilesButton"
    _stack: Gtk.Stack = Gtk.Template.Child()

    @GObject.Property(type=bool, default=True)
    def collapsed(self):
        return self._stack.get_visible_child_name() != "expanded"

    @collapsed.setter
    def collapsed(self, value):
        self._stack.set_visible_child_name("narrow" if value else "expanded")

