import \
    struct  # Імпортуємо модуль struct для перетворення даних у байти та розбиття ключа на частини фіксованої довжини.


# Функція expand_key генерує набір раундових ключів для алгоритму RC5 на основі початкового ключа.
def expand_key(key, word_size=16, num_rounds=20):
    P = 0xB7E15163  # Константа P для ініціалізації ключових значень, специфічна для алгоритму RC5.
    Q = 0x9E3779B9  # Константа Q для генерації наступних значень раундових ключів.

    # Створюємо початковий список round_keys, де кожне значення обчислюється за формулою (P + i * Q).
    # Використовуємо word_size для обмеження кожного значення ключа до відповідного розміру слова.
    round_keys = [(P + (i * Q)) & ((1 << word_size) - 1) for i in range(2 * (num_rounds + 1))]

    # Перетворюємо ключ (key) у список слів фіксованої довжини, кожне з яких містить 4 байти.
    key_words = list(struct.unpack('!' + 'I' * (len(key) // 4), key))

    A = B = 0  # Ініціалізуємо значення A та B для подальшого використання у циклі генерації ключів.
    i = j = 0  # Ініціалізуємо індекси i та j для ітерації по round_keys і key_words.

    # Основний цикл генерації раундових ключів.
    # Виконується 3 * max(len(key_words), 2 * (num_rounds + 1)) ітерацій для рівномірного змішування.
    for _ in range(3 * max(len(key_words), 2 * (num_rounds + 1))):
        # Оновлюємо round_keys[i] і додаємо значення A та B.
        A = round_keys[i] = (round_keys[i] + A + B) & ((1 << word_size) - 1)
        # Оновлюємо key_words[j] і додаємо значення A та B.
        B = key_words[j] = (key_words[j] + A + B) & ((1 << word_size) - 1)

        # Збільшуємо індекси i та j з обмеженням їх довжиною списків.
        i = (i + 1) % (2 * (num_rounds + 1))
        j = (j + 1) % len(key_words)

    return round_keys  # Повертаємо згенерований список раундових ключів.