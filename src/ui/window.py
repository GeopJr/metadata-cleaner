# SPDX-FileCopyrightText: Metadata Cleaner contributors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Application window of Metadata Cleaner."""

from gettext import gettext as _
from gi.repository import Adw, Gdk, Gio, GLib, GObject, Gtk, Pango
from typing import Any

from metadatacleaner.modules.filestore import FileStore, FileStoreState
from metadatacleaner.modules.pride import get_celebration

from metadatacleaner.ui.dropoverlay import DropOverlay
from metadatacleaner.ui.filechooserdialog import FileChooserDialog
from metadatacleaner.ui.filesview import FilesView
from metadatacleaner.ui.folderchooserdialog import FolderChooserDialog
from metadatacleaner.ui.menubutton import MenuButton
from metadatacleaner.ui.detailsview import DetailsView
from metadatacleaner.ui.cleaningwarningdialog import CleaningWarningDialog


@Gtk.Template(resource_path="/dev/geopjr/MetadataCleaner/ui/Window.ui")
class Window(Adw.ApplicationWindow):
    """Application window of Metadata Cleaner."""

    __gtype_name__ = "Window"

    file_store = GObject.Property(type=FileStore, nick="file-store")

    _split_view: Adw.OverlaySplitView = Gtk.Template.Child()
    _view_stack: Gtk.Stack = Gtk.Template.Child()
    _details_view: DetailsView = Gtk.Template.Child()

    _file_chooser_dialog: Gtk.FileDialog = Gtk.Template.Child()
    _cleaning_warning_dialog: CleaningWarningDialog = Gtk.Template.Child()
    _header: Adw.HeaderBar = Gtk.Template.Child()
    _add_files_button: Gtk.MenuButton = Gtk.Template.Child()
    _drop_overlay: DropOverlay = Gtk.Template.Child()
    _toast_overlay: Adw.ToastOverlay = Gtk.Template.Child()

    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        """Window initialization."""
        app = kwargs["application"]
        super().__init__(
            title=app.name,
            *args,
            **kwargs
        )
        self._setup_size()
        self._setup_devel_style()
        self._setup_file_store()
        self._setup_drop_target()
        self._setup_actions()

    # SETUP #

    def _setup_size(self) -> None:
        def on_close_request(window: Gtk.Window) -> None:
            width, height = self.get_default_size()
            maximized = self.is_maximized()
            self.get_application().settings.set_uint("window-width", width)
            self.get_application().settings.set_uint("window-height", height)
            self.get_application().settings.set_boolean(
                "window-maximized", maximized)
        self.set_default_size(
            self.get_application().settings.get_uint("window-width"),
            self.get_application().settings.get_uint("window-height"))
        if self.get_application().settings.get_boolean("window-maximized"):
            self.maximize()
        self.connect("close-request", on_close_request)

    def _setup_devel_style(self) -> None:
        if self.get_application().devel:
            self.add_css_class("devel")

    def _setup_file_store(self) -> None:

        def on_items_changed(
                file_store: FileStore,
                position: int,
                added: int,
                removed: int) -> None:
            if len(file_store) == 0:
                self.lookup_action("clean-metadata").set_enabled(False)
                self.close_details_view()
                self.show_empty_view()
            else:
                self.show_files_view()

        def on_state_changed(
                file_store: FileStore,
                file_index: int) -> None:
            self.lookup_action("clean-metadata").set_enabled(not (
                file_store.state == FileStoreState.WORKING
                or len(file_store.get_cleanable_files()) == 0))

        self.file_store = FileStore()
        self.file_store.connect("items-changed", on_items_changed)
        self.file_store.connect("file-state-changed", on_state_changed)
        self.file_store.connect("state-changed", on_state_changed)
        self.get_application().settings.bind(
            "lightweight-cleaning",
            self.file_store,
            "lightweight-mode",
            Gio.SettingsBindFlags.DEFAULT)

    def _setup_drop_target(self) -> None:

        def on_drop(
                widget: Gtk.DropTarget,
                value: Any,
                x: int,
                y: int):
            self._drop_overlay.dropping = False
            if isinstance(value, Gdk.FileList):
                self.file_store.add_gfiles(value.get_files())

        def on_leave(widget: Gtk.DropTarget):
            self._drop_overlay.dropping = False

        def on_enter(widget: Gtk.DropTarget, x: int, y: int):
            self._drop_overlay.dropping = True
            return Gdk.DragAction.COPY

        drop_target = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)
        drop_target.connect("drop", on_drop)
        drop_target.connect("enter", on_enter)
        drop_target.connect("leave", on_leave)
        self.add_controller(drop_target)

    def _present_about(self) -> None:
        about = Adw.AboutDialog.new()
        about.set_application_icon("dev.geopjr.MetadataCleaner")
        about.set_application_name(self.get_application().name)
        about.set_version(self.get_application().version)
        about.set_license_type(Gtk.License.GPL_3_0_ONLY)
        about.set_developer_name("Evangelos \"GeopJr\" Paterakis")
        # TODO set website, issue_url etc

        about.set_artists(
            [
                "Romain Vigier https://www.romainvigier.fr",
                "GNOME Design Team https://gitlab.gnome.org/Teams/Design"
            ]
        )
        about.set_developers(
            [
                "Evangelos \"GeopJr\" Paterakis https://geopjr.dev/",
                "Romain Vigier https://www.romainvigier.fr/",
            ]
        )

        # translators: Translate this string as your translator credits.
        # Name only:    Gregor Niehl
        # Name + URL:   Gregor Niehl https://gitlab.gnome.org/gregorni/
        # Name + Email: Gregor Niehl <gregorniehl@web.de>
        # Do not remove existing names.
        # Names are separated with newlines.
        about.set_translator_credits(_("translator-credits"))

        # translators: Application metainfo for the app "Archives". <https://gitlab.gnome.org/GeopJr/Archives/>
        about.add_other_app(
            "dev.geopjr.Archives", _("Archives"), _("Create and view web archives")
        )
        # translators: Application metainfo for the app "Calligraphy". <https://gitlab.gnome.org/GeopJr/Calligraphy>
        about.add_other_app(
            "dev.geopjr.Calligraphy", _("Calligraphy"), _("Turn text into ASCII banners")
        )
        # translators: Application metainfo for the app "Collision". <https://github.com/GeopJr/Collision>
        about.add_other_app(
            "dev.geopjr.Collision", _("Collision"), _("Check hashes for your files")
        )
        # translators: Application metainfo for the app "Turntable". <https://codeberg.org/GeopJr/Turntable>
        about.add_other_app("dev.geopjr.Turntable", _("Turntable"), _("Scrobble your music"))
        # translators: Application metainfo for the app "Tuba". <https://github.com/GeopJr/Tuba>
        about.add_other_app("dev.geopjr.Tuba", _("Tuba"), _("Browse the Fediverse"))

        about.add_legal_section(
            title="mat2",
            copyright="Copyright 2018 Julien (jvoisin) Voisin julien.voisin+mat2@dustri.org\nCopyright 2016 Marie-Rose for mat2's logo",
            license_type=Gtk.License.LGPL_3_0,
        )
        celebrate = get_celebration()
        if celebrate != "":
            about.add_css_class(celebrate)
        about.present(self)

    def _setup_actions(self) -> None:

        def on_close(action: Gio.Action, parameters: None) -> None:
            self.destroy()
        close = Gio.SimpleAction.new("close", None)
        close.connect("activate", on_close)
        self.add_action(close)

        def on_about(action: Gio.Action, parameters: None) -> None:
            self._present_about()
        about = Gio.SimpleAction.new("about", None)
        about.connect("activate", on_about)
        self.add_action(about)

        def on_toast(action: Gio.Action, parameters: GLib.Variant) -> None:
            self._toast_overlay.add_toast(Adw.Toast.new(title=parameters.get_string()))
        toast = Gio.SimpleAction.new("toast", GLib.VariantType.new("s"))
        toast.connect("activate", on_toast)
        self.add_action(toast)

        def on_info(action: Gio.Action, parameters: None) -> None:
            self._on_show_info_dialog()
        info = Gio.SimpleAction.new("info", None)
        info.connect("activate", on_info)
        self.add_action(info)

        def on_add_files(action: Gio.Action, parameters: None) -> None:
            self._file_chooser_dialog.open_multiple(self, None, self._on_file_chooser_dialog_response)
        add_files = Gio.SimpleAction.new("add-files", None)
        add_files.connect("activate", on_add_files)
        self.add_action(add_files)

        def on_add_folders(action: Gio.Action, parameters: None) -> None:
            self._file_chooser_dialog.select_multiple_folders(self, None, self._on_folder_chooser_dialog_response)
        add_folders = Gio.SimpleAction.new("add-folders", None)
        add_folders.connect("activate", on_add_folders)
        self.add_action(add_folders)

        def on_remove_file(
                action: Gio.Action,
                parameters: GLib.Variant) -> None:
            self.file_store.remove_file_with_index(parameters.get_uint32())
        remove_file = Gio.SimpleAction.new(
            "remove-file",
            GLib.VariantType.new("u"))
        remove_file.connect("activate", on_remove_file)
        self.add_action(remove_file)

        def on_clear_files(action: Gio.Action, parameters: None) -> None:
            self.file_store.remove_files()
        clear_files = Gio.SimpleAction.new("clear-files", None)
        clear_files.connect("activate", on_clear_files)
        clear_files.set_enabled(False)
        self.add_action(clear_files)

        def on_view_details(
                action: Gio.Action,
                parameters: GLib.Variant) -> None:
            f = self.file_store.get_file_with_index(parameters.get_uint32())
            self._details_view.view_file(f)
            self.open_details_view()
        view_details = Gio.SimpleAction.new(
            "view-details",
            GLib.VariantType.new("u"))
        view_details.connect("activate", on_view_details)
        self.add_action(view_details)

        def on_close_details_view(
                action: Gio.Action,
                parameters: None) -> None:
            self.close_details_view()
        close_details_view = Gio.SimpleAction.new(
            "close-details-view",
            None)
        close_details_view.connect("activate", on_close_details_view)
        self.add_action(close_details_view)

        def on_clean_metadata(action: Gio.Action, parameters: None) -> None:
            self.close_details_view()
            if not self.get_application() \
                    .settings.get_boolean("cleaning-without-warning"):
                self._cleaning_warning_dialog.choose(self)
                return
            self.file_store.clean_files()
        clean_metadata = Gio.SimpleAction.new("clean-metadata", None)
        clean_metadata.connect("activate", on_clean_metadata)
        clean_metadata.set_enabled(False)
        self.add_action(clean_metadata)

    # SIGNALS

    @Gtk.Template.Callback()
    def _on_sidebar_toggled(self,
            widget: Gtk.Widget,
            pspec: GObject.ParamSpec) -> None:
        if self._split_view.get_show_sidebar() == False:
            self._view_stack.get_child_by_name("files").clear_selected_file()

    def _on_file_chooser_dialog_response(
            self, file_dialog: Gtk.FileDialog, result: Gio.AsyncResult) -> None:
        try:
            self.file_store.add_gfiles(file_dialog.open_multiple_finish(result))
        except GLib.Error as e:
            if e.code == 2:
                # dismissed
                return

            error(f"Couldn't open files: {e.code} {e.message}")
            return

    def _on_folder_chooser_dialog_response(
            self, file_dialog: Gtk.FileDialog, result: Gio.AsyncResult) -> None:
        try:
            self.file_store.add_gfiles(
                file_dialog.select_multiple_folders_finish(result),
                True)
        except GLib.Error as e:
            if e.code == 2:
                # dismissed
                return

            error(f"Couldn't open folders: {e.code} {e.message}")
            return

    @Gtk.Template.Callback()
    def _on_cleaning_warning_dialog_response(
            self,
            dialog: CleaningWarningDialog,
            response: str) -> None:
        if response == "clean":
            self.file_store.clean_files()

    def _on_show_info_dialog(self) -> None:
        dlg = Adw.Dialog.new()
        dlg.set_title(_("Info"))
        dlg.set_content_width(600)
        dlg.set_content_height(500)
        box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.append(Gtk.Label(label=_("Meatadata & Privacy"), wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR, xalign=0, css_classes=["heading"], margin_top = 6))
        box.append(Gtk.Label(label=_("Metadata consists of information that characterizes data. Metadata is used to provide documentation for data products. In essence, metadata answers who, what, when, where, why, and how about every facet of the data that is being documented.\nMetadata within a file can tell a lot about you. Cameras record data about when and where a picture was taken and which camera was used. Office applications automatically add author and company information to documents and spreadsheets. This is sensitive information and you may not want to disclose it."), xalign=0, wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR))
        box.append(Gtk.Label(label=_("Cleaning Process"), wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR, xalign=0, css_classes=["heading"], margin_top = 6))
        box.append(Gtk.Label(label=_("While Metadata Cleaner is doing its very best to display metadata, it doesn't mean that a file is clean from metadata if it doesn't show any. There is no reliable way to detect every single possible metadata for complex file formats. This is why you shouldn't rely on metadata's presence to decide if your file must be cleaned or not.\nMetadata Cleaner takes the content of the file and puts it into a new one without metadata, ensuring that any undetected metadata is stripped."), xalign=0, wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR))
        box.append(Gtk.Label(label=_("Limitations"), wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR, xalign=0, css_classes=["heading"], margin_top = 6))
        box.append(Gtk.Label(label=_("Be aware that metadata is not the only way of marking a file. If the content itself discloses personal information or has been watermarked, traditionally or via steganography, Metadata Cleaner will not protect you."), xalign=0, wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR))
        tbarview = Adw.ToolbarView(content=Gtk.ScrolledWindow(
            propagate_natural_height = True,
            propagate_natural_width = True,
            child=Adw.Clamp(child=box, margin_start = 6, margin_end = 6, margin_bottom = 6)))
        tbarview.add_top_bar(Adw.HeaderBar.new())
        dlg.set_child(tbarview)
        dlg.present(self)

    # VIEWS #

    def show_empty_view(self) -> None:
        """Show an empty view."""
        self._add_files_button.set_visible(False)
        self._view_stack.set_visible_child_name("empty")
        self._header.set_show_title(False)
        self.lookup_action("clear-files").set_enabled(False)

    def show_files_view(self) -> None:
        """Show the files."""
        self._add_files_button.set_visible(True)
        self._view_stack.set_visible_child_name("files")
        self._header.set_show_title(True)
        self.lookup_action("clear-files").set_enabled(True)

    def open_details_view(self) -> None:
        """Show the details view."""
        self._split_view.set_show_sidebar(True)

    def close_details_view(self) -> None:
        """Close the details view."""
        self._split_view.set_show_sidebar(False)
