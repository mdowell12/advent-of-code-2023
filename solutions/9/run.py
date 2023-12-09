from solutions.get_inputs import read_inputs


def run_1(inputs):
    sequences = [[int(j) for j in i.strip().split(' ')] for i in inputs]
    result = 0
    for sequence in sequences:
        prediction = _predict_sequence(sequence)
        result += prediction
    return result


def run_2(inputs):
    sequences = [[int(j) for j in i.strip().split(' ')] for i in inputs]
    result = 0
    for sequence in sequences:
        prediction = _predict_sequence_2(sequence)
        result += prediction
    return result


def _predict_sequence(sequence):
    diffs = _collect_diffs(sequence)
    result = 0
    for d in reversed(diffs[:-1]):
        result += d[-1]
    result += sequence[-1]
    return result


def _predict_sequence_2(sequence):
    diffs = _collect_diffs(sequence)
    result = 0
    for d in reversed(diffs[:-1]):
        result = d[0] - result
    result = sequence[0] - result
    return result


def _collect_diffs(sequence):
    diffs = [_make_diffs(sequence)]
    while any(i != 0 for i in diffs[-1]):
        diffs.append(_make_diffs(diffs[-1]))
    return diffs


def _make_diffs(sequence):
    result = []
    for i in range(len(sequence)-1):
        result.append(sequence[i+1] - sequence[i])
    return result


def run_tests():
    test_inputs = """
    0 3 6 9 12 15
    1 3 6 10 15 21
    10 13 16 21 30 45
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 114:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 2:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(9)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
