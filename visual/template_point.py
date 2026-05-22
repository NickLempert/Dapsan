from visual.point import Point
from visual.transforms import Transforms, XShift, YShift


class TemplatePoint(Point):
    def __init__(self, transforms: Transforms):
        super().__init__(transforms[XShift], transforms[YShift])
        self.transforms = transforms

