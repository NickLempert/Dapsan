import copy
from typing import Type

from visual.point import Point
from visual.shapes import Shape
from visual.transforms import Transforms, XShift, YShift


class TemplatePoint(Point):
    def __init__(self, transforms: Transforms, active=True):
        super().__init__(transforms[XShift].amount, transforms[YShift].amount)
        self.transforms = transforms
        self.active = active

    def get_shape(self, shape: Type[Shape] | Shape):
        if isinstance(shape, Shape):
            shape2 = copy.deepcopy(shape)
            shape2.transforms = self.transforms
            return shape2
        return shape(transforms=self.transforms)
