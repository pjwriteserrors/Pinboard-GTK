import os
import json


def write_config():
    # store in name for ez location
    settings_file = os.path.expanduser("~") + "/.config/pinboard/settings.json"

    # dict of all default settings
    settings = {
        "always_on_top": True,
        "close_key": "q",
        'increase_size_key': '+',
        'decrease_size_key': '-',
        "reset_size_key": "b",
        "buttons": False,
    }

    print("Writing new config file...")  # debug
    with open(settings_file, "w") as file:
        json.dump(settings, file, indent=4) # dump settings into file

    return settings


def read_config() -> dict:
    # store in name for ez location
    settings_file = os.path.expanduser("~") + "/.config/pinboard/settings.json"

    if os.path.isfile(settings_file):
        with open(settings_file, "r") as file:
            settings = json.load(file) # load dict of all settings stored in the file
    else:
        settings = write_config()

    return settings
