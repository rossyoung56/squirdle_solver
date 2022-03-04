import itertools
import math

import numpy as np


def filter_dex(dex: np.recarray, guess: np.record,
               gen_operation: int, type_1_operation: int, type_2_operation: int,
               height_operation: int, weight_operation: int) -> np.recarray:
    gen_filter = dex.generation == guess.generation
    if gen_operation == 1:
        gen_filter = dex.generation > guess.generation
    elif gen_operation == -1:
        gen_filter = dex.generation < guess.generation

    type_1_filter = dex.type_1 == guess.type_1
    if type_1_operation == 1:
        type_1_filter = dex.type_1 == guess.type_2
    elif type_1_operation == -1:
        type_1_filter = (dex.type_1 != guess.type_1) & (dex.type_1 != guess.type_2)

    type_2_filter = dex.type_2 == guess.type_2
    if type_2_operation == 1:
        type_2_filter = dex.type_2 == guess.type_1
    elif type_2_operation == -1:
        type_2_filter = (dex.type_2 != guess.type_2) & (dex.type_2 != guess.type_1)

    height_filter = dex.height_m == guess.height_m
    if height_operation == 1:
        height_filter = dex.height_m > guess.height_m
    elif height_operation == -1:
        height_filter = dex.height_m < guess.height_m

    weight_filter = dex.weight_kg == guess.weight_kg
    if weight_operation == 1:
        weight_filter = dex.weight_kg > guess.weight_kg
    elif weight_operation == -1:
        weight_filter = dex.weight_kg < guess.weight_kg

    return dex[gen_filter & type_1_filter & type_2_filter & height_filter & weight_filter]


def main() -> None:
    dex = np.recfromcsv('resources/pokedex.csv', encoding='utf-8')
    dex = dex[dex.generation == 3]
    total = dex.size
    entropies = []
    for guess in dex:
        entropy = 0
        for permutation in itertools.product([-1, 0, 1], repeat=5):
            filtered_dex = filter_dex(dex, guess, *permutation)
            p = filtered_dex.size / total
            information = math.log2(1 / p) if p > 0 else 0
            entropy += p * information
        entropies.append((guess.name, entropy))

    print(sorted(entropies, key=lambda entry: entry[1], reverse=True), sep='\n')


if __name__ == '__main__':
    main()
