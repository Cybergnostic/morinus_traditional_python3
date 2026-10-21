"""Shared presentation helpers for bitmap-backed Morinus tables.

These change only *display*, never the computed table values or column
selection. Specialist speculum tables retain all original numerical fields.
"""
import math
from PIL import Image, ImageFilter

MIN_ZOOM = 0.5
MAX_ZOOM = 3.0
MAX_DISPLAY_PIXELS = 24_000_000


def zoom_value(requested, width, height):
    """Fit a requested zoom in range without allocating an enormous bitmap."""
    value = max(MIN_ZOOM, min(MAX_ZOOM, float(requested)))
    pixels = max(1, int(width)) * max(1, int(height))
    if pixels * value * value > MAX_DISPLAY_PIXELS:
        value = max(MIN_ZOOM, min(value, math.sqrt(MAX_DISPLAY_PIXELS / pixels)))
    value = round(value, 3)
    return 1.0 if abs(value - 1.0) < 0.01 else value


def pixel_size(width, height, zoom):
    """Display raster dimensions, independent of scroll and export sizing."""
    return (max(1, round(width * zoom)), max(1, round(height * zoom)))


def anchored_scroll(origin, pointer, old_zoom, new_zoom):
    """Keep the source point under pointer fixed when changing zoom."""
    return max(0, round(((origin + pointer) / old_zoom) * new_zoom - pointer))


def header_colour(background, grid, black_white=False):
    """Gentle tint for headings. Monochrome mode remains strictly original."""
    if black_white:
        return tuple(background)
    return tuple(round(b * 0.92 + g * 0.08) for b, g in zip(background, grid))


def resample(image, size):
    """Smoothly resize original raster; modest sharpening helps small glyphs."""
    if image.size == size:
        return image.copy()
    result = image.resize(size, Image.Resampling.LANCZOS)
    if size[0] > image.width or size[1] > image.height:
        result = result.filter(ImageFilter.UnsharpMask(radius=1.0, percent=65, threshold=3))
    return result
