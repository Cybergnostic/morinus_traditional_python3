"""Non-destructive visibility for multiwheel chart slots.

Slots are permanent assignments (original inner, rings 1–3). Display
layers are the selected subset, in order; the first enabled slot becomes
the visible centre. Never change a source picker to hide a chart.
"""


def visible_slot_indices(slot_count, flags):
    """Return selected visible slot indexes, requiring two or more."""
    if not 2 <= slot_count <= 4:
        raise ValueError("Multiwheel must contain 2–4 chart slots")
    if len(flags) < slot_count:
        raise ValueError("One visibility flag per active slot is required")
    indices = tuple(i for i in range(slot_count) if bool(flags[i]))
    if len(indices) < 2:
        raise ValueError("At least two chart layers must remain visible")
    return indices


def displayed_charts(slots, visible):
    if len(visible) < 2:
        raise ValueError("A multiwheel needs at least two visible charts")
    return slots[visible[0]], [slots[i] for i in visible[1:]]


def remap_highlights(data, visible):
    """Copy highlight rows with display ring numbers (0=center)."""
    remap = {slot: ring for ring, slot in enumerate(visible)}
    result = dict(data)
    for field in ("marks", "areas"):
        result[field] = [
            dict(entry, ring=remap[entry["ring"]])
            for entry in data[field] if entry["ring"] in remap]
    # The legend describes the chart's time lords globally and its entries
    # have no ring key. Keep those unchanged even if radix is temporarily
    # omitted from the rendered bands.
    result["legend"] = [dict(item) for item in data["legend"]]
    return result


def aspect_ring(target_slot, visible):
    """Map a source-slot selection to the current drawn wheel.

    -1 disables lines, 0 draws only the visible centre, and positive
    slots refer to originally assigned ring slots (not display indices).
    """
    if target_slot == -1:
        return -1
    if target_slot == 0:
        return 0
    return visible.index(target_slot) if target_slot in visible[1:] else -1
