import argparse

def init_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Pinboard is a simple Python GTK app that can pin your images to your desktop.')
    parser.add_argument('-s', '--standard', nargs='?', const=True, metavar='', help='Open clipboard image in default image viewer')
    parser.add_argument('-p', '--pin', nargs='?', const=True, metavar='', help='Pin image to desktop')
    parser.add_argument('-f', '--file', nargs='?', const=True, metavar='', help='Select a file to display (need to specify --pin/-p or --standard/-s)')
    parser.add_argument('-c', '--create_config', nargs='?', const=True, metavar='', help='Make config file (Waring: Overwrites the current file if exists)')

    return parser