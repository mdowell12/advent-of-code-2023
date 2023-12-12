from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


def run_1(inputs):
    return run(inputs, 2)


def run_2(inputs, expansion_factor):
    return run(inputs, expansion_factor)


def run(inputs, expansion_factor):
    grid = Grid2D([i.strip() for i in inputs])
    galaxies = [(x, y) for (x, y), value in grid if value == '#']
    empty_columns = set([x for x in range(grid.max_x+1) if x not in set([i[0] for i in galaxies])])
    empty_rows = set([y for y in range(grid.max_y+1) if y not in set([i[1] for i in galaxies])])
    pairs = make_pairs(galaxies)

    result = 0
    for pair in pairs:
        result += distance(pair, empty_columns, empty_rows, expansion_factor)
    return result


def make_pairs(galaxies):
    queue = [i for i in galaxies]
    result = []
    while queue:
        first = queue.pop(0)
        for other in queue:
            result.append((first, other))
    return result


def distance(pair, empty_columns, empty_rows, expansion_factor):
    left, right = pair
    diff_x = abs(left[0] - right[0])
    for i in empty_columns:
        if min(left[0], right[0]) <= i <= max(left[0], right[0]):
            diff_x += 1 * expansion_factor - 1
    diff_y = abs(left[1] - right[1])
    for i in empty_rows:
        if min(left[1], right[1]) <= i <= max(left[1], right[1]):
            diff_y += 1 * expansion_factor - 1
    return diff_x + diff_y


def run_tests():
    test_inputs = """
    ...#......
    .......#..
    #.........
    ..........
    ......#...
    .#........
    .........#
    ..........
    .......#..
    #...#.....
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 374:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs, 10)
    if result_2 != 1030:
        raise Exception(f"Test 2 did not pass, got {result_2}")

    result_2 = run_2(test_inputs, 100)
    if result_2 != 8410:
        raise Exception(f"Test 2.1 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(11)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input, 1_000_000)
    print(f"Finished 2 with result {result_2}")
