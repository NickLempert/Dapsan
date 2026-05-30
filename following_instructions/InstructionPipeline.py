from __future__ import annotations

import random

from following_instructions.instructions import Instruction, INSTRUCTIONS
from following_instructions.products import Product


class InstructionPipeline:
    def __init__(self, first_product: Product, instruction):
        self.first_product = first_product
        self.instruction = instruction
        self.next: InstructionPipeline | None = None

    def __call__(self):
        if self.next is None:
            return self.instruction(self.first_product)
        return self.next()

    def get_difficulty(self):
        out = self.instruction.difficulty_for_product(self.first_product)
        if self.next is not None:
            out += self.next.get_difficulty()
        return out

    @staticmethod
    def generate(difficulty: float = 5.0, product: Product | None = None):
        original_product = product
        out_pipeline = InstructionPipeline(Product.generate(), Instruction())
        for _ in range(100):
            if product is None:
                instruction = None
                while instruction is None or not instruction.supports_input_product(product):
                    instruction = random.choice(INSTRUCTIONS)()
                    product = random.choice(instruction.input_products).generate()
            else:
                candidates = list(map(lambda inst: inst(), INSTRUCTIONS))
                weights = list(map(lambda cand: cand.supports_input_product(product), candidates))
                if sum(weights) == 0:
                    return InstructionPipeline(product, Instruction())
                instruction = random.choices(candidates, weights=weights)[0]
            out_pipeline = InstructionPipeline(product, instruction)

            if difficulty - instruction.difficulty_for_product(product) <= 0:
                return out_pipeline
            out_pipeline.next = InstructionPipeline.generate(difficulty - instruction.difficulty_for_product(product),
                                                             out_pipeline())
            product = original_product
            if str(out_pipeline.next.instruction) == str(out_pipeline.instruction):
                continue
            if out_pipeline.get_difficulty() >= difficulty:
                break
        else:
            out_pipeline.next = None
        return out_pipeline

    def string_without_first_product(self, end_chain=False):
        return f'{self.instruction} the resulting {self.first_product.name}.\n' \
               f'{"" if end_chain or self.next is None else self.next.string_without_first_product()}'

    def __str__(self):
        return f'Given the {self.first_product.name}: {self.first_product.text}\n\n' \
               + self.string_without_first_product()


if __name__ == '__main__':
    test_p = InstructionPipeline.generate()
    print(' '.join(chr(i+ord('A')) for i in range(26)))
    print()
    print(test_p)
    input('reveal answer...')
    print(test_p())
