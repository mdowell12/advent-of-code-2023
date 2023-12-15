from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D

def run_1(inputs):
    grids = parse_grids(inputs)
    result = 0
    for g in grids:
        left_of_vertical, above_horizontal = find_reflections(g)
        # print(g)
        # print(left_of_vertical, above_horizontal)
        # print()
        result += left_of_vertical + 100 * above_horizontal
    return result


def run_2(inputs):
    grids = parse_grids(inputs)
    result = 0
    for g in grids:
        left_of_vertical, above_horizontal = find_reflections_2(g)
        print(g)
        print(left_of_vertical, above_horizontal)
        print()
        result += left_of_vertical + 100 * above_horizontal
    return result


def find_reflections(grid):
    columns = [[grid.value_at_position((x,y)) for y in range(grid.max_y+1)] for x in range(grid.max_x+1)]
    rows = [[grid.value_at_position((x,y)) for x in range(grid.max_x+1)] for y in range(grid.max_y+1)]

    previous_column = columns[0]
    vertical_reflection_point = None
    num_left_of_vertical = 0
    for i in range(1, grid.max_x+1):
        column = columns[i]
        if previous_column == column:
            vertical_reflection_point = i-1
            size = get_size_of_reflection(columns, vertical_reflection_point)
            if size is not None:
                num_left_of_vertical = vertical_reflection_point+1
                break
        previous_column = column

    previous_row = rows[0]
    horizontal_reflection_point = None
    num_above_horizontal = 0
    for i in range(1, grid.max_y+1):
        row = rows[i]
        if previous_row == row:
            horizontal_reflection_point = i-1
            size = get_size_of_reflection(rows, horizontal_reflection_point)
            if size is not None:
                num_above_horizontal = horizontal_reflection_point+1
                break
        previous_row = row

    return num_left_of_vertical, num_above_horizontal


def find_reflections_2(grid):
    columns = [[grid.value_at_position((x,y)) for y in range(grid.max_y+1)] for x in range(grid.max_x+1)]
    rows = [[grid.value_at_position((x,y)) for x in range(grid.max_x+1)] for y in range(grid.max_y+1)]

    previous_column = columns[0]
    vertical_reflection_point = None
    num_left_of_vertical = 0
    for i in range(1, grid.max_x+1):
        column = columns[i]
        if distance(previous_column, column) == 1:
            vertical_reflection_point = i-1
            size = get_size_of_reflection(columns, vertical_reflection_point)
            if size is not None:
                num_left_of_vertical = vertical_reflection_point+1
                break
        previous_column = column

    previous_row = rows[0]
    horizontal_reflection_point = None
    num_above_horizontal = 0
    for i in range(1, grid.max_y+1):
        row = rows[i]
        if distance(previous_row, row) == 1:
            horizontal_reflection_point = i-1
            size = get_size_of_reflection(rows, horizontal_reflection_point)
            if size is not None:
                num_above_horizontal = horizontal_reflection_point+1
                break
        previous_row = row

    return num_left_of_vertical, num_above_horizontal


def distance(left, right):
    result = 0
    for i in range(len(left)):
        if left[i] != right[i]:
            result += 1
        if result > 1:
            return result
    return result



def get_size_of_reflection(rows, horizontal_reflection_point):
    i = 0
    left, right = rows[horizontal_reflection_point], rows[horizontal_reflection_point+1]
    while (horizontal_reflection_point-i) > 0 and (horizontal_reflection_point+1+i) < len(rows)-1 and left == right:
        i += 1
        left, right = rows[horizontal_reflection_point-i], rows[horizontal_reflection_point+1+i]

    if (horizontal_reflection_point + i + 1 == len(rows)-1 or horizontal_reflection_point - i == 0) and left == right:
        return i
    return None


def parse_grids(inputs):
    grids = []
    lines = []
    for line in inputs:
        if line.strip():
            lines.append(line.strip())
        else:
            grids.append(Grid2D(lines))
            lines = []
    if lines:
        grids.append(Grid2D(lines))
    return grids




def run_tests():
    test_inputs = """
    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.

    #...##..#
    #....#..#
    ..##..###
    #####.##.
    #####.##.
    ..##..###
    #....#..#
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 405:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 400:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(13)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
