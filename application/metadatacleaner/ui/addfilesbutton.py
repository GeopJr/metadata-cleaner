# SPDX-FileCopyrightText: 2020 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Button allowing to add files."""

from gi.repository import Adw, Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/AddFilesButton.ui"
)
class AddFilesButton(Adw.SplitButton):
    """Button allowing to add files."""

    __gtype_name__ = "AddFilesButton"

    def __init__(self, *args, **kwargs) -> None:
        """Button initialization."""
        super().__init__(*args, **kwargs)

    @Gtk.Template.Callback()
    def _on_add_folders_button_clicked(self, button: Gtk.Button) -> None:
        self.popdown()
