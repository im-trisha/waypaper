import os.path
from pathlib import Path
from abc import ABC, abstractmethod


class Backend(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def binary_name(self) -> str | None: ...

    @property
    @abstractmethod
    def allowed_extensions(self) -> list[str]: ...

    def is_extension_supported(self, path: str) -> bool:
        ext = os.path.splitext(path)[1].lower()
        return ext in self.allowed_extensions

    def get_supported_images(
        self,
        folders: list[str],
        include_subfolders: bool = False,
        include_all_subfolders: bool = False,
        include_hidden: bool = False,
        only_gifs: bool = False,
    ) -> list[str]:
        """Get a list of file paths depending on the filters that were requested."""
        paths: list[str] = []

        for folder in folders:
            for root, directories, files in os.walk(folder, followlinks=True):
                if not include_hidden:
                    directories[:] = [d for d in directories if not d.startswith(".")]

                if not include_subfolders and root != folder:
                    continue

                depth = len(Path(root).relative_to(folder).parts)
                if not include_all_subfolders and depth > 1:
                    continue

                # Remove files that are not images from consideration:
                for file in files:
                    if not include_hidden and file.startswith("."):
                        continue

                    if not self.is_extension_supported(file):
                        continue

                    if only_gifs and not file.lower().endswith(".gif"):
                        continue

                    paths.append(os.path.join(root, file))

        return paths


class NoBackend(Backend):
    """
    A no-backend backend. Everything will just be no-ops
    """

    @property
    def name(self) -> str:
        return "None"

    @property
    def allowed_extensions(self) -> list[str]:
        return [".gif", ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".pnm", ".tiff"]

    @property
    def binary_name(self) -> str | None:
        return None
