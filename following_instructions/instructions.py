import random
from abc import abstractmethod
from typing import Type, Sequence

from following_instructions.products import Product, Number, Word, Digit
from following_instructions.utils import multiple_choice


class Instruction:
    input_products: Sequence[Type[Product]] = [Product]
    output_product: Type[Product] = Product

    def __init__(self):
        pass

    def __call__(self, product: Product):
        return Product(product.text)

    def __str__(self):
        return 'do nothing'

    @abstractmethod
    def difficulty_for_product(self, product: Product):
        return 0.1

    def supports_input_product(self, product: Product):
        return any(map(lambda t: isinstance(product, t), self.input_products))


class CountLetters(Instruction):
    input_products = [Word]
    output_product = Number

    def __init__(self):
        super().__init__()

    def __call__(self, product: Word):
        return Number(len(product))

    def difficulty_for_product(self, product: Word):
        return len(product.text) / 5

    def __str__(self):
        return f'count letters in'


class CountDigits(Instruction):
    input_products = [Number]
    output_product = Number

    def __init__(self):
        super().__init__()

    def __call__(self, product: Word):
        return Number(len(product))

    def __str__(self):
        return f'count digits in'

    def difficulty_for_product(self, product: Product):
        return len(product.text) / 4

    def supports_input_product(self, product: Word):
        return super().supports_input_product(product) and self(product).text != '1'


class GetWordWithLetterCount(Instruction):
    input_products = [Number, Digit]
    output_product = Word

    def __init__(self):
        super().__init__()
        self.words = [Word.generate() for _ in range(5)]

    def __call__(self, product: Word):
        return list(filter(lambda word: len(word) == product.get_weight(), self.words))[0]

    def __str__(self):
        return f'given the words:\n {multiple_choice(list(map(str, self.words)))}\n' \
               f'Take the first word where the length is'

    def supports_input_product(self, product: Product):
        # print(product, self.words)
        # print(super().supports_input_product(product) and (product.get_weight() in map(len, self.words)))
        return super().supports_input_product(product) and (product.get_weight() in map(len, self.words))

    def difficulty_for_product(self, product: Number):
        return int(product.get_weight()) / 3


class SelectWordWithLetterCount(GetWordWithLetterCount):
    output_product = Digit

    def __call__(self, product: Word):
        return list(map(lambda word: len(word) == product.get_weight(), self.words)).index(True) + 1

    def __str__(self):
        return f'given the words:\n {multiple_choice(list(map(str, self.words)))}\n' \
               f'Take the digit before the first word where the length is'


class FirstLetterIndex(Instruction):
    input_products = [Word]
    output_product = Number

    def __call__(self, product: Word):
        return ord(product.text[0].lower()) - ord('a') + 1

    def difficulty_for_product(self, product: Word):
        return (self(product) + 14) / 15

    def __str__(self):
        return 'return the place in the alphabet of the first letter of'


class FirstLetterIndexMatches(Instruction):
    input_products = [Digit, Number]
    output_product = Digit

    def __init__(self):
        super().__init__()
        self.words = [Word.generate() for _ in range(5)]

    def __call__(self, product: Number):
        matching = list(map(lambda word: ord(word.text[0]) - ord('a') + 1 == product.get_weight(), self.words))
        if any(matching):
            return Number(matching.index(True) + 1)
        return Number(-1)

    def difficulty_for_product(self, product: Number):
        return (int(product.text) + 14) / 15

    def supports_input_product(self, product: Number):
        return super().supports_input_product(product) and self(product).text != '-1'

    def __str__(self):
        return f'given the words:\n {multiple_choice(list(map(str, self.words)))}\n' \
               f'Take the digit before word with the first letter matching'


INSTRUCTIONS = [
    CountDigits,
    CountLetters,
    GetWordWithLetterCount,
    SelectWordWithLetterCount,
    FirstLetterIndex,
    FirstLetterIndexMatches
]
