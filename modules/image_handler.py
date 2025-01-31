import gi
import sys

gi.require_version("Gtk", "3.0")
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

from PIL import ImageGrab, Image


def get_image_clipboard():
    # grab the image from the clipboard and return size and file if there is image in clipboard
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        width, height = img.size
        img_data = img.tobytes()
        
        # make pixbuf
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(
            img_data,
            GdkPixbuf.Colorspace.RGB,
            True, # has alpha
            8, # bits per sample
            width,
            height,
            width * 4 # rowstride (RGBA = 4 Bytes per pixel)
        )

        return width, height, pixbuf
    else:
        print('No image in clipboard.')
        sys.exit()
