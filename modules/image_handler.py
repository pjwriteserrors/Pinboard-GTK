import gi
import sys

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf, Gtk

from PIL import ImageGrab, Image


def get_image():
    # grab the image from the clipboard and return size and pixbuf
    img = get_image_clipboard()
    width, height, pixbuf = make_pixbuf(img)

    return width, height, pixbuf


def show_img_in_viewer():
    img = get_image_clipboard()
    # show in default viewer
    img.show()


def get_image_clipboard():
    # get image from clipboard and return it if there is image in clipboard
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        return img
    else:
        print("No image in clipboard.")
        sys.exit()


def open_file_dialog():
    # make file chooser
    dialog = Gtk.FileChooserDialog(
        title="Choose image",
        action=Gtk.FileChooserAction.OPEN,
        buttons=(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        ),
    )

    # setting filters
    filter_images = Gtk.FileFilter()
    filter_images.set_name("Images (JPG, PNG)")
    filter_images.add_mime_type("image/jpeg")
    filter_images.add_mime_type("image/png")

    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        # get filepath
        file_path = dialog.get_filename()
        dialog.destroy()

        # make pillow img to convert to pixbuf
        img = Image.open(file_path)

        width, height, pixbuf = make_pixbuf(img)
        return width, height, pixbuf

    dialog.destroy()
    return

def make_pixbuf(img):
    width, height = img.size
    img_data = img.tobytes()

    # make pixbuf
    pixbuf = GdkPixbuf.Pixbuf.new_from_data(
        img_data,
        GdkPixbuf.Colorspace.RGB,
        True,  # has alpha
        8,  # bits per sample
        width,
        height,
        width * 4,  # rowstride (RGBA = 4 Bytes per pixel)
    )

    return width, height, pixbuf
