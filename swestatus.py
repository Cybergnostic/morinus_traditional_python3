"""Swiss Ephemeris return-flag compatibility for the Morinus C extension.

The bundled extension returns status as a one-element tuple, unlike some
other Swiss Ephemeris bindings which return a plain integer.
"""


def status_code(value):
    """Unwrap the return flag from sweastrology.swe_calc_ut."""
    if isinstance(value, (tuple, list)):
        if len(value) != 1:
            raise ValueError('Expected exactly one Swiss Ephemeris status code')
        value = value[0]
    if not isinstance(value, int):
        raise TypeError('Swiss Ephemeris status code must be an integer')
    return value
