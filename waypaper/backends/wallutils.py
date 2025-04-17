from .base import Backend


class WallutilsBackend(Backend):
    """
    Backend using wallutils
    """

    @property
    def name(self) -> str:
        return "wallutils"

    @property
    def allowed_extensions(self) -> list[str]:
        return [".gif", ".jpg", ".jpeg", ".png"]

    @property
    def binary_name(self) -> str | None:
        return "setwallpaper"
