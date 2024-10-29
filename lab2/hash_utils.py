import hashlib  # Імпортуємо бібліотеку hashlib для використання вбудованих алгоритмів хешування
import multiprocessing  # Імпортуємо бібліотеку multiprocessing для паралельного виконання задач
import os  # Імпортуємо бібліотеку os для роботи з файловою системою
import struct  # Імпортуємо бібліотеку struct для роботи з байтовими структурами
import math  # Імпортуємо бібліотеку math для математичних операцій, таких як sin

# Константи зсувів для кожного раунду алгоритму MD5 (значення S)
S = [
        7, 12, 17, 22,  # Перша група зсувів
    ] * 4 + [
        5, 9, 14, 20,  # Друга група зсувів
    ] * 4 + [
        4, 11, 16, 23,  # Третя група зсувів
    ] * 4 + [
        6, 10, 15, 21  # Четверта група зсувів
    ] * 4  # Повторюємо кожну групу 4 рази для загальної кількості 64 зсувів

# Коефіцієнти для кожного кроку MD5 (значення K), обчислені на основі синусоїдних функцій
K = [int(abs(math.sin(i + 1)) * (2 ** 32)) & 0xFFFFFFFF for i in range(64)]


# Генеруємо 64 32-бітних константи для використання в основному циклі MD5

def left_rotate(x, c):
    """Функція для лівого циклічного зсуву 32-бітного числа x на c позицій.

    Параметри:
    x: число, яке потрібно зсунути.
    c: кількість позицій для зсуву.

    Повертає:
    Результат лівого циклічного зсуву.
    """
    # Виконуємо циклічний зсув і застосовуємо маску для отримання 32-бітного результату
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF


def compute_md5(message):
    """Обчислює MD5-хеш повідомлення.

    Параметри:
    message: байтовий рядок повідомлення.

    Повертає:
    Шістнадцятковий рядок MD5-хеша.
    """
    # Ініціалізація змінних відповідно до специфікації MD5
    A = 0x67452301  # Початкове значення A
    B = 0xEFCDAB89  # Початкове значення B
    C = 0x98BADCFE  # Початкове значення C
    D = 0x10325476  # Початкове значення D

    # Попередня обробка повідомлення (доповнення)
    original_byte_len = len(message)  # Початкова довжина повідомлення в байтах
    original_bit_len = original_byte_len * 8  # Початкова довжина повідомлення в бітах
    message += b'\x80'  # Додаємо біт '1' після повідомлення
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'  # Додаємо біти '0' поки довжина не стане конгруентною 448 по модулю 512
    message += struct.pack('<Q', original_bit_len)  # Додаємо 64-бітне представлення початкової довжини

    # Розбиваємо повідомлення на 512-бітні блоки і обробляємо кожен блок
    for offset in range(0, len(message), 64):
        a, b, c, d = A, B, C, D  # Копіюємо значення для поточного блоку
        chunk = message[offset:offset + 64]  # Вибираємо 64-байтний блок
        M = list(struct.unpack('<16I', chunk))  # Розбиваємо блок на шістнадцять 32-бітних слів

        # Основний цикл з 64 кроків
        for i in range(64):
            if 0 <= i <= 15:
                # Раунд 1
                f = (b & c) | (~b & d)
                g = i
            elif 16 <= i <= 31:
                # Раунд 2
                f = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                # Раунд 3
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                # Раунд 4
                f = c ^ (b | ~d)
                g = (7 * i) % 16

            # Маскуємо змінні для забезпечення 32-бітних значень
            f = (f + a + K[i] + M[g]) & 0xFFFFFFFF
            a = d
            d = c
            c = b
            b = (b + left_rotate(f, S[i])) & 0xFFFFFFFF

        # Додаємо результати поточного блоку до загальних значень
        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    # Формуємо остаточний MD5-хеш і повертаємо його у шістнадцятковому форматі
    digest = struct.pack('<4I', A, B, C, D)
    return ''.join('{:02x}'.format(byte) for byte in digest).upper()


def compute_hash_from_string(input_str):
    """Обчислення MD5-хеша для рядка.

    Параметри:
    input_str: вхідний рядок.

    Повертає:
    Шістнадцятковий рядок MD5-хеша.
    """
    message = input_str.encode('utf-8')  # Кодуємо рядок у байти
    return compute_md5(message)  # Обчислюємо і повертаємо хеш


def compute_chunk_hash(args):
    """Обчислення хеша одного блоку файлу.

    Параметри:
    args: кортеж (offset, size, file_path).

    Повертає:
    Шістнадцятковий рядок MD5-хеша блоку або None.
    """
    offset, size, file_path = args  # Розпаковуємо аргументи
    with open(file_path, 'rb') as f:
        f.seek(offset)  # Переміщуємо вказівник на початок блоку
        data = f.read(size)  # Читаємо дані блоку
        if not data:
            return None  # Якщо даних немає, повертаємо None
        return compute_md5(data)  # Повертаємо хеш блоку


def compute_md5_tree_hash(file_path):
    """Паралельне обчислення хеша файлу за допомогою дерево-хешування.

    Параметри:
    file_path: шлях до файлу.

    Повертає:
    Шістнадцятковий рядок MD5-хеша файлу.
    """
    CHUNK_SIZE = 1024 * 1024  # Встановлюємо розмір блоку в 1 МБ

    file_size = os.path.getsize(file_path)  # Отримуємо розмір файлу
    num_chunks = math.ceil(file_size / CHUNK_SIZE)  # Обчислюємо кількість блоків
    # Формуємо список аргументів для кожного блоку
    chunk_args = [(i * CHUNK_SIZE, min(CHUNK_SIZE, file_size - i * CHUNK_SIZE), file_path) for i in range(num_chunks)]

    # Виконуємо паралельне обчислення хешів блоків
    with multiprocessing.Pool() as pool:
        chunk_hashes = pool.map(compute_chunk_hash, chunk_args)

    # Фільтруємо порожні значення
    chunk_hashes = [h for h in chunk_hashes if h]

    # Об'єднуємо хеші блоків в дерево
    while len(chunk_hashes) > 1:
        temp_hashes = []
        for i in range(0, len(chunk_hashes), 2):
            if i + 1 < len(chunk_hashes):
                combined = chunk_hashes[i].encode('utf-8') + chunk_hashes[i + 1].encode(
                    'utf-8')  # Об'єднуємо пари хешів
            else:
                combined = chunk_hashes[i].encode('utf-8')  # Якщо залишився один хеш, залишаємо його
            temp_hashes.append(compute_md5(combined))  # Обчислюємо хеш від об'єднаних хешів
        chunk_hashes = temp_hashes  # Оновлюємо список хешів

    return chunk_hashes[0].upper()  # Повертаємо остаточний хеш у верхньому регістрі


def compute_hash_from_file_1(file_path):
    """Обчислення MD5-хеша файлу за допомогою модуля hashlib.

    Параметри:
    file_path: шлях до файлу.

    Повертає:
    Шістнадцятковий рядок MD5-хеша.
    """
    hash_md5 = hashlib.md5()  # Створюємо об'єкт MD5
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)  # Оновлюємо хеш з кожним прочитаним блоком
    return hash_md5.hexdigest().upper()  # Повертаємо хеш у шістнадцятковому форматі


def verify_file_integrity(file_path, hash_file_path):
    """Перевірка цілісності файлу шляхом порівняння його MD5-хеша із збереженим хешем.

    Параметри:
    file_path: шлях до файлу.
    hash_file_path: шлях до файлу з очікуваним хешем.

    Повертає:
    True, якщо хеші співпадають, інакше False.
    """
    computed_hash = compute_hash_from_file_1(file_path)  # Обчислюємо хеш файлу

    # Читаємо очікуваний хеш з файлу і видаляємо зайві пробіли
    with open(hash_file_path, 'r') as f:
        original_hash = f.read().strip().upper()

    return computed_hash == original_hash  # Повертаємо результат порівняння хешів


### ==== Реалізація внутрішньо послідовним алгоритмом ===

# Функція для зчитування блоку даних
def read_chunk(args):
    file_path, offset, size = args
    with open(file_path, 'rb') as f:
        f.seek(offset)
        return f.read(size)


# Основна функція для обчислення MD5 хешу файлу з розпаралелюванням зчитування
def md5_file_parallel(file_path, chunk_size=1024 * 1024):
    file_size = os.path.getsize(file_path)
    num_chunks = math.ceil(file_size / chunk_size)

    # Формуємо список аргументів для кожного блоку
    chunk_args = [(file_path, i * chunk_size, min(chunk_size, file_size - i * chunk_size)) for i in range(num_chunks)]

    # Використовуємо пул процесів для паралельного зчитування даних
    with multiprocessing.Pool() as pool:
        chunks = pool.map(read_chunk, chunk_args)

    # Створюємо об'єкт для зберігання стану хешу
    md5_state = MD5State()

    # Проходимо по всіх зчитаних блоках і оновлюємо стан хешу
    for chunk in chunks:
        md5_state.update(chunk)

    # Повертаємо фінальний хеш
    return md5_state.hexdigest()


# Клас для зберігання та оновлення стану MD5
class MD5State:
    def __init__(self):
        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        self.message_byte_length = 0
        self.buffer = b''

    def update(self, data):
        self.message_byte_length += len(data)
        self.buffer += data

        # Обробляємо 512-бітові блоки (64 байти)
        while len(self.buffer) >= 64:
            self._process_chunk(self.buffer[:64])
            self.buffer = self.buffer[64:]

    def _process_chunk(self, chunk):
        a, b, c, d = self.A, self.B, self.C, self.D
        M = list(struct.unpack('<16I', chunk))

        for i in range(64):
            if 0 <= i <= 15:
                f = (b & c) | (~b & d)
                g = i
            elif 16 <= i <= 31:
                f = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7 * i) % 16

            temp = (a + f + K[i] + M[g]) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + left_rotate(temp, S[i])) & 0xFFFFFFFF

        # Оновлюємо значення
        self.A = (self.A + a) & 0xFFFFFFFF
        self.B = (self.B + b) & 0xFFFFFFFF
        self.C = (self.C + c) & 0xFFFFFFFF
        self.D = (self.D + d) & 0xFFFFFFFF

    def hexdigest(self):
        # Додаємо доповнення до залишку даних у буфері
        data = self.buffer

        original_bit_len = self.message_byte_length * 8

        # Додаємо біт '1'
        data += b'\x80'

        # Додаємо біти '0' поки довжина не стане конгруентною 448 по модулю 512
        while (len(data) * 8) % 512 != 448:
            data += b'\x00'

        # Додаємо 64-бітне представлення початкової довжини
        data += struct.pack('<Q', original_bit_len)

        # Обробляємо залишкові блоки
        for offset in range(0, len(data), 64):
            self._process_chunk(data[offset:offset + 64])

        # Формуємо остаточний хеш
        digest = struct.pack('<4I', self.A, self.B, self.C, self.D)
        return ''.join('{:02x}'.format(byte) for byte in digest)
