"""Module with some of the common functions, like file and image operations"""

import os, random, shutil, gi
import imageio as iio
from pathlib import Path
from PIL import Image
from gi.repository import GdkPixbuf

from waypaper.consts import VIDEO_EXTENSIONS
from waypaper.options import BackendOptions
from waypaper.backends import Backend

gi.require_version("Gtk", "3.0")


def get_image_name(full_path: str, base_folders: list[Path], include_path: bool) -> str:
    """Get image name that may or may not include parent folders"""
    resolved_path: Path = Path(full_path).resolve()

    if not include_path:
        return resolved_path.name

    for base_folder in base_folders:
        base_folder = Path(base_folder).resolve()
        if resolved_path.is_relative_to(base_folder):
            relative_path = resolved_path.relative_to(base_folder)
            return str(base_folder.name / relative_path)

    # If no base folder matched, fallback to just the file name
    return resolved_path.name


def get_random_file(
    backend: Backend,
    folder_list: list[str],
    include_subfolders: bool,
    include_all_subfolders: bool,
    cache_dir: Path,
    include_hidden: bool = False,
) -> str | None:
    """Pick a random file from the folder and update cache"""
    try:
        # Get all image paths from the folder:
        image_paths = get_image_paths(
            backend,
            folder_list,
            include_subfolders,
            include_all_subfolders,
            include_hidden,
            only_gifs=False,
        )

        # Read cache file with already used images:
        cache_file = cache_dir / "used_wallpapers.txt"
        if cache_file.exists():
            with cache_file.open("r") as file:
                used_images = [line.strip() for line in file.readlines()]
        # Create it if the file does not exists:
        else:
            cache_file.touch()
            used_images = []

        # Pick a random image from unused images:
        remaining_images = list(
            filter(lambda img: img not in set(used_images), image_paths)
        )
        if remaining_images:
            random_image = random.choice(remaining_images)
            used_images.append(random_image)
        else:
            random_image = random.choice(image_paths)
            used_images = [random_image]

        # Write the cache file:
        with cache_file.open("w") as file:
            for img in used_images:
                file.write(img + "\n")

        return random_image

    except Exception as e:
        print(f"Error getting random image: {e}")
        return None


def check_installed_backends() -> list[Backend]:
    """Check which backends are installed in the system"""
    return [
        option.backend
        for option in BackendOptions
        if option.backend.binary_name and shutil.which(option.backend.binary_name)
    ]


def cache_image(image_path: str, cache_dir: Path) -> None:
    """Create small copies of images using various libraries depending on the file type"""
    ext = os.path.splitext(image_path)[1].lower()
    cache_file = cache_dir / Path(os.path.basename(image_path))
    width = 240

    try:
        # If it's a video, extract the first frame:
        if ext in VIDEO_EXTENSIONS:
            reader = iio.get_reader(image_path)
            first_frame = reader.get_data(0)
            # Convert the numpy array to a PIL image:
            pil_image = Image.fromarray(first_frame)
            aspect_ratio = pil_image.height / pil_image.width
            new_height = int(width * aspect_ratio)
            resized_image = pil_image.resize((width, new_height))
            resized_image.save(str(cache_file), "JPEG")
            return

        # If it's an image, create preview depending on the filetype
        if ext == ".webp":
            img = Image.open(image_path)
            data = img.tobytes()
            img_width, img_height = img.size
            pixbuf = GdkPixbuf.Pixbuf.new_from_data(
                data,
                GdkPixbuf.Colorspace.RGB,
                False,
                8,
                img_width,
                img_height,
                img_width * 3,
            )
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(image_path))
        aspect_ratio = pixbuf.get_width() / pixbuf.get_height()
        height = int(width / aspect_ratio)
        scaled_pixbuf = pixbuf.scale_simple(
            width, height, GdkPixbuf.InterpType.BILINEAR
        )
        scaled_pixbuf.savev(str(cache_file), "jpeg", [], [])

    # If image processing failed, create a black placeholder:
    except Exception as e:
        print(f"Could not generate preview for {os.path.basename(image_path)}")
        print(e)
        black_pixbuf = GdkPixbuf.Pixbuf.new(
            GdkPixbuf.Colorspace.RGB, True, 8, width, width * 9 / 16
        )
        black_pixbuf.fill(0x0)
        black_pixbuf.savev(str(cache_file), "jpeg", [], [])
