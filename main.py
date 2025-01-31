import gi
from modules import args_handler, config_handler, image_handler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class main_window(Gtk.Window):
    # main GTK window
    def __init__(self, img_x=None, img_y=None, img=None):
        super().__init__()
        self.set_decorated(False)  # remove window decoration

        # set size of window if img was given
        if img_x and img_y:
            self.set_default_size(img_x, img_y)

        self.connect("destroy", Gtk.main_quit)

        # -- Button click events --
        self.connect("key-press-event", self.quit_on_q)  # close on q press
        self.connect("button-press-event", self.on_mouse_click)  # start drag
        self.connect("button-release-event", self.on_mouse_release)  # start drag
        self.connect(
            "motion-notify-event", self.move_window
        )  # move window if motion is detected

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

        # show image if image was given
        if img:
            self.display_image(img)

    # need to have a function for that to access the event name
    def quit_on_q(self, widget, event):
        if event.keyval == Gdk.KEY_q:
            # if the key value is q, close the window
            print("Closing window...")  # debug
            self.close()

    def on_mouse_click(self, widget, event):
        # This function just saves the position of the mouse in the window
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:  # left click
            self.start_x, self.start_y = event.x_root, event.y_root
            self.window_x, self.window_y = self.get_position()

            self.dragging = True

    def on_mouse_release(self, widget, event):
        # canceles dragging mode if mouse button is released
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.button == 1:
            self.dragging = False

    def move_window(self, widget, event):
        # Moves the window based on mouse movement
        if (
            event.state & Gdk.ModifierType.BUTTON1_MASK
        ):  # check if left mouse button is pressed
            # calculate new position
            new_x = self.window_x + (event.x_root - self.start_x)
            new_y = self.window_y + (event.y_root - self.start_y)
            self.move(new_x, new_y)

    def display_image(self, img):
        image = Gtk.Image.new_from_pixbuf(img)
        self.add(image)



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

    win = main_window(img=pixbuf)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
