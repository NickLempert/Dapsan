from typing import Iterator


def expand4(func):
    def __helper__(*args, **kwargs):
        expand = kwargs.get('expand')
        if expand is None:
            expand = 1
        else:
            del kwargs['expand']
        out = func(*args, **kwargs)
        return *map(lambda v: v-expand, out[:2]), *map(lambda v: v+expand, out[2:])
    return __helper__


class Renderable:
    @expand4
    def get_bounding_box(self) -> tuple[float, float, float, float]:
        raise NotImplementedError()

    def get_value(self, x: float, y: float) -> bool:
        raise NotImplementedError()

    def get_positions(self, resolution: tuple[int, int]) -> Iterator[tuple[int, int]]:
        raise NotImplementedError()

    def refresh(self):
        pass

