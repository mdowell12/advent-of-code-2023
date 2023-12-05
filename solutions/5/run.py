from solutions.get_inputs import read_inputs


MAP_NAMES = [
    'seed-to-soil',
    'soil-to-fertilizer',
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location',
]


class Map:

    def __init__(self, name, lines):
        self.name = name
        self.ranges = self._parse_lines(lines)

    def map(self, value):
        for start, end, target_start in self.ranges:
            if start <= value <= end:
                return target_start + (value - start)
        return value

    def _parse_lines(self, lines):
        result = []
        for line in lines:
            target_start, source_start, range = [int(i) for i in line.strip().split(' ')]
            result.append(tuple([source_start, source_start + range - 1, target_start]))
        return result

    def __repr__(self):
        return f'{self.name}: {self.ranges}'


def run_1(inputs):
    seeds = [int(i) for i in inputs[0].split(':')[-1].split(' ') if i]
    i = 1
    maps = {}
    for map_name in MAP_NAMES:
        maps[map_name] = _make_map(map_name, inputs)
    lowest = None
    for seed in seeds:
        mapped = _map_seed(seed, maps)
        if lowest is None or mapped < lowest:
            lowest = mapped
    return lowest


def run_2(inputs):
    maps = {}
    for map_name in MAP_NAMES:
        maps[map_name] = _make_map(map_name, inputs)
    parts = [int(i) for i in inputs[0].split(':')[-1].split(' ') if i]
    lowest = None
    i = 0
    while i < len(parts):
        result = _binary_search_seed_range(parts[i], parts[i]+parts[i+1]-1, maps)
        if lowest is None or result < lowest:
            lowest = result
        i += 2
    return lowest


def _binary_search_seed_range(lower_seed, higher_seed, maps):
    lower_mapped = _map_seed(lower_seed, maps)
    higher_mapped = _map_seed(higher_seed, maps)
    # If we found a contiguous segment, we do not need to evaluate the whole thing
    # Just take the lower_mapped value, because we know it will monotonically increase
    if (higher_mapped - lower_mapped) == (higher_seed - lower_seed):
        return lower_mapped
    # Otherwise, split the interval in two and recurse on both sides, keeping the smallest result
    mid_point = lower_seed + int((higher_seed - lower_seed) / 2)
    left_range_mapped = _binary_search_seed_range(lower_seed, mid_point, maps)
    right_range_mapped = _binary_search_seed_range(mid_point+1, higher_seed, maps)
    return min(left_range_mapped, right_range_mapped)


def _map_seed(seed, maps):
    result = seed
    for map_name in MAP_NAMES:
        result = maps[map_name].map(result)
    return result


def _make_map(map_name, inputs):
    for i, line in enumerate(inputs):
        if map_name in line:
            map_lines = []
            j = i + 1
            line = inputs[j].strip()
            while line:
                map_lines.append(line)
                j += 1
                line = inputs[j].strip() if j < len(inputs) else ''
            return Map(map_name, map_lines)
    raise Exception(f'No map for name {map_name}')


def run_tests():
    test_inputs = """
    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 35:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 46:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(5)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
