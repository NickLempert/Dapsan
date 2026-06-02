import math
import random
from typing import Sequence, Callable

from following_instructions.random_samples import get_random_word, get_random_sentence
from following_instructions.utils import multiple_choice


class Product:
    name = 'product'
    difficulty_limit = 2.0
    auto_reveal = True
    refer_by_name = True

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

    def get_alphabetical_order(self):
        out = 0
        for index, order in enumerate(map(ord, self.text)):
            out += order / 10 ** index
        return out


class Text(Product):
    name = 'text'


class ProductCollection(Text):
    product_type = Product

    def __init__(self, text: str | Sequence[str] | Sequence[Product]):
        self.products = None
        if isinstance(text, Sequence):
            self.products = text
            if len(text) > 0 and isinstance(text[0], str):
                self.products = list(map(self.product_type, text))
            text = ' '.join(map(str, text))
            self.last_text_update = text
        super().__init__(text)

    def __len__(self):
        return len(self.get_products())

    def get_products(self):
        if self.products is None or self.last_text_update != self.text:
            self.products = list(map(self.product_type, self.text.split()))
            self.last_text_update = self.text
        return self.products

    @staticmethod
    def generate(difficulty: float = 1.0):
        return ProductCollection([Product(get_random_word()) for _ in range(5)])

    def get_multiple_choice(self):
        return multiple_choice(list(map(str, self.get_products())))

    def get_matching_product(self, check_product: Callable):
        for product in self.get_products():
            if check_product(product):
                return product
        return ''

    def find_matching_product(self, check_product: Callable):
        for index, product in enumerate(self.get_products()):
            if check_product(product):
                return index
        return -1

    def __iter__(self):
        return self.get_products().__iter__()


class Word(Text):
    name = 'word'

    @staticmethod
    def generate(difficulty: float = 1.0):
        return Word(get_random_word())


class WordCollection(ProductCollection):
    product_type = Word

    def __init__(self, text: str | Sequence[str | Word]):
        super().__init__(text)
        self.text = self.text.replace(',', '').replace('.', '').replace('!', '').replace('?', '')

    @staticmethod
    def generate(difficulty: float = 1.0):
        return WordCollection([Word.generate(difficulty) for _ in range(5)])


class Sentence(WordCollection):
    @staticmethod
    def generate(difficulty: float = 1.0):
        return Sentence(get_random_sentence())


class Number(Product):
    name = 'number'

    def __init__(self, val: str | int):
        super().__init__(str(val))

    @staticmethod
    def generate(difficulty: float | None = None):
        if difficulty is None:
            difficulty = random.uniform(0.2, 2)
        min_num = int('1' + '0' * math.ceil(difficulty * 5 - 1))
        max_num = int('9' * math.ceil(difficulty * 5))
        return Number(random.randint(min_num, max_num))

    def get_weight(self):
        return int(self.text)


class Digit(Number):
    name = 'digit'

    @staticmethod
    def generate(difficulty: float = 1.0):
        return Digit(random.randint(0, 9))


class NumberCollection(ProductCollection):
    product_type = Number

    def __init__(self, text: str | Sequence[int | Number]):
        super().__init__(text)

    @staticmethod
    def generate(difficulty: float | None = None):
        return NumberCollection([Number.generate(difficulty) for _ in range(4)])


class Property(Product):
    names = {'biggest': Product.get_weight,
             'smallest': lambda product: -product.get_weight(),
             'longest': len,
             'shortest': lambda product: -len(product),
             }
    name = 'property'
    auto_reveal = False
    refer_by_name = False

    def __init__(self, text: str = ''):
        super().__init__(text)

    def __call__(self, product: Product):
        # if self.names.get(self.text).__code__.co_argcount > 1:
        #     return self.names.get(self.text)(product, full_list)
        return self.names.get(self.text)(product)

    def get_product_from(self, products: Sequence[Product]):
        return max(products, key=self.names.get(self.text))

    @staticmethod
    def generate(difficulty: float = 1.0):
        return Property(random.choice(tuple(Property.names.keys())))


class WordProperty(Property):
    names = Property.names.copy()
    names.update({
        'first alphabetically': Product.get_alphabetical_order,
        'last alphabetically': lambda product: -product.get_alphabetical_order(),
    })

    @staticmethod
    def generate(difficulty: float = 1.0):
        return WordProperty(random.choice(list(WordProperty.names.keys())))


PRODUCTS = [Word, Number, Digit, Sentence, Property, WordProperty]

if __name__ == '__main__':
    print(Product.generate())
    print(Word.generate())
    print(Number.generate())
    print(Number.generate(2))
    print(Number.generate(2))
    print(Number.generate(2))
