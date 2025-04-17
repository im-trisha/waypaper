"""Main module that either runs cli commands or starts GUI"""

import argparse, sys, time, json, pathlib, threading

from waypaper.app import App
from waypaper.changer import change_wallpaper
from waypaper.common import get_random_file
from waypaper.config import Config
from waypaper.options import BackendOptions, FillOptions, MONITOR_OPTIONS
from i18n import I18N, Languages


__version__ = "2.5"

# Get application settings and language package:
cf = Config()
txt = I18N.strings(Languages.FRENCH)

# Define command line argument parser and parse user arguments:
parser = argparse.ArgumentParser(prog=cf.name, description=txt.desc, epilog=txt.info)
parser.add_argument("-v", "--version", help=txt.arg_help, action="store_true")
parser.add_argument("--restore", help=txt.arg_rest, action="store_true")
parser.add_argument("--random", help=txt.arg_rand, action="store_true")
parser.add_argument("--fill", help=txt.arg_fill, choices=FillOptions)
parser.add_argument("--wallpaper", help=txt.arg_wall)
parser.add_argument("--folder", help=txt.arg_folder, nargs="+", default=[])
parser.add_argument("--state-file", help=txt.arg_statefile)
parser.add_argument("--backend", help=txt.arg_back, choices=BackendOptions)
parser.add_argument("--list", help=txt.arg_list, action="store_true")
parser.add_argument("--monitor", help=txt.arg_monitor, choices=MONITOR_OPTIONS)
parser.add_argument("--no-post-command", help=txt.arg_post, action="store_true")
args = parser.parse_args()


def run():
    """Read user arguments and either run GUI app or perform requested action"""

    # Read user arguments, and update things if alternative state file was provided:
    # TODO: Change this. parser.parse_args should use a callback
    cf.read_parameters_from_user_arguments(args)
    if args.state_file:
        cf.read_state()
        cf.read_parameters_from_user_arguments(args)
    cf.check_validity()

    # Set monitor and wallpaper from user arguments:
    if args.monitor:
        monitor = args.monitor

        # Set wallpaper from user arguments if provided:
        if args.wallpaper:
            wallpaper = pathlib.Path(args.wallpaper).expanduser()

        # Otherwise set a random wallpaper:
        else:
            wallpaper_str = get_random_file(
                cf.backend,
                cf.image_folder_list,
                cf.include_subfolders,
                cf.include_all_subfolders,
                cf.cache_dir,
                cf.show_hidden,
            )
            if wallpaper_str:
                wallpaper = pathlib.Path(wallpaper_str)
            else:
                print("Could not get random wallpaper.")
                sys.exit(0)

        # Launch commands to change wallpaper in a separate thread:
        threading.Thread(target=change_wallpaper, args=(wallpaper, cf, monitor)).start()
        time.sleep(0.1)

        # Save this wallpaper in config and quit:
        cf.selected_wallpaper = wallpaper
        cf.selected_monitor = monitor
        cf.attribute_selected_wallpaper()
        if cf.use_xdg_state:
            cf.save_state_file()
        else:
            cf.save()
        sys.exit(0)

    # Set previous wallpapers or random wallpaper:
    if args.restore or args.random:
        for index, (wallpaper, monitor) in enumerate(zip(cf.wallpapers, cf.monitors)):
            if args.random:
                wallpaper_str = get_random_file(
                    cf.backend,
                    cf.image_folder_list,
                    cf.include_subfolders,
                    cf.include_all_subfolders,
                    cf.cache_dir,
                    cf.show_hidden,
                )
                if wallpaper_str:
                    wallpaper = pathlib.Path(wallpaper_str)
                    cf.wallpapers[index] = wallpaper

            if cf.wallpapers[index] is None:
                continue

            # Launch commands to change wallpaper in a separate thread:
            threading.Thread(
                target=change_wallpaper, args=(wallpaper, cf, monitor)
            ).start()
            time.sleep(0.1)

        # Save new wallpapers:
        if cf.use_xdg_state:
            cf.save_state_file()
        else:
            cf.save()
        sys.exit(0)

    # Set wallpaper from user arguments:
    if args.wallpaper:
        monitor = "All"
        wallpaper = pathlib.Path(args.wallpaper).expanduser()
        threading.Thread(target=change_wallpaper, args=(wallpaper, cf, monitor)).start()

        # Save this wallpaper in config and quit:
        cf.selected_wallpaper = wallpaper
        cf.selected_monitor = monitor
        cf.attribute_selected_wallpaper()
        if cf.use_xdg_state:
            cf.save_state_file()
        else:
            cf.save()
        sys.exit(0)

    # Output some information in json format:
    if args.list:
        info = list(
            map(
                lambda x: {
                    "monitor": x[0],
                    "wallpaper": str(x[1]),
                    "backend": cf.backend,
                },
                zip(cf.monitors, cf.wallpapers),
            )
        )
        print(json.dumps(info))
        sys.exit(0)

    # Print the version and quit:
    if args.version:
        print(f"waypaper v.{__version__}")
        sys.exit(0)

    # Start GUI:
    app = App(txt, cf)
    app.run()


if __name__ == "__main__":
    run()
