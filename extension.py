import gi
gi.require_version('Nautilus', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Nautilus, GObject, GLib, Gtk


class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):

    def open_quickstart_gui(self, menu, file):
        win = Gtk.Window()
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        Gtk.main()

    def get_file_items(self, window, files):
        if len(files) != 1:
            return

        file = files[0]

        if not self._check_executable(file):
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
