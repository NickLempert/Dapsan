import math
import random

from following_instructions.random_samples import get_random_word


class Product:
    name = 'product'
    difficulty_limit = 2.0

    def __init__(self, val: str = ''):
        self.text = val

    @staticmethod
    def generate(difficulty: float = 1.0):
        return Product('product')

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)

    def get_weight(self):
        return len(self)


class Word(Product):
    name = 'word'

    @staticmethod
    def generate(difficulty: float = 1.0):
        return Word(get_random_word())


class Number(Product):
    name = 'number'

    def __init__(self, val: str | int):
        super().__init__(str(val))

    @staticmethod
    def generate(difficulty: float = 1.0):
        min_num = int('1'+'0'*math.ceil(difficulty*5-1))
        max_num = int('9'*math.ceil(difficulty*5))
        return Number(random.randint(min_num, max_num))

    def get_weight(self):
        return int(self.text)


class Digit(Number):
    name = 'digit'

    @staticmethod
    def generate(difficulty: float = 1.0):
        return Digit(random.randint(0, 9))


PRODUCTS = [Word, Number, Digit]


if __name__ == '__main__':
    print(Product.generate())
    print(Word.generate())
    print(Number.generate())
    print(Number.generate(2))
    print(Number.generate(2))
    print(Number.generate(2))
