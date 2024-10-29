import re
import struct
import math
import hashlib


def left_rotate(x, c):
    """Операція циклічного зсуву вліво"""
    return (x << c) & 0xFFFFFFFF | (x >> (32 - c))


class MD5:
    def __init__(self):
        # Ініціалізація констант
        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        # Коефіцієнти для кожного раунду
        self.K = [int(abs(math.sin(i + 1)) * (2 ** 32)) & 0xFFFFFFFF for i in range(64)]
        # Зміщення для кожного раунду
        self.shifts = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

    def md5_padding(self, message):
        """Додає підкладку до повідомлення для вирівнювання"""
        original_length = len(message) * 8  # Довжина повідомлення в бітах
        message += b'\x80'  # Додаємо біти, щоб заповнити повідомлення
        while (len(message) * 8) % 512 != 448:
            message += b'\x00'  # Заповнюємо нулями до 448 бітів
        message += struct.pack('<Q', original_length)  # Додаємо початкову довжину як 64-бітове число
        return message

    def process_block(self, block):
        """Обробка одного блоку розміром 512 біт"""
        X = list(struct.unpack('<16I', block))
        A, B, C, D = self.A, self.B, self.C, self.D

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

            F = (F + A + self.K[i] + X[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + left_rotate(F, self.shifts[i])) & 0xFFFFFFFF

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


def clean_input_string(input_string: str) -> str:
    # Видаляємо лише зайві пробіли з початку і кінця рядка
    cleaned_string = input_string.strip()
    return cleaned_string



def md5_string(input_string: str) -> str:
    input_string = clean_input_string(input_string)  # Очищаємо вхідний рядок
    md5 = MD5()  # Створюємо екземпляр класу MD5
    md5.update(input_string.encode('utf-8'))  # Оновлюємо хеш, передаючи байтове представлення рядка
    return md5.hexdigest()  # Повертаємо результат хешування



# Функція для хешування файлу з використанням hashlib
def md5_file(file_path: str) -> str:
    md5 = hashlib.md5()  # Використовуємо hashlib для хешування файлу
    buffer_size = 4 * 1024  # 4 KB буфер для читання файлу частинами
    with open(file_path, 'rb') as f:
        while chunk := f.read(buffer_size):  # Читаємо файл частинами по 4 KB
            md5.update(chunk)

    return md5.hexdigest().upper()


# Функція для перевірки файлу
def verify_file(file_path: str, expected_hash: str) -> bool:
    """Порівнює хеш файлу з очікуваним хешем"""
    actual_hash = md5_file(file_path)  # Генеруємо хеш файлу з використанням hashlib
    return actual_hash == expected_hash  # Порівнюємо з очікуваним хешем
