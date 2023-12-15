from solutions.get_inputs import read_inputs


def run_1(inputs):
    return run(inputs)


def run_2(inputs):
    lines = []
    for line in inputs:
        sequence = line.strip().split(' ')[0].strip()
        new_sequence = '?'.join([sequence]*5)
        frequencies = line.strip().split(' ')[1].strip()
        new_frequencies = ','.join([frequencies]*5)
        lines.append(f'{new_sequence} {new_frequencies}')
    return run(lines)


def run(lines):
    result = 0
    i = 0
    for line in lines:
        sequence = line.strip().split(' ')[0].strip()
        frequencies = [int(i) for i in line.strip().split(' ')[1].split(',')]
        # import pdb; pdb.set_trace()
        result += num_possible(sequence, frequencies)
        i += 1
        print(i, result)
    return result


def num_possible(original_sequence, frequencies):
    valid_sequences = []
    tried_sequences = set()

    queue = [original_sequence]
    while queue:
        sequence = queue.pop(0)
        tried_sequences.add(sequence)
        # print(sequence)
        print(len(tried_sequences))
        # import pdb; pdb.set_trace()
        if '?' not in sequence:
            if is_valid(sequence, frequencies):
                valid_sequences.append(sequence)
        else:
            for i, value in enumerate(sequence):
                if value == '?':
                    new_broken = ''.join(val if j != i else '#' for j, val in enumerate(sequence))
                    new_working = ''.join(val if j != i else '.' for j, val in enumerate(sequence))
                    if new_broken not in tried_sequences:
                        queue.append(new_broken)
                    if new_working not in tried_sequences:
                        queue.append(new_working)
                    break
    # print(valid_sequences)
    return len(valid_sequences)


def is_valid(sequence, frequencies):
    counted_frequencies = []
    # if sequence == '.###........':
    #     import pdb; pdb.set_trace()
    i = 0
    frequency_to_check = 0
    for value in sequence:
        if value == '.':
            if i > 0:
                # if i != frequencies[frequency_to_check]:
                #     return False
                # frequency_to_check += 1
                counted_frequencies.append(i)
                i = 0
        else:
            # if frequency_to_check == len(frequencies):
            #     return False
            i += 1
    # if frequency_to_check != len(frequencies)-1:
    #     return False
    # if i > 0:
    #     return i == frequencies[frequency_to_check]
    # return True
    if i > 0:
        counted_frequencies.append(i)
    return counted_frequencies == frequencies


def run_tests():
    test_inputs = """
    ???.### 1,1,3
    .??..??...?##. 1,1,3
    ?#?#?#?#?#?#?#? 1,3,1,6
    ????.#...#... 4,1,1
    ????.######..#####. 1,6,5
    ?###???????? 3,2,1
    """.strip().split('\n')

    result = num_possible('???.###', [1, 1, 3])
    if result != 1:
        raise Exception(f"Test 0.1 did not pass, got {result}")

    result = num_possible('.??..??...?##.', [1, 1, 3])
    if result != 4:
        raise Exception(f"Test 0.2 did not pass, got {result}")

    result = num_possible('?###????????', [3, 2, 1])
    if result != 10:
        raise Exception(f"Test 0.3 did not pass, got {result}")

    result_1 = run_1(test_inputs)
    if result_1 != 21:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 525152:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(12)

    # result_1 = run_1(input)
    # print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
