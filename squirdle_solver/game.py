import random
from typing import Tuple
import numpy as np
import colorama
from colorama import Fore


GEN, TYPE1, TYPE2, HEIGHT, WEIGHT = 0, 1, 2, 3, 4


def play(filename: str, encoding: str) -> int:
    colorama.init()
    dex = np.recfromcsv(filename, encoding=encoding)
    solution = pick_solution(dex)
    attempts = 8
    while attempts > 0:
        guess = input('Guess a Pokemon: ')
        guess_item = dex[dex.name == guess]
        if len(guess_item) < 1:
            print('Invalid Pokemon')
            continue

        guess_item = guess_item[0]
        print('Generation Type_1 Type_2 Height(m) Weight(kg)')
        for i in range(1, len(guess_item)):
            print(guess_item[i], end=' ')
        print()
        result = check_guess(dex, solution, guess_item)
        print_result(result, guess_item.type_1, guess_item.type_2)
        if min(result) == 0 and max(result) == 0:
            print('You win!')
            return 8 - attempts

        attempts -= 1

    print('You lose! The answer was: ' + solution)
    return 0


def pick_solution(dex: np.recarray) -> np.record:
    return dex[random.randint(0, len(dex))]


def check_guess(dex: np.recarray, solution: np.record, guess: np.record) -> Tuple[int, int, int, int, int]:
    solution_item = dex[dex.name == solution.name][0]
    guess_item = dex[dex.name == guess.name][0]
    result = [0, -1, -1, 0, 0]

    if solution_item.generation > guess_item.generation:
        result[GEN] = 1
    elif solution_item.generation < guess_item.generation:
        result[GEN] = -1

    if guess_item.type_1 == solution_item.type_1:
        result[TYPE1] = 0
    elif guess_item.type_1 == solution_item.type_2:
        result[TYPE1] = 1

    if guess_item.type_2 == solution_item.type_2:
        result[TYPE2] = 0
    elif guess_item.type_2 == solution_item.type_1:
        result[TYPE2] = 1

    if solution_item.height_m > guess_item.height_m:
        result[HEIGHT] = 1
    elif solution_item.height_m < guess_item.height_m:
        result[HEIGHT] = -1

    if solution_item.weight_kg > guess_item.weight_kg:
        result[WEIGHT] = 1
    elif solution_item.weight_kg < guess_item.weight_kg:
        result[WEIGHT] = -1

    return tuple(result)


def print_result(result: Tuple[int, int, int, int, int], type_1: str, type_2: str) -> None:
    output = Fore.RESET

    if result[GEN] == 1:
        output += 'Higher'
    elif result[GEN] == -1:
        output += 'Lower'
    else:
        output += Fore.GREEN + 'Correct'
    output += Fore.RESET + ' '

    if result[TYPE1] == 1:
        output += Fore.YELLOW
    elif result[TYPE1] == -1:
        output += Fore.RED
    else:
        output += Fore.GREEN
    output += type_1 + Fore.RESET + ' '

    if result[TYPE2] == 1:
        output += Fore.YELLOW
    elif result[TYPE2] == -1:
        output += Fore.RED
    else:
        output += Fore.GREEN
    output += type_2 + Fore.RESET + ' '

    if result[HEIGHT] == 1:
        output += 'Higher'
    elif result[HEIGHT] == -1:
        output += 'Lower'
    else:
        output += Fore.GREEN + 'Correct'
    output += Fore.RESET + ' '

    if result[WEIGHT] == 1:
        output += 'Higher'
    elif result[WEIGHT] == -1:
        output += 'Lower'
    else:
        output += Fore.GREEN + 'Correct'
    output += Fore.RESET

    print(output)
