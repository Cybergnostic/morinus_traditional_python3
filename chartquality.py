"""Output-space helpers for the Morinus natal and bi-wheel chart renderer.

High quality renders at twice the logical bitmap size and reduces it once.
No astrology or wheel coordinates are changed; hit testing converts from
display pixels to render pixels.
"""

HIGH = 'high'
STANDARD = 'standard'
MAX_RENDER_PIXELS = 12000000


def scale_for(size, quality):
    """Return 1 or 2, respecting a cap on temporary raster memory."""
    width, height = (max(1, int(v)) for v in size)
    if quality != HIGH or min(width, height) < 240:
        return 1
    return 2 if 4 * width * height <= MAX_RENDER_PIXELS else 1


def raster_size(size, scale):
    return tuple(max(1, int(v)) * scale for v in size)


def render_position(position, scale):
    """Scale a wx mouse position into the original drawn wheel's coordinates."""
    return (position[0] * scale, position[1] * scale)
