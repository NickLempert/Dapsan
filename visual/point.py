

class Point:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __getitem__(self, item):
        match item:
            case 0:
                return self.x
            case 1:
                return self.y
            case 'x':
                return self.x
            case 'y':
                return self.y
            case 'X':
                return self.x
            case 'Y':
                return self.y

        raise KeyError(f"{item} is not a property of Point.")

    def __setitem__(self, key, value):
        match key:
            case 0:
                self.x = value
            case 1:
                self.y = value
            case 'x':
                self.x = value
            case 'y':
                self.y = value
            case 'X':
                self.x = value
            case 'Y':
                self.y = value
        raise KeyError(f"{key} is not a property of Point.")

    def __iter__(self):
        yield self.x
        yield self.y

    def __str__(self):
        return f'({self.x} {self.y})'

