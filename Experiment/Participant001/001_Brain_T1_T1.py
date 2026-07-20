words = ["abcd","def","xyz"]
weights = {
    'a': 5,
    'b': 3,
    'c': 12,
    'd': 14,
    'e': 1,
    'f': 2,
    'g': 3,
    'h': 2,
    'i': 10,
    'j': 6,
    'k': 6,
    'l': 9,
    'm': 7,
    'n': 8,
    'o': 7,
    'p': 10,
    'q': 8,
    'r': 9,
    's': 6,
    't': 9,
    'u': 9,
    'v': 8,
    'w': 3,
    'x': 7,
    'y': 7,
    'z': 2,
}
weight_to_letter_map = {
    25: 'a',
    24: 'b',
    23: 'c',
    22: 'd',
    21: 'e',
    20: 'f',
    19: 'g',
    18: 'h',
    17: 'i',
    16: 'j',
    15: 'k',
    14: 'l',
    13: 'm',
    12: 'n',
    11: 'o',
    10: 'p',
    9: 'q',
    8: 'r',
    7: 's',
    6: 't',
    5: 'u',
    4: 'v',
    3: 'w',
    2: 'x',
    1: 'y',
    0: 'z',
}

final_result = ""

# Esqueci como converte o char pra byte foi mal kkk
for w in words:
    score = 0
    for c in w:
        w_c = weights[c]
        score += w_c
    total_w = score % 26
    final_letter = weight_to_letter_map[total_w]
    final_result += final_letter

print(final_result)
