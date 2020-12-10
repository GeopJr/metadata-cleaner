# SPDX-FileCopyrightText: 2020 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""About dialog giving informations about the application."""

from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/AboutDialog.ui"
)
class AboutDialog(Gtk.AboutDialog):
    """About dialog."""

    __gtype_name__ = "AboutDialog"

    def __init__(self, *args, **kwargs) -> None:
        """About dialog initialization."""
        super().__init__(*args, **kwargs)
