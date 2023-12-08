from math import lcm

from solutions.get_inputs import read_inputs


def run_1(inputs):
    directions = inputs[0].strip()
    map = _parse_map(inputs)
    return _num_steps_until_end('AAA', lambda x: x == 'ZZZ', map, directions)



def run_2(inputs):
    directions = inputs[0].strip()
    map = _parse_map(inputs)
    starts = [position for position in map.keys() if position.endswith('A')]
    cycle_lengths = []
    for start in starts:
        cycle_lengths.append(
            _num_steps_until_end(start, lambda x: x.endswith('Z'), map, directions)
        )
    return lcm(*cycle_lengths)


def _num_steps_until_end(start, is_end_fn, map, directions):
    i = 0
    position = start
    while not is_end_fn(position):
        direction = directions[i % len(directions)]
        left_or_right = 0 if direction == 'L' else 1
        position = map[position][left_or_right]
        i += 1
    return i


def _parse_map(inputs):
    map = {}
    for line in inputs[2:]:
        key = line.split('=')[0].strip()
        value = [i.strip() for i in line.split('=')[1].strip().replace('(', '').replace(')', '').split(',')]
        map[key] = value
    return map


def run_tests():
    test_inputs = """
    RL

    AAA = (BBB, CCC)
    BBB = (DDD, EEE)
    CCC = (ZZZ, GGG)
    DDD = (DDD, DDD)
    EEE = (EEE, EEE)
    GGG = (GGG, GGG)
    ZZZ = (ZZZ, ZZZ)
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 2:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    test_inputs = """
    LLR

    AAA = (BBB, BBB)
    BBB = (AAA, ZZZ)
    ZZZ = (ZZZ, ZZZ)
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 6:
        raise Exception(f"Test 1.2 did not pass, got {result_1}")

    test_inputs = """
    LR

    11A = (11B, XXX)
    11B = (XXX, 11Z)
    11Z = (11B, XXX)
    22A = (22B, XXX)
    22B = (22C, 22C)
    22C = (22Z, 22Z)
    22Z = (22B, 22B)
    XXX = (XXX, XXX)
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 6:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(8)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
