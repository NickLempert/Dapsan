import math

UNITS_PER_IMAGE = 35


def px_to_unit(*vals, resolution):
    # return x/resolution*UNITS_PER_IMAGE, y/resolution*UNITS_PER_IMAGE
    return tuple(map(lambda val: val/resolution*UNITS_PER_IMAGE, vals))


def unit_to_px(*vals, resolution):
    # return round(x*resolution/UNITS_PER_IMAGE), round(y*resolution/UNITS_PER_IMAGE)
    return tuple(map(lambda val: round(val*resolution/UNITS_PER_IMAGE), vals))


def sign(val):
    return -1 if val < 0 else 1


def get_angle(x, y):
    return math.atan2(y, x)


def from_angle(angle, distance=1.0):
    return math.cos(angle) * distance, math.sin(angle) * distance
