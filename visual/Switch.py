import copy
from abc import abstractmethod

from shared_utility import deepcopy_args
from visual.template_point import TemplatePoint


class Switch:
    def __init__(self, target_point: TemplatePoint, assembly_template):
        self.target_point = target_point
        self.assembly_template = assembly_template

    def get_point(self):
        return self.do_switch(self.target_point)

    @abstractmethod
    @deepcopy_args()
    def do_switch(self, point: TemplatePoint):
        return point

    def is_point_targeted(self, point: TemplatePoint):
        return point is self.target_point

    def related_to_point(self, point: TemplatePoint):
        """
        Checks whether if the switch uses the point for get_point.
        For example, Redirect.related_to_point will return True if the given point is the target_point or the destination
        of the redirect.
        """
        return point is self.target_point

    def is_fair(self):
        """
        Returns whether the effects of the switch are clear.
        """
        raise NotImplementedError(f'{self.__class__} did not implement "is_fair".')
