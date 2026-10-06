# Лабораторная работа №1.
# Реализация прямого и обратного раундового преобразования DES

import random

# ==================== ТАБЛИЦЫ ====================

# Функция расширения E (32 -> 48 бит)
E_TABLE = [
    32, 1,  2,  3,  4,  5,
     4, 5,  6,  7,  8,  9,
     8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Перестановка P (32 -> 32 бит)
P_TABLE = [
    16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10,
     2,  8, 24, 14, 32, 27,  3,  9,
    19, 13, 30,  6, 22, 11,  4, 25
]

# S-блоки S1–S8
S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]


# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

def int_to_bin_str(value, length):
    """Преобразует целое число в битовую строку заданной длины."""
    return bin(value)[2:].zfill(length)


def bin_str_to_int(bit_str):
    """Преобразует битовую строку в целое число."""
    return int(bit_str, 2)


def permute(bit_str, table):
    """Перестановка битов согласно таблице (нумерация с 1)."""
    return ''.join(bit_str[i - 1] for i in table)


# ==================== ФУНКЦИЯ f ====================

def f(half_block, round_key, verbose=True):
    """
    Функция f DES.
    half_block — 32-битная строка
    round_key  — 48-битная строка
    """
    if verbose:
        print("\n--- Функция f ---")
        print("Входной полублок (32 бит):", half_block)
        print("Раундовый ключ  (48 бит):", round_key)

    # 1. Расширение E
    expanded = permute(half_block, E_TABLE)
    if verbose:
        print("1. После расширения E (48 бит):", expanded)

    # 2. XOR с раундовым ключом
    xor_result = ''.join(
        str(int(a) ^ int(b)) for a, b in zip(expanded, round_key)
    )
    if verbose:
        print("2. После XOR с ключом (48 бит):", xor_result)

    # 3. S-блоки
    s_output = ''
    if verbose:
        print("3. Обработка S-блоками:")
    for i in range(8):
        six_bits = xor_result[i * 6:(i + 1) * 6]
        row = int(six_bits[0] + six_bits[5], 2)
        col = int(six_bits[1:5], 2)
        val = S_BOXES[i][row][col]
        four_bits = int_to_bin_str(val, 4)
        s_output += four_bits
        if verbose:
            print("   S%d: вход=%s -> row=%d, col=%d -> %2d = %s" % (
                i + 1, six_bits, row, col, val, four_bits))

    if verbose:
        print("   После всех S-блоков (32 бит):", s_output)

    # 4. Перестановка P
    result = permute(s_output, P_TABLE)
    if verbose:
        print("4. После перестановки P (32 бит):", result)
        print("--- Конец функции f ---\n")

    return result


# ==================== ПРЯМОЕ ПРЕОБРАЗОВАНИЕ ====================

def encrypt_round(block, round_key, verbose=True):
    """
    Прямое раундовое преобразование DES.
    block     — 64-битная строка
    round_key — 48-битная строка
    """
    if len(block) != 64:
        raise ValueError("Блок должен быть длиной 64 бита")
    if len(round_key) != 48:
        raise ValueError("Раундовый ключ должен быть длиной 48 бит")

    L = block[:32]
    R = block[32:]

    if verbose:
        print("=" * 60)
        print("ПРЯМОЕ РАУНДОВОЕ ПРЕОБРАЗОВАНИЕ")
        print("=" * 60)
        print("Входной блок (64 бит):", block)
        print("L =", L)
        print("R =", R)
        print("Ключ (48 бит):", round_key)

    f_out = f(R, round_key, verbose=verbose)
    R_new = ''.join(str(int(a) ^ int(b)) for a, b in zip(L, f_out))
    L_new = R

    result = L_new + R_new

    if verbose:
        print("Новый L = R_old          :", L_new)
        print("Новый R = L_old XOR f(R) :", R_new)
        print("Выходной блок (64 бит)   :", result)
        print("=" * 60)

    return result


# ==================== ОБРАТНОЕ ПРЕОБРАЗОВАНИЕ ====================

def decrypt_round(block, round_key, verbose=True):
    """
    Обратное раундовое преобразование DES.
    block     — 64-битная строка
    round_key — 48-битная строка
    """
    if len(block) != 64:
        raise ValueError("Блок должен быть длиной 64 бита")
    if len(round_key) != 48:
        raise ValueError("Раундовый ключ должен быть длиной 48 бит")

    L = block[:32]
    R = block[32:]

    if verbose:
        print("=" * 60)
        print("ОБРАТНОЕ РАУНДОВОЕ ПРЕОБРАЗОВАНИЕ")
        print("=" * 60)
        print("Входной блок (64 бит):", block)
        print("L =", L)
        print("R =", R)
        print("Ключ (48 бит):", round_key)

    f_out = f(L, round_key, verbose=verbose)
    L_old = ''.join(str(int(a) ^ int(b)) for a, b in zip(R, f_out))
    R_old = L

    result = L_old + R_old

    if verbose:
        print("Старый L = R XOR f(L)    :", L_old)
        print("Старый R = L             :", R_old)
        print("Выходной блок (64 бит)   :", result)
        print("=" * 60)

    return result


# ==================== ТЕСТОВЫЙ ЗАПУСК ====================

if __name__ == "__main__":
    # Случайный 64-битный блок и 48-битный ключ
    block = ''.join(str(random.randint(0, 1)) for _ in range(64))
    round_key = ''.join(str(random.randint(0, 1)) for _ in range(48))

    print("\n" + "#" * 60)
    print("ТЕСТОВЫЙ ЗАПУСК")
    print("#" * 60)
    print("Исходный блок  (64 бит):", block)
    print("Раундовый ключ (48 бит):", round_key)

    # Прямое преобразование
    encrypted = encrypt_round(block, round_key, verbose=True)

    # Обратное преобразование
    decrypted = decrypt_round(encrypted, round_key, verbose=True)

    # Проверка
    print("\n" + "#" * 60)
    print("ПРОВЕРКА")
    print("#" * 60)
    print("Исходный блок :", block)
    print("После decrypt :", decrypted)
    print("Совпадают?    :", block == decrypted)
    if block == decrypted:
        print("OK: прямое и обратное преобразования работают корректно!")
    else:
        print("Ошибка: блоки не совпадают!")