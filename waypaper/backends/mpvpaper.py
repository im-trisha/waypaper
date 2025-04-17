from waypaper.consts import VIDEO_EXTENSIONS
from .base import Backend


class MpvPaperBackend(Backend):
    """
    Backend using mpvpaper
    """

    @property
    def name(self) -> str:
        return "mpvpaper"

    @property
    def allowed_extensions(self) -> list[str]:
        return [
            ".gif",
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".bmp",
            ".pnm",
            ".tiff",
            ".avif",
        ] + VIDEO_EXTENSIONS

    @property
    def binary_name(self) -> str | None:
        return "mpvpaper"
