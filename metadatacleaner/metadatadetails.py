"""List of a file's metadata."""

from gettext import gettext as _
from gi.repository import Gtk
from typing import Dict

from metadatacleaner.file import File


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/MetadataDetails.ui"
)
class MetadataDetails(Gtk.Box):
    """List of a file's metadata."""

    __gtype_name__ = "MetadataDetails"

    _label: Gtk.Label = Gtk.Template.Child()
    _grid: Gtk.Grid = Gtk.Template.Child()

    def __init__(self, filename: str, metadata: Dict, *args, **kwargs) -> None:
        """Widget initialization.

        Args:
            filename (str): The file name.
            metadata (Dict): The metadata to display.
        """
        super().__init__(*args, **kwargs)
        self._filename = filename
        self._metadata = metadata
        self._setup_label()
        self._setup_metadata_grid()

    def _setup_label(self) -> None:
        self._label.set_label(
            _("{filename}:").format(filename = self._filename)
        )

    def _setup_metadata_grid(self) -> None:
        for row, (key, value) in enumerate(self._metadata.items()):
            key_label = Gtk.Label(
                visible=True,
                label=key,
                # style_class="dim-label",
                halign="end",
                valign="start",
                justify="left",
                wrap=True
            )
            key_label.get_style_context().add_class("dim-label")
            value_label = Gtk.Label(
                visible=True,
                label=value,
                halign="start",
                valign="start",
                justify="left",
                selectable=True,
                wrap=True
            )
            self._grid.attach(key_label, 0, row, 1, 1)
            self._grid.attach(value_label, 1, row, 1, 1)
