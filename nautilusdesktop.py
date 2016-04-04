import os
import hashlib
import gi
gi.require_version('Nautilus', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Nautilus, GObject, GLib, Gtk, GdkPixbuf


class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):

    def open_quickstart_gui(self, menu, file):
        NautilusDesktopGui().show("nautilusdesktop.glade", file.get_location().get_path())

    def get_file_items(self, window, files):
        if len(files) != 1:
            return

        file = files[0]

        if not os.path.isfile(file.get_location().get_path()) or not self._check_executable(file):
            return

        item = Nautilus.MenuItem(
            name="SimpleMenuExtension::Show_File_Name",
            label="Create a shell shortcut for %s" % file.get_name(),
            tip="Create a shell shortcut for %s" % file.get_name()
        )
        item.connect('activate', self.open_quickstart_gui, file)

        return [item]

    def _check_executable(self, file):
        """True if the file seems executable"""
        return GLib.file_test(file.get_location().get_path(), GLib.FileTest.IS_EXECUTABLE)


class Handler:
    def __init__(self, builder, executable):
        self.__starter_file = ""
        self.builder = builder
        self.window = builder.get_object("applicationWindow")
        builder.get_object("applicationFileChooser").set_filename(executable)

    def on_cancelButton_clicked(self, *args):
        self.window.destroy()
        Gtk.main_quit(*args)

    def on_saveButton_clicked(self, button):
        title = self.builder.get_object("titleEntry").get_text()
        categories = self.builder.get_object("categoriesEntry").get_text()
        application_file = self.builder.get_object("applicationFileChooser").get_filename()

        if title == "":
            self._error_dialog("Wrong input", "Title can't be empty!")
            return
        if application_file is None:
            self._error_dialog("Wrong input", "Application path can't be empty!")
            return

        with open("{0}/.local/share/applications/nautilus-starter-{1}.desktop".format(os.path.expanduser("~"), hashlib.sha1(application_file).hexdigest()), "w+") as desktop_file:
            desktop_file.write("[Desktop Entry]\nType=Application\nName={0}\nExec={1}\nIcon={2}\nCategories={3}".format(title, application_file, self.__starter_file, categories))

        self.window.destroy()
        Gtk.main_quit()

    def on_starterButton_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            "Select image",
            self.window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        preview = self.builder.get_object("previewImage")
        dialog.set_preview_widget(preview)
        dialog.connect("update_preview", self.on_starterFileChooser_update_preview, preview)

        application_file = self.builder.get_object("applicationFileChooser").get_filename()
        if application_file is not None:
            dialog.set_current_folder(os.path.dirname(application_file))

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.__starter_file = dialog.get_filename()
            image = self.builder.get_object("starterImage")
            image.set_from_file(dialog.get_filename())
            image.set_from_pixbuf(self._scale_pixbuf(image.get_pixbuf(), 50))

        dialog.destroy()

    def on_starterFileChooser_update_preview(self, dialog, preview):
        if dialog.get_preview_filename() is None:
            return

        preview.set_from_file(dialog.get_preview_filename())

        if preview.get_pixbuf() is not None:
            preview.set_from_pixbuf(self._scale_pixbuf(preview.get_pixbuf(), 100))

    def _scale_pixbuf(self, pixbuf, max_size):
        heigher = pixbuf.get_height() > pixbuf.get_width()
        ratio = 1.0 * pixbuf.get_height() / pixbuf.get_width()
        return pixbuf.scale_simple(
            max_size / ratio if heigher else max_size, max_size if heigher else max_size * ratio,
            GdkPixbuf.InterpType.BILINEAR)

    def _error_dialog(self, title, text):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, title)
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()


class NautilusDesktopGui:
    def show(self, glade_file, executable):
        builder = Gtk.Builder()
        builder.add_from_file(glade_file)
        builder.connect_signals(Handler(builder, executable))

        window = builder.get_object("applicationWindow")
        window.show_all()

        Gtk.main()
