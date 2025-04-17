from .base import Backend


class SwayBgBackend(Backend):
    """
    Backend using swaybg
    """

    @property
    def name(self) -> str:
        return "swaybg"

    @property
    def allowed_extensions(self) -> list[str]:
        return [".gif", ".jpg", ".jpeg", ".png"]

    @property
    def binary_name(self) -> str | None:
        return "swaybg"
