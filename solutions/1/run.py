from solutions.get_inputs import read_inputs


def run_1(inputs):
    total = 0
    for line in inputs:
        first, last = _get_first_and_last(line.strip())
        total += first * 10 + last
    return total


def _get_first_and_last(line):
    first, last = None, None
    i = 0
    while first is None:
        char = line[i]
        if char.isdigit():
            first = int(char)
        i += 1
    i = len(line) - 1
    while last is None:
        char = line[i]
        if char.isdigit():
            last = int(char)
        i -= 1

    return first, last


def run_2(inputs):
    total = 0
    for line in inputs:
        first, last = _get_first_and_last_with_words(line.strip())
        total += first * 10 + last
    return total


WORD_TO_VAL = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def _get_first_and_last_with_words(line):
    first, last = None, None
    i = 0
    while first is None:
        char = line[i]
        if char.isdigit():
            first = int(char)
        else:
            word = line[i:i+5]
            val = val_from_word(word)
            if val is not None:
                first = val
        i += 1
    i = len(line) - 1
    while last is None:
        char = line[i]
        if char.isdigit():
            last = int(char)
        else:
            word = line[max(i-4,0):i+1]
            val = val_from_word_reverse(word)
            if val is not None:
                last = val
        i -= 1
    return first, last


def val_from_word(word):
    if word in WORD_TO_VAL:
        return WORD_TO_VAL[word]
    elif word[:-1] in WORD_TO_VAL:
        return WORD_TO_VAL[word[:-1]]
    elif word[:-2] in WORD_TO_VAL:
        return WORD_TO_VAL[word[:-2]]
    return None


def val_from_word_reverse(word):
    if word in WORD_TO_VAL:
        return WORD_TO_VAL[word]
    elif word[1:] in WORD_TO_VAL:
        return WORD_TO_VAL[word[1:]]
    elif word[2:] in WORD_TO_VAL:
        return WORD_TO_VAL[word[2:]]
    return None


def run_tests():
    test_inputs = """
    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 142:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    test_inputs = """
        two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 281:
        raise Exception(f"Test 2 did not pass, got {result_2}")

    test_input = "2sixnbvpfrdvcctmdzxl"
    result_3 = _get_first_and_last_with_words(test_input)
    if result_3 != (2, 6):
        raise Exception(f"Test 3 did not pass, got {result_3}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(1)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    # 52841 too high
    print(f"Finished 2 with result {result_2}")
