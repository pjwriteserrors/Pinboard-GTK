import gi
from modules import args_handler, config_handler, image_handler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf


class main_window(Gtk.Window):
    def __init__(self, img_x=None, img_y=None, img=None):
        super().__init__()
        self.settings = config_handler.read_config()

        self.set_decorated(False)  # remove window decoration

        # always on top if set in settings
        if self.settings["always_on_top"]:
            self.set_keep_above(True)

        # set size of window if img was given
        if img_x and img_y:
            self.set_default_size(img_x, img_y)

        self.connect("destroy", Gtk.main_quit)

        # -- Button click events --
        self.connect("key-press-event", self.quit)  # close on q press
        self.connect("button-press-event", self.on_mouse_click)  # start drag
        self.connect("button-release-event", self.on_mouse_release)  # start drag
        self.connect(
            "motion-notify-event", self.mouse_move
        )  # move window if motion is detected
        self.connect("key-press-event", self.resize_window)  # resize image

        # register window to understand mouse events
        self.set_events(
            Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
            | Gdk.EventMask.POINTER_MOTION_MASK
        )

        self.dragging = False  # name to store if window is being dragged

        # start position
        self.start_x = 0
        self.start_y = 0

        self.img_widget = Gtk.Image()
        self.original_pixbuf = img

        # show image if image was given
        if img:
            self.display_image(img)

    # need to have a function for that to access the event name
    def quit(self, widget, event):
        if event.keyval == ord(self.settings["close_key"]):
            # if the key value is q, close the window
            self.close()

    def on_mouse_click(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            # start dragging if left click is pressed
            self.start_x, self.start_y = event.x_root, event.y_root
            self.window_x, self.window_y = self.get_position()
            self.dragging = True

    def on_mouse_release(self, widget, event):
        # canceles dragging/resizing mode if mouse button is released
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.button == 1:
            self.dragging = False

    def mouse_move(self, widget, event):
        if self.dragging:
            # calculate new position
            new_x = self.window_x + (event.x_root - self.start_x)
            new_y = self.window_y + (event.y_root - self.start_y)
            self.move(new_x, new_y)

    def display_image(self, img):
        # add image widget to window
        self.img_widget.set_from_pixbuf(img)
        self.add(self.img_widget)
        self.show_all()

    def resize_window(self, widget, event):
        # change size of window and image with scale factor
        if event.keyval == ord(self.settings["increase_size_key"]):
            new_width = int(self.get_size()[0] * 1.1)
            new_height = int(self.get_size()[1] * 1.1)
        elif event.keyval == ord(self.settings["decrease_size_key"]):
            new_width = int(self.get_size()[0] * 0.9)
            new_height = int(self.get_size()[1] * 0.9)
        elif event.keyval == ord(self.settings["reset_size_key"]):
            # reset image and window size
            new_width, new_height = (
                self.original_pixbuf.get_width(),
                self.original_pixbuf.get_height(),
            )
        else:
            return

        self.resize(new_width, new_height)
        self.resize_image(new_width, new_height)

    def resize_image(self, new_width, new_height):
        if self.original_pixbuf:
            # scale the pixbuf
            scaled_pixbuf = self.original_pixbuf.scale_simple(
                new_width, new_height, GdkPixbuf.InterpType.BILINEAR
            )
            # set newly scaled pixbuf into image widget and display
            self.img_widget.set_from_pixbuf(scaled_pixbuf)
            self.show_all()


def main():
    # get the args parser
    parser = args_handler.init_args()
    args = parser.parse_args()  # get all available args

    # set -p as default if no args have been given
    if not any(vars(args).values()):
        args.pin = True

    if args.create_config:
        # call write_config if create_config is in args
        config_handler.write_config()

    if args.standard:
        print("Open clipboard image in default img viewer")

    if args.file:
        print("Open file chooser")

    if args.pin:
        img_x, img_y, pixbuf = image_handler.get_image_clipboard()
        win = main_window(img_x, img_y, img=pixbuf)
    else:
        win = main_window()

    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
