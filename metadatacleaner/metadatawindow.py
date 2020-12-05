"""Window detailing the file's metadata."""

from gi.repository import Gtk
from typing import Dict

from metadatacleaner.file import File
from metadatacleaner.metadatadetails import MetadataDetails


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/MetadataWindow.ui"
)
class MetadataWindow(Gtk.Window):
    """Window detailing the file's metadata."""

    __gtype_name__ = "MetadataWindow"

    _box: Gtk.Box = Gtk.Template.Child()

    def __init__(self, f: File, *args, **kwargs) -> None:
        """Window initialization.

        Args:
            f (File): The file the popover will give details about.
        """
        super().__init__(*args, **kwargs)
        self._file = f
        self._setup_metadata_details()

    def _setup_metadata_details(self) -> None:
        if not self._file.metadata:
            return
        if isinstance(self._file.metadata[list(self._file.metadata)[0]], Dict):
            for filename, metadata in self._file.metadata.items():
                self._box.add(MetadataDetails(
                    filename=f"{self._file.filename}/{filename}",
                    metadata=metadata
                ))
        else:
            self._box.add(MetadataDetails(
                filename=self._file.filename,
                metadata=self._file.metadata
            ))
