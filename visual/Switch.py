import copy

from visual.template_point import TemplatePoint


class Switch:
    def __init__(self, target_point: TemplatePoint, assembly_template):
        self.target_point = target_point
        self.assembly_template = assembly_template

    def get_point(self):
        return copy.deepcopy(self.target_point)

    def related_to_point(self, point):
        """
        Checks whether if the switch uses the point for get_point.
        For example, Redirect.related_to_point will return True if the given point is the target_point or the destination
        of the redirect.
        """
        return point is self.target_point


