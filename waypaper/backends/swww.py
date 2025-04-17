from .base import Backend


class SwwwBackend(Backend):
    """
    Backend using swww
    """

    @property
    def name(self) -> str:
        return "swww"

    @property
    def allowed_extensions(self) -> list[str]:
        return [".gif", ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".pnm", ".tiff"]

    @property
    def binary_name(self) -> str | None:
        return "swww"
