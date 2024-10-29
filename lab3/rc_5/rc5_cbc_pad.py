import \
    os  # Імпортуємо модуль os для генерації випадкових байтів, які будуть використовуватись для генерації початкового вектора.

from information_defence.lab3.lemer_gen import LemerGenerator  # Імпортуємо генератор випадкових чисел LemerGenerator.
from information_defence.lab3.rc_5.block_operations import xor_bytes, split_blocks, rc5_decrypt_block, \
    rc5_encrypt_block  # Імпортуємо функції для блочних операцій та шифрування/розшифрування.
from information_defence.lab3.rc_5.padding import pad_data, \
    unpad_data  # Імпортуємо функції для додавання та видалення паддінгу.


# Клас RC5CBCPad реалізує RC5 шифрування у режимі CBC з використанням паддінгу.
class RC5CBCPad:
    def __init__(self, key, word_size=16, num_rounds=20):
        self.block_size = 8  # Розмір блоку для алгоритму RC5 у байтах (8 байтів = 64 біти).
        self.word_size = word_size  # Розмір слова для RC5 (16 біт).
        self.num_rounds = num_rounds  # Кількість раундів шифрування.
        self.key = self._pad_key(key, 8)  # Зберігаємо ключ, доповнений до потрібної довжини.

    # # Метод _pad_key доповнює ключ до заданої довжини (block_size).
    def _pad_key(self, key, block_size):
        key_len = len(key)
        return key[:block_size] if key_len >= block_size else key + b'\x00' * (block_size - key_len)

    # Метод generate_seed генерує випадкове число для ініціалізації генератора LemerGenerator.
    def generate_seed(self):
        return int.from_bytes(os.urandom(4),
                              byteorder='big')  # Генерує 4 випадкові байти та перетворює їх у ціле число.

    # Метод encrypt_file шифрує файл з ім'ям input_filename та записує результат у output_filename.
    def encrypt_file(self, input_filename, output_filename):
        seed = self.generate_seed()  # Генеруємо seed для LemerGenerator.
        lemer_generator = LemerGenerator(seed)  # Ініціалізуємо генератор випадкових чисел.
        iv = lemer_generator.get_bytes(self.block_size)  # Отримуємо вектор ініціалізації (IV) розміром block_size.

        with open(input_filename, 'rb') as infile:
            plaintext = infile.read()  # Зчитуємо весь текст з вхідного файлу.

        encrypted_data = self.encrypt_file_mode(plaintext, iv)  # Шифруємо дані з використанням IV.

        with open(output_filename, 'wb') as outfile:
            outfile.write(encrypted_data)  # Записуємо зашифровані дані у вихідний файл.

    # Метод decrypt_file розшифровує файл з ім'ям input_filename та записує результат у output_filename.
    def decrypt_file(self, input_filename, output_filename):
        with open(input_filename, 'rb') as infile:
            iv_ciphertext = infile.read()  # Зчитуємо вектор ініціалізації та зашифровані дані.

        iv = iv_ciphertext[:self.block_size]  # Витягуємо IV з початку файлу.
        ciphertext = iv_ciphertext[self.block_size:]  # Решта є зашифрованими даними.

        decrypted_data = self.decrypt_file_mode(ciphertext, iv)  # Розшифровуємо дані з використанням IV.

        with open(output_filename, 'wb') as outfile:
            outfile.write(decrypted_data)  # Записуємо розшифровані дані у вихідний файл.

    # Метод encrypt_console шифрує дані в пам'яті, використовуючи поданий вектор ініціалізації.
    def encrypt_console(self, plaintext, iv):
        plaintext = pad_data(plaintext, self.block_size)  # Додаємо паддінг до plaintext для вирівнювання блоку.
        blocks = split_blocks(plaintext, self.block_size)  # Розбиваємо текст на блоки розміром block_size.
        ciphertext = b''
        prev_block = iv

        # Шифруємо кожен блок, застосовуючи XOR з попереднім зашифрованим блоком (CBC).
        for block in blocks:
            block = xor_bytes(block, prev_block)  # Виконуємо XOR з попереднім блоком.
            cipher = rc5_encrypt_block(block, self.word_size, self.num_rounds, self.key)  # Шифруємо блок.
            ciphertext += cipher
            prev_block = cipher  # Оновлюємо попередній блок.

        return iv + ciphertext  # Повертаємо IV та зашифровані дані.

    # Метод decrypt_console розшифровує дані в пам'яті, використовуючи поданий вектор ініціалізації.
    def decrypt_console(self, ciphertext, iv):
        blocks = split_blocks(ciphertext[len(iv):], self.block_size)  # Розбиваємо зашифровані дані на блоки.
        plaintext = b''
        prev_block = iv

        # Розшифровуємо кожен блок, застосовуючи XOR з попереднім зашифрованим блоком (CBC).
        for block in blocks:
            decrypted_block = rc5_decrypt_block(block, self.word_size, self.num_rounds, self.key)  # Розшифровуємо блок.
            plaintext += xor_bytes(decrypted_block,
                                   prev_block)  # Виконуємо XOR з попереднім блоком для отримання plaintext.
            prev_block = block  # Оновлюємо попередній блок.

        return unpad_data(plaintext, self.block_size)  # Видаляємо паддінг і повертаємо розшифровані дані.

    # Метод encrypt_file_mode шифрує дані для файлу з поданим вектором ініціалізації (IV).
    def encrypt_file_mode(self, plaintext, iv):
        plaintext = pad_data(plaintext, self.block_size)  # Додаємо паддінг до plaintext.
        blocks = split_blocks(plaintext, self.block_size)  # Розбиваємо текст на блоки.
        ciphertext = b''
        prev_block = iv

        # Шифруємо кожен блок, використовуючи CBC-режим.
        for block in blocks:
            block = xor_bytes(block, prev_block)
            cipher = rc5_encrypt_block(block, self.word_size, self.num_rounds, self.key)
            ciphertext += cipher
            prev_block = cipher

        return iv + ciphertext  # Повертаємо IV та зашифровані дані.

    # Метод decrypt_file_mode розшифровує дані для файлу з поданим вектором ініціалізації (IV).
    def decrypt_file_mode(self, ciphertext, iv):
        blocks = split_blocks(ciphertext, self.block_size)  # Розбиваємо зашифровані дані на блоки.
        plaintext = b''
        prev_block = iv

        # Розшифровуємо кожен блок, використовуючи CBC-режим.
        for block in blocks:
            decrypted_block = rc5_decrypt_block(block, self.word_size, self.num_rounds, self.key)
            plaintext += xor_bytes(decrypted_block, prev_block)
            prev_block = block

        return unpad_data(plaintext, self.block_size)  # Видаляємо паддінг і повертаємо розшифровані дані.
