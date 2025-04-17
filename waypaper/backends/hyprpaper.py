from .base import Backend


class HyprpaperBackend(Backend):
    """
    Backend using hyprpaper
    """

    @property
    def name(self) -> str:
        return "Hyprpaper"

    @property
    def allowed_extensions(self) -> list[str]:
        return [".jpg", ".jpeg", ".png", ".webp"]

    @property
    def binary_name(self) -> str | None:
        return "hyprpaper"
