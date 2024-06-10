import random


def expansion(input):
    substrings = []
    for i in range(0, 100, 4):
        substrings.append(input[i:i + 4])
    result = input[99] + input[:5]
    for i in range(1, 24):
        result += substrings[i - 1][-1] + substrings[i] + substrings[i + 1][0]
    result += substrings[23][-1] + substrings[24] + input[0]
    return result


def keygen(key):
    key = expansion(key)
    keys = []
    for i in range(8):
        keys.append(key[0:64])
        keys.append(key[64:128])
        key = key[30:] + key[:30]

    return keys


def f(input, key):
    output_blocks = []
    for i in range(4):
        input_block = input[i * 8:i * 8 + 8]
        key_block = key[i * 16:i * 16 + 16]
        key_odd = ''
        key_even = ''
        for j in range(0, len(key_block) - 1, 2):
            key_odd += key_block[j]
            key_even += key_block[j + 1]

        temp1 = (int(input_block, 2) + int(key_odd, 2)) % (2 ** 8)
        temp2 = temp1 * int(key_even, 2) % (2 ** 8)
        output_block = bin(temp2)[2:].zfill(8)
        output_blocks.append(output_block)
    output = ''.join(output_blocks)
    return output


def encrypt(plaintext, key):
    keys = keygen(key)
    input_of_round = plaintext
    for i in range(15):
        left = input_of_round[:32]
        right = input_of_round[32:]
        next_left = right
        next_right = bin(int(left, 2) ^ int(f(right, keys[i]), 2))[2:].zfill(32)
        input_of_round = next_left + next_right

    # last round
    left = input_of_round[:32]
    right = input_of_round[32:]
    next_right = right
    next_left = bin(int(left, 2) ^ int(f(right, keys[15]), 2))[2:].zfill(32)
    output = next_left + next_right
    return output


plaintext = ''.join(str(random.randint(0, 1)) for i in range(64))
key = ''.join(str(random.randint(0, 1)) for i in range(100))
ciphertext = encrypt(plaintext, key)
print(f'plaintext: {plaintext}')
print(f'key: {key}')
print(f'ciphertext: {ciphertext}')
