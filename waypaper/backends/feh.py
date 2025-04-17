from .base import Backend


class FehBackend(Backend):
    """
    Backend using feh
    """

    @property
    def name(self) -> str:
        return "feh"

    @property
    def allowed_extensions(self) -> list[str]:
        return [".gif", ".jpg", ".jpeg", ".png", ".bmp", ".pnm", ".tiff"]

    @property
    def binary_name(self) -> str | None:
        return "feh"
