import math

UNITS_PER_IMAGE = 35
IMAGE_FIFTH = UNITS_PER_IMAGE / 5
IMAGE_THIRD = UNITS_PER_IMAGE / 3
IMAGE_HALF = UNITS_PER_IMAGE / 2


def px_to_unit(*vals, resolution):
    return tuple(map(lambda val: val/resolution*UNITS_PER_IMAGE, vals))


def unit_to_px(*vals, resolution):
    return tuple(map(lambda val: round(val*resolution/UNITS_PER_IMAGE), vals))


def sign(val):
    return -1 if val < 0 else 1


def get_angle(x, y):
    return math.atan2(y, x)


def from_angle(angle, distance=1.0):
    return math.cos(angle) * distance, math.sin(angle) * distance
