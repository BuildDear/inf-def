# import \
#     struct  # Імпортуємо модуль struct для роботи з бінарними даними (упаковка та розпаковка даних у бінарні структури)
# import \
#     os  # Імпортуємо модуль os для генерації випадкових чисел (оскільки потрібний надійний генератор випадкових чисел)
# from LemerGen import LemerGenerator  # Імпортуємо генератор Лемера для створення вектора ініціалізації (IV)
#
#
# # Клас RC5CBCPad реалізує алгоритм шифрування RC5 у режимі CBC з паддінгом
# class RC5CBCPad:
#     def __init__(self, key, word_size=16, num_rounds=20):
#         # Ініціалізуємо розмір блоку, розмір слова та кількість раундів шифрування
#         self.block_size = 8  # 64 біти (8 байт) на блок для шифрування
#         self.word_size = word_size  # Розмір слова (32 біти за замовчуванням)
#         self.num_rounds = num_rounds  # Кількість раундів шифрування (20 за замовчуванням)
#         self.key = self._pad_key(key, 8)  # Приводимо ключ до розміру 16 байтів (128 біт)
#
#     # Метод для доповнення ключа до потрібної довжини (16 байтів)
#     def _pad_key(self, key, block_size):
#         key_len = len(key)  # Отримуємо довжину ключа
#         if key_len >= block_size:  # Якщо ключ вже більше або дорівнює необхідній довжині
#             return key[:block_size]  # Обрізаємо його до потрібних 16 байтів
#         else:
#             return key + b'\x00' * (block_size - key_len)  # Доповнюємо ключ нулями до 16 байтів
#
#     # Метод для операції побітового XOR над двома байтовими рядками
#     def _xor_bytes(self, a, b):
#         return bytes(x ^ y for x, y in zip(a, b))  # Виконуємо побітовий XOR між відповідними байтами a і b
#
#     # Метод для доповнення (паддінг) даних згідно з розміром блоку
#     def _pad_data(self, data):
#         padding_len = self.block_size - len(
#             data) % self.block_size  # Обчислюємо кількість байтів, яких не вистачає до розміру блоку
#         padding = bytes([padding_len] * padding_len)  # Створюємо байти для доповнення (паддінг)
#         return data + padding  # Повертаємо доповнені дані
#
#     # Метод для видалення паддінгу з розшифрованих даних
#     def _unpad_data(self, data):
#         padding_len = data[-1]  # Останній байт містить кількість байтів паддінгу
#         if padding_len < 1 or padding_len > self.block_size:  # Перевіряємо, чи коректний паддінг
#             raise ValueError("Invalid padding")  # Якщо ні, кидаємо помилку
#         if data[-padding_len:] != bytes([padding_len] * padding_len):  # Перевіряємо, чи паддінг коректний
#             raise ValueError("Invalid padding")  # Якщо паддінг некоректний, кидаємо помилку
#         return data[:-padding_len]  # Видаляємо паддінг і повертаємо очищені дані
#
#     # Метод для розбиття даних на блоки фіксованого розміру
#     def _split_blocks(self, data):
#         return [data[i:i + self.block_size] for i in
#                 range(0, len(data), self.block_size)]  # Розбиваємо дані на блоки розміром block_size
#
#     # Шифрує один блок даних за допомогою алгоритму RC5
#     def _rc5_encrypt_block(self, block):
#         A, B = struct.unpack('!II', block)  # Розпаковуємо блок у два 32-бітові слова
#         round_keys = self._expand_key()  # Генеруємо раундові ключі
#
#         for i in range(self.num_rounds):  # Проходимо 20 раундів шифрування
#             A = (A + round_keys[2 * i]) & ((1 << self.word_size) - 1)  # Додаємо раундовий ключ до A
#             B = (B + round_keys[2 * i + 1]) & ((1 << self.word_size) - 1)  # Додаємо раундовий ключ до B
#             A ^= B  # Виконуємо XOR між A і B
#             A = (A << (B % self.word_size)) | (A >> (self.word_size - (B % self.word_size)))  # Циклічно зміщуємо A
#             A &= ((1 << self.word_size) - 1)  # Обмежуємо розмір слова до word_size
#             B ^= A  # Виконуємо XOR між B і A
#             B = (B << (A % self.word_size)) | (B >> (self.word_size - (A % self.word_size)))  # Циклічно зміщуємо B
#             B &= ((1 << self.word_size) - 1)  # Обмежуємо розмір слова до word_size
#
#         return struct.pack('!II', A, B)  # Пакуємо назад у два 32-бітові слова і повертаємо
#
#     # Дешифрує один блок даних за допомогою алгоритму RC5
#     def _rc5_decrypt_block(self, block):
#         A, B = struct.unpack('!II', block)  # Розпаковуємо блок у два 32-бітові слова
#         round_keys = self._expand_key()  # Генеруємо раундові ключі
#
#         for i in range(self.num_rounds - 1, -1, -1):  # Проходимо раунди дешифрування у зворотному порядку
#             B = (B >> (A % self.word_size)) | (
#                         B << (self.word_size - (A % self.word_size)))  # Циклічно зміщуємо B у зворотному напрямку
#             B &= ((1 << self.word_size) - 1)  # Обмежуємо розмір слова до word_size
#             B ^= A  # Виконуємо XOR між B і A
#             A = (A >> (B % self.word_size)) | (
#                         A << (self.word_size - (B % self.word_size)))  # Циклічно зміщуємо A у зворотному напрямку
#             A &= ((1 << self.word_size) - 1)  # Обмежуємо розмір слова до word_size
#             A ^= B  # Виконуємо XOR між A і B
#             B = (B - round_keys[2 * i + 1]) & ((1 << self.word_size) - 1)  # Віднімаємо раундовий ключ від B
#             A = (A - round_keys[2 * i]) & ((1 << self.word_size) - 1)  # Віднімаємо раундовий ключ від A
#
#         return struct.pack('!II', A, B)  # Пакуємо назад у два 32-бітові слова і повертаємо
#
#     # Генеруємо ключі для кожного раунду шифрування
#     def _expand_key(self):
#         P = 0xB7E15163  # Початкове значення для генерації ключів
#         Q = 0x9E3779B9  # Додаткове значення для генерації ключів
#         # Створюємо раундові ключі (2 * (num_rounds + 1) значень)
#         round_keys = [(P + (i * Q)) & ((1 << self.word_size) - 1) for i in range(2 * (self.num_rounds + 1))]
#
#         # Розбиваємо ключ на 32-бітові слова для кожного раунду
#         key_words = list(struct.unpack('!' + 'I' * (len(self.key) // 4), self.key))
#         i = j = 0  # Індекси для кругового оброблення ключових слів
#         A = B = 0  # Початкові значення для обробки ключів
#
#         # Проходимо цикл, щоб адаптувати раундові ключі та ключові слова
#         for _ in range(3 * max(len(key_words), 2 * (self.num_rounds + 1))):
#             A = round_keys[i] = (round_keys[i] + A + B) & ((1 << self.word_size) - 1)
#             B = key_words[j] = (key_words[j] + A + B) & ((1 << self.word_size) - 1)
#             i = (i + 1) % (2 * (self.num_rounds + 1))  # Переходимо до наступного ключа
#             j = (j + 1) % len(key_words)  # Переходимо до наступного слова ключа
#
#         return round_keys  # Повертаємо згенеровані раундові ключі
#
#     # Генеруємо випадкове число для вектора ініціалізації (IV)
#     def generate_seed(self):
#         return int.from_bytes(os.urandom(4), byteorder='big')  # Використовуємо надійний генератор випадкових чисел
#
#     # Метод для шифрування файлу
#     def encrypt_file(self, input_filename, output_filename):
#         seed = self.generate_seed()  # Генеруємо випадкове значення для IV
#         lemer_generator = LemerGenerator(seed)  # Використовуємо генератор Лемера для створення IV
#         iv = lemer_generator.get_bytes(self.block_size)  # Генеруємо IV для шифрування
#
#         with open(input_filename, 'rb') as infile:  # Читаємо вхідний файл у бінарному режимі
#             plaintext = infile.read()  # Зчитуємо всі дані з файлу
#
#         encrypted_data = self.encrypt_file_mode(plaintext, iv)  # Шифруємо дані
#
#         with open(output_filename, 'wb') as outfile:  # Відкриваємо вихідний файл для запису в бінарному режимі
#             outfile.write(encrypted_data)  # Записуємо зашифровані дані
#
#     # Метод для дешифрування файлу
#     def decrypt_file(self, input_filename, output_filename):
#         with open(input_filename, 'rb') as infile:  # Читаємо вхідний файл у бінарному режимі
#             iv_ciphertext = infile.read()  # Зчитуємо зашифровані дані разом з IV
#
#         iv = iv_ciphertext[:self.block_size]  # Витягуємо IV із початку файлу
#         ciphertext = iv_ciphertext[self.block_size:]  # Витягуємо решту зашифрованих даних
#
#         decrypted_data = self.decrypt_file_mode(ciphertext, iv)  # Дешифруємо дані
#
#         with open(output_filename, 'wb') as outfile:  # Відкриваємо вихідний файл для запису в бінарному режимі
#             outfile.write(decrypted_data)  # Записуємо розшифровані дані
#
#     # Метод для шифрування з консолі
#     def encrypt_console(self, plaintext, iv):
#         plaintext = self._pad_data(plaintext)  # Доповнюємо дані для відповідності блоку
#         blocks = self._split_blocks(plaintext)  # Розбиваємо дані на блоки
#         ciphertext = b''  # Ініціалізуємо змінну для зберігання шифрованих блоків
#         prev_block = iv  # Початковий блок - це IV
#
#         for block in blocks:
#             block = self._xor_bytes(block, prev_block)  # Виконуємо XOR з попереднім блоком
#             cipher = self._rc5_encrypt_block(block)  # Шифруємо блок
#             ciphertext += cipher  # Додаємо зашифрований блок до результату
#             prev_block = cipher  # Оновлюємо попередній блок
#
#         return iv + ciphertext  # Повертаємо IV разом з шифрованими даними
#
#     # Метод для дешифрування з консолі
#     def decrypt_console(self, ciphertext, iv):
#         blocks = self._split_blocks(ciphertext[len(iv):])  # Розбиваємо шифровані дані на блоки, виключаючи IV
#         plaintext = b''  # Ініціалізуємо змінну для зберігання розшифрованих блоків
#         prev_block = iv  # Початковий блок - це IV
#
#         for block in blocks:
#             decrypted_block = self._rc5_decrypt_block(block)  # Дешифруємо блок
#             plaintext += self._xor_bytes(decrypted_block, prev_block)  # Виконуємо XOR з попереднім блоком
#             prev_block = block  # Оновлюємо попередній блок
#
#         plaintext = self._unpad_data(plaintext)  # Видаляємо паддінг з даних
#         return plaintext  # Повертаємо розшифровані дані
#
#     # Функції для шифрування та дешифрування для файлів
#     def encrypt_file_mode(self, plaintext, iv):
#         plaintext = self._pad_data(plaintext)  # Доповнюємо дані для відповідності блоку
#         blocks = self._split_blocks(plaintext)  # Розбиваємо дані на блоки
#         ciphertext = b''  # Ініціалізуємо змінну для зберігання шифрованих блоків
#         prev_block = iv  # Початковий блок - це IV
#
#         for block in blocks:
#             block = self._xor_bytes(block, prev_block)  # Виконуємо XOR з попереднім блоком
#             cipher = self._rc5_encrypt_block(block)  # Шифруємо блок
#             ciphertext += cipher  # Додаємо зашифрований блок до результату
#             prev_block = cipher  # Оновлюємо попередній блок
#
#         return iv + ciphertext  # Повертаємо IV разом з шифрованими даними
#
#     # Функція для дешифрування файлів
#     def decrypt_file_mode(self, ciphertext, iv):
#         blocks = self._split_blocks(ciphertext)  # Розбиваємо шифровані дані на блоки
#         plaintext = b''  # Ініціалізуємо змінну для зберігання розшифрованих блоків
#         prev_block = iv  # Початковий блок - це IV
#
#         for block in blocks:
#             decrypted_block = self._rc5_decrypt_block(block)  # Дешифруємо блок
#             plaintext += self._xor_bytes(decrypted_block, prev_block)  # Виконуємо XOR з попереднім блоком
#             prev_block = block  # Оновлюємо попередній блок
#
#         plaintext = self._unpad_data(plaintext)  # Видаляємо паддінг з даних
#         return plaintext  # Повертаємо розшифровані дані
