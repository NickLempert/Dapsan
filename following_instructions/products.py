import math
import random
from typing import Sequence, Callable

from following_instructions.random_samples import get_random_word, get_random_sentence
from following_instructions.utils import multiple_choice


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


class Text(Product):
    name = 'text'


class Word(Text):
    name = 'word'

    @staticmethod
    def generate(difficulty: float = 1.0):
        return Word(get_random_word())


class WordCollection(Text):
    def __init__(self, text: str | Sequence[str] | Sequence[Word]):
        self.words = None
        if isinstance(text, Sequence):
            self.words = text
            if len(text) > 0 and isinstance(text[0], str):
                self.words = list(map(Word, text))
            text = ' '.join(map(str, text))
            self.last_text_update = text
        text = text.replace(',', '').replace('.', '').replace('!', '').replace('?', '')
        super().__init__(text)

    def get_words(self):
        if self.words is None or self.last_text_update != self.text:
            self.words = list(map(Word, self.text.split()))
            self.last_text_update = self.text
        return self.words

    @staticmethod
    def generate(difficulty: float = 1.0):
        return WordCollection([Word(get_random_word()) for _ in range(5)])

    def get_multiple_choice(self):
        return multiple_choice(list(map(str, self.get_words())))

    def get_matching_word(self, check_word: Callable):
        for word in self.get_words():
            if check_word(word):
                return word
        return ''

    def find_matching_word(self, check_word: Callable):
        for index, word in enumerate(self.get_words()):
            if check_word(word):
                return index
        return -1


class Sentence(WordCollection):
    @staticmethod
    def generate(difficulty: float = 1.0):
        return Sentence(get_random_sentence())


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


PRODUCTS = [Word, Number, Digit, Sentence]


if __name__ == '__main__':
    print(Product.generate())
    print(Word.generate())
    print(Number.generate())
    print(Number.generate(2))
    print(Number.generate(2))
    print(Number.generate(2))
