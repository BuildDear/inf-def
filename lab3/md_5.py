import re  # Імпортуємо модуль re для роботи з регулярними виразами (не використовується в цьому коді).
import struct  # Імпортуємо модуль struct для роботи з байтовими структурами.
import math  # Імпортуємо модуль math для математичних обчислень.
import hashlib  # Імпортуємо модуль hashlib для використання стандартної бібліотеки MD5.

# Функція left_rotate виконує циклічний зсув числа x вліво на c позицій.
def left_rotate(x, c):
    """Операція циклічного зсуву вліво"""
    return (x << c) & 0xFFFFFFFF | (x >> (32 - c))

# Клас MD5 реалізує алгоритм хешування MD5 з нуля.
class MD5:
    def __init__(self):
        # Ініціалізація константних значень для MD5
        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        # Ініціалізуємо коефіцієнти K, які є функцією синуса
        self.K = [int(abs(math.sin(i + 1)) * (2 ** 32)) & 0xFFFFFFFF for i in range(64)]
        # Набір зміщень для кожного раунду
        self.shifts = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

    def md5_padding(self, message):
        """Додає підкладку до повідомлення для вирівнювання"""
        original_length = len(message) * 8  # Довжина повідомлення в бітах
        message += b'\x80'  # Додаємо одиничний біт з наступними нулями
        while (len(message) * 8) % 512 != 448:
            message += b'\x00'  # Заповнюємо нулями до 448 бітів
        message += struct.pack('<Q', original_length)  # Додаємо початкову довжину як 64-бітове число
        return message

    def process_block(self, block):
        """Обробка одного блоку розміром 512 біт (64 байти)"""
        X = list(struct.unpack('<16I', block))  # Розбиваємо блок на 16 32-бітних слів
        A, B, C, D = self.A, self.B, self.C, self.D  # Копіюємо початкові значення хешу

        # Основний цикл MD5, що обробляє 64 ітерації
        for i in range(64):
            if i < 16:
                F = (B & C) | (~B & D)
                g = i
            elif i < 32:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif i < 48:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            else:
                F = C ^ (B | ~D)
                g = (7 * i) % 16

            F = (F + A + self.K[i] + X[g]) & 0xFFFFFFFF  # Обчислюємо значення F і додаємо поточний ключ і значення з X[g]
            A, D, C, B = D, C, B, (B + left_rotate(F, self.shifts[i])) & 0xFFFFFFFF  # Оновлюємо значення A, B, C, D

        # Додаємо результати до початкових значень
        self.A = (self.A + A) & 0xFFFFFFFF
        self.B = (self.B + B) & 0xFFFFFFFF
        self.C = (self.C + C) & 0xFFFFFFFF
        self.D = (self.D + D) & 0xFFFFFFFF

    def update(self, message):
        """Оновлює стан хешу новими даними"""
        message = self.md5_padding(message)  # Додаємо підкладку до повідомлення
        for i in range(0, len(message), 64):  # Обробляємо кожен 512-бітний блок
            self.process_block(message[i:i + 64])

    def hexdigest(self):
        """Повертає хеш у вигляді шістнадцяткового рядка"""
        return ''.join([struct.pack('<I', x).hex() for x in [self.A, self.B, self.C, self.D]]).upper()


# Функція для очищення вхідного рядка, видаляючи пробіли з початку і кінця
def clean_input_string(input_string: str) -> str:
    cleaned_string = input_string.strip()
    return cleaned_string


# Функція md5_string хешує рядок за допомогою реалізації MD5
def md5_string(input_string: str) -> str:
    input_string = clean_input_string(input_string)  # Очищаємо вхідний рядок
    md5 = MD5()  # Створюємо екземпляр класу MD5
    md5.update(input_string.encode('utf-8'))  # Оновлюємо хеш, передаючи байтове представлення рядка
    return md5.hexdigest()  # Повертаємо результат хешування


# Функція md5_file хешує файл з використанням стандартної бібліотеки hashlib
def md5_file(file_path: str) -> str:
    md5 = hashlib.md5()  # Використовуємо стандартний MD5 з бібліотеки hashlib
    buffer_size = 4 * 1024  # Розмір буфера 4 KB для читання файлу частинами
    with open(file_path, 'rb') as f:
        while chunk := f.read(buffer_size):  # Читаємо файл по частинах
            md5.update(chunk)  # Оновлюємо хеш для кожної частини

    return md5.hexdigest().upper()  # Повертаємо хеш у вигляді шістнадцяткового рядка у верхньому регістрі


# Функція verify_file перевіряє хеш файлу на відповідність очікуваному хешу
def verify_file(file_path: str, expected_hash: str) -> bool:
    """Порівнює хеш файлу з очікуваним хешем"""
    actual_hash = md5_file(file_path)  # Генеруємо хеш файлу
    return actual_hash == expected_hash  # Порівнюємо з очікуваним хешем
