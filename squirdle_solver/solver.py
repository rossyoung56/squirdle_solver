import game
import entropy

import numpy as np


def solve(dex: np.recarray, solution: np.record) -> int:
    attempts = 8
    while attempts > 0:
        attempts -= 1

        guess = entropy.select_guess(dex)
        result = game.check_guess(dex, solution, guess)
        if min(result) == 0 and max(result) == 0:
            return 8 - attempts

        dex = entropy.filter_dex(dex, guess, *result)

    return -1


def main():
    dex = np.recfromcsv('resources/pokedex.csv', encoding='utf-8')
    distribution = {-1: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    for solution in dex:
        distribution[solve(dex, solution)] += 1
        print(distribution)

    print(distribution)


if __name__ == '__main__':
    main()
