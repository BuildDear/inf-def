import struct  # Імпортуємо модуль struct для роботи з байтами та конвертації чисел у байтовий формат та навпаки.

from information_defence.lab3.rc_5.key_expansion import \
    expand_key  # Імпортуємо функцію expand_key з модуля key_expansion для генерації ключів для кожного раунду шифрування.


# Функція xor_bytes виконує побітову операцію XOR між двома байтами однакової довжини.
def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a,
                                       b))  # Для кожної пари байтів з a і b виконується операція XOR і результат зберігається у вигляді нових байтів.


# Функція split_blocks розбиває дані на блоки заданого розміру.
def split_blocks(data, block_size):
    return [data[i:i + block_size] for i in
            range(0, len(data), block_size)]  # Розбиваємо data на блоки розміром block_size, формуючи список блоків.


# Функція rc5_encrypt_block шифрує один блок даних з використанням алгоритму RC5.
def rc5_encrypt_block(block, word_size, num_rounds, key):
    A, B = struct.unpack('!II',
                         block)  # Розбиваємо вхідний блок на два 32-бітні цілі числа A та B за допомогою struct.unpack.
    round_keys = expand_key(key, word_size,
                            num_rounds)  # Генеруємо раундові ключі на основі основного ключа, розміру слова та кількості раундів.

    # Основний цикл шифрування RC5, який виконується num_rounds разів.
    for i in range(num_rounds):
        A = (A + round_keys[2 * i]) & ((1 << word_size) - 1)  # Додаємо ключ до A з модулем за розміром слова.
        B = (B + round_keys[2 * i + 1]) & ((1 << word_size) - 1)  # Додаємо ключ до B з модулем за розміром слова.

        A ^= B  # Виконуємо XOR між A та B.
        A = (A << (B % word_size)) | (
                    A >> (word_size - (B % word_size)))  # Виконуємо циклічний зсув вліво на B % word_size позицій.
        A &= ((1 << word_size) - 1)  # Обмежуємо A до розміру слова.

        B ^= A  # Виконуємо XOR між B та A.
        B = (B << (A % word_size)) | (
                    B >> (word_size - (A % word_size)))  # Виконуємо циклічний зсув вліво на A % word_size позицій.
        B &= ((1 << word_size) - 1)  # Обмежуємо B до розміру слова.

    return struct.pack('!II', A, B)  # Повертаємо зашифрований блок у вигляді байтів.


# Функція rc5_decrypt_block розшифровує один блок даних з використанням алгоритму RC5.
def rc5_decrypt_block(block, word_size, num_rounds, key):
    A, B = struct.unpack('!II', block)  # Розбиваємо вхідний блок на два 32-бітні цілі числа A та B.
    round_keys = expand_key(key, word_size,
                            num_rounds)  # Генеруємо раундові ключі на основі основного ключа, розміру слова та кількості раундів.

    # Основний цикл розшифрування RC5, який виконується num_rounds разів у зворотному порядку.
    for i in range(num_rounds - 1, -1, -1):
        B = (B >> (A % word_size)) | (
                    B << (word_size - (A % word_size)))  # Виконуємо циклічний зсув вправо на A % word_size позицій.
        B &= ((1 << word_size) - 1)  # Обмежуємо B до розміру слова.
        B ^= A  # Виконуємо XOR між B та A.

        A = (A >> (B % word_size)) | (
                    A << (word_size - (B % word_size)))  # Виконуємо циклічний зсув вправо на B % word_size позицій.
        A &= ((1 << word_size) - 1)  # Обмежуємо A до розміру слова.
        A ^= B  # Виконуємо XOR між A та B.

        B = (B - round_keys[2 * i + 1]) & ((1 << word_size) - 1)  # Віднімаємо ключ від B з модулем за розміром слова.
        A = (A - round_keys[2 * i]) & ((1 << word_size) - 1)  # Віднімаємо ключ від A з модулем за розміром слова.

    return struct.pack('!II', A, B)  # Повертаємо розшифрований блок у вигляді байтів.