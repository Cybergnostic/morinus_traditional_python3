"""Offline IANA time-zone lookup for Morinus's separate standard offset and DST fields."""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class TimezoneLookupError(ValueError):
    pass


def resolve_timezone(year, month, day, hour, minute, second, latitude, longitude):
    """Return (zone_name, standard_utc_minutes, dst, warning).

    Morinus subtracts a separate one-hour DST flag, so do NOT enter the
    full summer UTC offset in its GMT fields. DST that is not one hour is
    folded into the standard offset with the flag off.
    """
    try:
        from timezonefinder import TimezoneFinder
    except ImportError as exc:
        raise TimezoneLookupError(
            "Install timezonefinder (pip install -r requirements.txt)."
        ) from exc
    try:
        name = TimezoneFinder(in_memory=True).timezone_at(lat=latitude, lng=longitude)
    except (ValueError, TypeError) as exc:
        raise TimezoneLookupError("Invalid latitude/longitude.") from exc
    if not name:
        raise TimezoneLookupError("No IANA time zone for these coordinates.")
    try:
        zone = ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise TimezoneLookupError(
            "IANA time-zone data unavailable. Install tzdata."
        ) from exc
    try:
        naive = datetime(year, month, day, hour, minute, second)
    except ValueError as exc:
        raise TimezoneLookupError(str(exc)) from exc
    candidates = []
    for fold in (0, 1):
        local = naive.replace(tzinfo=zone, fold=fold)
        offset, dst = local.utcoffset(), local.dst()
        if offset is None or dst is None:
            raise TimezoneLookupError("Unable to calculate the historical offset.")
        # Round-trip through UTC to detect nonexistent spring-forward times.
        roundtrip = local.astimezone(timezone.utc).astimezone(zone)
        if roundtrip.replace(tzinfo=None) == naive:
            candidates.append((offset, dst))
    if not candidates:
        raise TimezoneLookupError(
            "This local time did not exist during a daylight-saving change."
        )
    if len(set(candidates)) > 1:
        raise TimezoneLookupError(
            "This local time occurs twice during a clock change. "
            "Enter the correct GMT offset and DST setting manually."
        )
    offset, dst = candidates[0]
    notes = []
    if dst not in (timedelta(0), timedelta(hours=1)):
        # Morinus's DST checkbox is always one hour; enter the whole offset
        # (Irish winter time, which IANA counts as negative DST, ends up here).
        dst = timedelta(0)
        notes.append("Daylight saving here is not one hour; the total "
                     "offset is entered with DST unchecked.")
    standard = offset - dst
    seconds = standard.total_seconds()
    if seconds % 60:
        raise TimezoneLookupError(
            "Historical offset contains seconds; Morinus accepts only minutes. "
            "Enter a researched approximation manually."
        )
    minutes = int(seconds // 60)
    if abs(minutes) > 12 * 60:
        raise TimezoneLookupError(
            "UTC offset exceeds Morinus's 12-hour field limit; enter it manually."
        )
    if name.startswith("Etc/"):
        notes.append("No country time zone here (at sea); nautical time assumed.")
    if year < 1970:
        notes.append("Historical time-zone rules before 1970 may be incomplete. "
                     "Confirm against a historical atlas.")
    return name, minutes, dst != timedelta(0), " ".join(notes)
