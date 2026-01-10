# SPDX-FileCopyrightText: Metadata Cleaner contributors
# SPDX-License-Identifier: GPL-3.0-or-later

"""View details of a file."""

from gettext import gettext as _
from gi.repository import Adw, GLib, Gtk
from typing import Optional

from metadatacleaner.modules.file import File, FileState

from metadatacleaner.ui.metadataview import MetadataView


@Gtk.Template(resource_path="/dev/geopjr/MetadataCleaner/ui/DetailsView.ui")
class DetailsView(Adw.Bin):
    """View details of a file."""

    __gtype_name__ = "DetailsView"

    def view_file(self, f: File) -> None:
        """Set the file to view.

        Args:
            f (File): The file to view.
        """
        self.set_child(None)
        if f.state == FileState.HAS_METADATA:
            self._setup_metadata_details(f)
        elif f.state == FileState.CLEANED:
            self._setup_cleaned_details()
        elif f.state in [
            FileState.ERROR_WHILE_CHECKING_METADATA,
            FileState.ERROR_WHILE_INITIALIZING,
            FileState.ERROR_WHILE_REMOVING_METADATA,
            FileState.HAS_NO_METADATA,
            FileState.UNSUPPORTED,
        ]:
            self._setup_error_details(f)

    def set_content(self, w) -> None:
        """Set the widget's child."""
        self.set_child(w)

    def _setup_cleaned_details(self) -> None:
        self.set_content(
            Adw.StatusPage(
                title=_("The File Has Been Cleaned"),
                description=_(
                    "Known metadata have been removed, however the cleaning "
                    "process has some limitations."
                ),
                child=Gtk.Button(
                    label=_("Learn more"),
                    action_name="win.info",
                    halign=Gtk.Align.CENTER,
                    css_classes=["pill", "suggested-action"],
                ),
                css_classes=["compact"],
            )
        )

    def _setup_metadata_details(self, f: File) -> None:
        self.set_content(MetadataView(metadata=f.metadata))

    def _setup_error_details(self, f: File) -> None:
        info_titles = {
            FileState.ERROR_WHILE_INITIALIZING: _("Unable to Read the File"),
            FileState.UNSUPPORTED: _("File Type not Supported"),
            FileState.ERROR_WHILE_CHECKING_METADATA: _("Unable to Check for Metadata"),
            FileState.HAS_NO_METADATA: _("No Known Metadata"),
            FileState.ERROR_WHILE_REMOVING_METADATA: _("Unable to Remove Metadata"),
        }
        info_details = str(f.error or "")
        if f.state == FileState.HAS_NO_METADATA:
            info_details = _("The file will be cleaned anyway to be sure.")
        self.set_content(
            Adw.StatusPage(
                title=info_titles[f.state],
                description=info_details,
                css_classes=["compact"],
            )
        )
