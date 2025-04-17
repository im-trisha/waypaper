from babel.support import Translations
from enum import Enum


class Languages(Enum):
    ENGLISH = 0
    GERMAN = 1
    FRENCH = 2
    SPANISH = 3
    POLISH = 4
    RUSSIAN = 5
    BELARUSSIAN = 6
    CHINESE = 7
    TRADITIONAL_CHINESE = 8


class I18N:
    @staticmethod
    def strings(lang: Languages = Languages.ENGLISH) -> "LocalizedStrings":
        return LocalizedStrings(lang)


class LocalizedStrings:
    def __init__(self, lang: Languages):
        translation = Translations.load("i18n/", (lang.name,))
        self._ = translation.gettext
        self._n = translation.ngettext

    @property
    def desc(self) -> str:
        return self._(
            "GUI wallpaper setter for Wayland and X11. It works as a frontend for feh, swaybg, wallutils, hyprpaper, mpvpaper, and swww."
        )

    @property
    def info(self) -> str:
        return self._(
            "For more information, visit:\nhttps://github.com/anufrievroman/waypaper"
        )

    @property
    def arg_help(self) -> str:
        return self._("print version of the program")

    @property
    def arg_fill(self) -> str:
        return self._("specify how to fill the screen with chosen image")

    @property
    def arg_rest(self) -> str:
        return self._("restore last wallpaper")

    @property
    def arg_back(self) -> str:
        return self._("specify which backend to use to set wallpaper")

    @property
    def arg_rand(self) -> str:
        return self._("set a random wallpaper")

    @property
    def arg_list(self) -> str:
        return self._("lists some parameters in json to standard out")

    @property
    def arg_wall(self) -> str:
        return self._("set the specified wallpaper")

    @property
    def arg_folder(self) -> str:
        return self._("specify which folder to scan for wallpapers")

    @property
    def arg_statefile(self) -> str:
        return self._("specify a custom file to store the application state")

    @property
    def arg_monitor(self) -> str:
        return self._("specify desired monitor using its name")

    @property
    def arg_post(self) -> str:
        return self._("prevents running post_command set in config")

    @property
    def arg_show_path_in_tooltip(self) -> str:
        return self._("show the relative path in the tooltip")

    @property
    def select(self) -> str:
        return self._("Select")

    @property
    def refresh(self) -> str:
        return self._("Refresh")

    @property
    def clear(self) -> str:
        return self._("Clear")

    @property
    def start(self) -> str:
        return self._("Start auto-change")

    @property
    def stop(self) -> str:
        return self._("Stop all")

    @property
    def sound(self) -> str:
        return self._("Sound")

    @property
    def pause(self) -> str:
        return self._("Pause")

    @property
    def search(self) -> str:
        return self._("Search")

    @property
    def random(self) -> str:
        return self._("Random")

    @property
    def exit(self) -> str:
        return self._("Exit")

    @property
    def options(self) -> str:
        return self._("Options")

    @property
    def subfolders(self) -> str:
        return self._("Show subfolders")

    @property
    def all_subfolders(self) -> str:
        return self._("Show all subfolders")

    @property
    def hidden(self) -> str:
        return self._("Show hidden")

    @property
    def gifs(self) -> str:
        return self._("Show gifs only")

    @property
    def transitions(self) -> str:
        return self._("Show transition options")

    @property
    def changefolder(self) -> str:
        return self._("Folder")

    @property
    def choosefolder(self) -> str:
        return self._("Please choose a folder")

    @property
    def caching(self) -> str:
        return self._("Caching wallpapers...")

    @property
    def show_path_in_tooltip(self) -> str:
        return self._("Show path in tooltip")

    @property
    def help(self) -> str:
        return (
            self._(
                "Waypaper's hotkeys:\n\nhjkl - Navigation (←↓↑→)\nEnter - Set selected wallpaper\nf - Change wallpaper folder\n"
                "g - Scroll to top\nG - Scroll to bottom\nR - Set random wallpaper\nr - Recache wallpapers\n"
                ". - Toggle hidden images\ns - Toggle images in subfolders\n/ - Search\n? - Help\nq - Exit\n\n"
            )
            + self.info
        )

    @property
    def err_cache(self) -> str:
        return self._("Error deleting cache")

    @property
    def err_backend(self) -> str:
        return (
            self._(
                "Looks like none of the wallpaper backends is installed in the system.\n"
                "Use your package manager to install at least one of these backends:\n\n"
                "- swaybg (Wayland)\n- swww (Wayland)\n"
                "- hyprpaper (Wayland)\n- feh (Xorg)\n"
                "- wallutils (Xorg & Wayland)\n- mpvpaper (Xorg & Wayland)\n\n"
            )
            + self.info
        )

    @property
    def tip_refresh(self) -> str:
        return self._("Recache the folder of images")

    @property
    def tip_fill(self) -> str:
        return self._("Choose fill type")

    @property
    def tip_backend(self) -> str:
        return self._("Choose backend")

    @property
    def tip_sorting(self) -> str:
        return self._("Choose sorting type")

    @property
    def tip_display(self) -> str:
        return self._("Choose display")

    @property
    def tip_color(self) -> str:
        return self._("Choose background color")

    @property
    def tip_random(self) -> str:
        return self._("Set random wallpaper")

    @property
    def tip_exit(self) -> str:
        return self._("Exit the application")

    @property
    def tip_transition(self) -> str:
        return self._("Choose transition type")

    @property
    def tip_mpv_stop(self) -> str:
        return self._("Stop all all mpv processes")

    @property
    def tip_mpv_pause(self) -> str:
        return self._("Play/Pause video wallpaper")

    @property
    def tip_mpv_sound(self) -> str:
        return self._("Play sound of the video")

    @property
    def tip_timer(self) -> str:
        return self._("How often to automatically change wallpaper")

    @property
    def tip_start(self) -> str:
        return self._("Initiate automatic change of wallpaper after a time interval")
