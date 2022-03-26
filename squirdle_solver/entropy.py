import itertools
import math
from util import function_time

import numpy as np


@function_time
def filter_dex(dex: np.recarray, guess: np.record,
               gen_operation: int, type_1_operation: int, type_2_operation: int,
               height_operation: int, weight_operation: int) -> np.recarray:
    """
    Takes a given guess Pokemon and filters the dex using the provided operations in relation to the guess Pokemon's
    attributes
    :param dex: array of Pokemon entries to filter
    :param guess: guess Pokemon
    :param gen_operation:
    :param type_1_operation:
    :param type_2_operation:
    :param height_operation:
    :param weight_operation:
    :return: filtered dex containing only Pokemon which satisfy the operations in relation to the guess Pokemon
    """
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


@function_time
def calculate_entropy(dex: np.recarray, guess: np.record) -> float:
    total = dex.size
    entropy = 0
    for permutation in itertools.product([-1, 0, 1], repeat=5):
        filtered_dex = filter_dex(dex, guess, *permutation)
        p = filtered_dex.size / total
        information = math.log2(1 / p) if p > 0 else 0
        entropy += p * information

    return entropy


@function_time
def select_guess(dex: np.recarray) -> np.record:
    max_entropy = -1
    max_entropy_guess = None
    for guess in dex:
        entropy = calculate_entropy(dex, guess)
        if max_entropy < 0 or entropy > max_entropy:
            max_entropy = entropy
            max_entropy_guess = guess

    return max_entropy_guess


def main() -> None:
    dex = np.recfromcsv('resources/pokedex.csv', encoding='utf-8')
    # dex = dex[dex.generation == 3]
    # entropies = []
    # for guess in dex:
    #     entropy = calculate_entropy(dex, guess)
    #     entropies.append((guess.name, entropy))
    #
    # print(sorted(entropies, key=lambda entry: entry[1], reverse=True), sep='\n')

    print(select_guess(dex))


if __name__ == '__main__':
    main()
