import gi
from modules import args_handler, config_handler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class main_window(Gtk.Window):
    # main GTK window
    def __init__(self):
        super().__init__()
        self.set_decorated(False) # remove window decoration

        self.connect("destroy", Gtk.main_quit)

        # close on q press
        self.connect('key-press-event', self.quit_on_q)

    # need to have a function for that to access the event name
    def quit_on_q(self, widget, event):
        if event.keyval == Gdk.KEY_q:
            # if the key value is q, close the window
            print('Closing window...') # debug
            self.close()

def main():
    # get the args parser
    parser = args_handler.init_args()
    args = parser.parse_args() # get all available args
    
    if args.create_config:
        # call write_config if create_config is in args
        config_handler.write_config()
    if args.standard:
        print('Open clipboard image in default img viewer')
    if args.pin:
        print('Pin clipboard image to desktop')
    if args.file:
        print('Open file chooser')
    
    win = main_window()
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
