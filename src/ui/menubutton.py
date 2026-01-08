# SPDX-FileCopyrightText: Metadata Cleaner contributors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Menu button."""

from gi.repository import Gtk


@Gtk.Template(
    resource_path="/dev/geopjr/MetadataCleaner/ui/MenuButton.ui"
)
class MenuButton(Gtk.MenuButton):
    """Menu button."""

    __gtype_name__ = "MenuButton"
