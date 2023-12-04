from math import prod

from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


def run_1(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    special_chars = set(position for position, value in grid if value != '.' and not value.isdigit())
    part_numbers = []
    current_number = []
    current_number_is_adjacent = False
    for (x, y), value in grid:
        if not value.isdigit():
            if current_number and current_number_is_adjacent:
                part_numbers.append(int(''.join(current_number)))
            current_number, current_number_is_adjacent = [], False
        else:
            current_number.append(value)
            if _is_next_to_special_char(x, y, special_chars):
                current_number_is_adjacent = True
        if x == grid.max_x:
            if current_number and current_number_is_adjacent:
                part_numbers.append(int(''.join(current_number)))
            current_number, current_number_is_adjacent = [], False
    return sum(part_numbers)


def _is_next_to_special_char(x, y, special_chars):
    return (x-1, y) in special_chars or (x+1, y) in special_chars or (x-1, y+1) in special_chars or (x, y+1) in special_chars or (x+1, y+1) in special_chars or (x-1, y-1) in special_chars or (x, y-1) in special_chars or (x+1, y-1) in special_chars


def run_2(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    stars_to_adjacent_numbers = {position: set() for position, value in grid if value == '*'}
    current_number = []
    adjacent_stars = set()
    for (x, y), value in grid:
        if not value.isdigit():
            if current_number and adjacent_stars:
                for star in adjacent_stars:
                    stars_to_adjacent_numbers[star].add(int(''.join(current_number)))
            current_number, adjacent_stars = [], set()
        else:
            current_number.append(value)
            adjacent_stars = adjacent_stars.union(_find_adjacent_stars(x, y, stars_to_adjacent_numbers.keys()))
        if x == grid.max_x:
            for star in adjacent_stars:
                stars_to_adjacent_numbers[star].add(int(''.join(current_number)))
            current_number, adjacent_stars = [], set()

    result = 0
    for adjacents in stars_to_adjacent_numbers.values():
        if len(adjacents) == 2:
            result += prod(adjacents)
    return result


def _find_adjacent_stars(x, y, stars):
    result = set()
    for star in stars:
        if (x-1, y) == star or (x+1, y) == star or (x-1, y+1) == star or (x, y+1) == star or (x+1, y+1) == star or (x-1, y-1) == star or (x, y-1) == star or (x+1, y-1) == star:
            result.add(star)
    return result


def run_tests():
    test_inputs = """
    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 4361:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 467835:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(3)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
