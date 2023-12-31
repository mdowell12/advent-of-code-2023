from solutions.get_inputs import read_inputs


def run_1(inputs):
    steps = []
    for i in inputs:
        steps += [j.strip() for j in i.strip().split(',')]
    total = 0
    for step in steps:
        hash = run_hash(step)
        total += hash
    return total


def run_2(inputs):
    steps = []
    for i in inputs:
        steps += [j.strip() for j in i.strip().split(',')]

    map = {i: [] for i in range(256)}
    for step in steps:
        if '=' in step:
            label, value = step.split('=')
            remove = False
        elif '-' in step:
            label = step.replace('-', '')
            remove = True
        else:
            raise Exception(step)
        values = map[run_hash(label)]
        index, matched_value = matching(label, values)
        if remove:
            if index is not None:
                del values[index]
        else:
            if index is None:
                values.append((label, value))
            else:
                values[index] = (label, max(value, value))

    result = 0
    for box, values in map.items():
        for slot, (label, value) in enumerate(values):
            result += (box+1) * (slot+1) * int(value)
    return result


def matching(label, values):
    for i, (other_label, value) in enumerate(values):
        if label == other_label:
            return (i, value)
    return None, None


def run_hash(string):
    result = 0
    for char in string:
        ascii = ord(char)
        result += ascii
        result = result * 17
        result = result % 256
    return result


def run_tests():

    result_1 = run_hash("HASH")
    if result_1 != 52:
        raise Exception(f"Test 0.1 did not pass, got {result_1}")

    test_inputs = """
    rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 1320:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 145:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(15)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
