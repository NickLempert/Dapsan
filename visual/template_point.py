import copy
from typing import Type

from visual.effects import Effect
from visual.point import Point
from visual.shapes import Shape
from visual.transforms import Transforms, XShift, YShift, Rotation


class TemplatePoint(Point):
    def __init__(self, transforms: Transforms,
                 active=True,
                 edge_type: Effect = None,
                 background: Effect = None,
                 background_rotation: Rotation = None):
        super().__init__(transforms[XShift].amount, transforms[YShift].amount)
        self.transforms = transforms
        self.active = active
        self.edge_type = edge_type
        self.background = background
        self.background_rotation = background_rotation

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.transforms[XShift].amount = self.x
        self.transforms[YShift].amount = self.y

    def get_shape(self, shape: Type[Shape] | Shape):
        if isinstance(shape, Shape):
            shape2 = copy.deepcopy(shape)
            shape2.transforms = self.transforms
            if self.edge_type is not None:
                shape2.edge_type = self.edge_type
            if self.background is not None:
                shape2.background = self.background
            if self.background_rotation is not None:
                shape2.background_rotation = self.background_rotation
            return shape2
        return shape(transforms=self.transforms)
