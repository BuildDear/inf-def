import multiprocessing
import os
import struct
from multiprocessing import Pool
from hash_utils import left_rotate, K, S  # Імпорт необхідних функцій з утиліт для хешування

# Граничний розмір файлу для переходу на паралельне обчислення (50 МБ)
PARALLEL_THRESHOLD = 50 * 1024 * 1024  # 50 MB


def compute_chunk_hash(file_path, start_offset, chunk_size):
    """Функція для обчислення хеша окремого блоку даних.
    Відкриває файл, зчитує вказаний блок і обчислює MD5-хеш для нього.

    file_path: шлях до файлу
    start_offset: початкова позиція блоку у файлі
    chunk_size: розмір блоку, який потрібно зчитати
    """
    with open(file_path, 'rb') as f:  # Відкриття файлу в режимі читання байтів
        f.seek(start_offset)  # Переміщуємо вказівник на початкову позицію блоку
        chunk = f.read(chunk_size)  # Зчитуємо блок даних
        return md5(chunk)  # Повертаємо обчислений MD5-хеш для цього блоку


def combine_hashes(hashes):
    """Комбінуємо хеші окремих блоків у фінальний хеш.

    hashes: список хешів для всіх блоків
    """
    combined_hash = b''.join(hashes)  # Об'єднуємо хеші блоків у один
    return md5(combined_hash)  # Повертаємо фінальний MD5-хеш для всього файлу


def parallel_compute_file_hash(file_path, num_processes=4):
    """Паралельне обчислення хеша для великого файлу.

    file_path: шлях до файлу
    num_processes: кількість процесів для паралельної обробки (за замовчуванням 4)
    """
    num_processes = multiprocessing.cpu_count()  # Використовуємо кількість доступних ядер процесора
    file_size = os.path.getsize(file_path)  # Отримуємо розмір файлу
    # Ділимо файл на блоки для обробки
    chunks = [(i * CHUNK_SIZE, CHUNK_SIZE) for i in range(file_size // CHUNK_SIZE)]
    if file_size % CHUNK_SIZE != 0:  # Якщо є залишкові байти, додаємо останній блок
        chunks.append(((file_size // CHUNK_SIZE) * CHUNK_SIZE, file_size % CHUNK_SIZE))

    # Створюємо пул процесів для паралельного обчислення хешів
    with Pool(processes=num_processes) as pool:
        # Паралельно обчислюємо хеші для кожного блоку
        hash_results = pool.starmap(compute_chunk_hash, [(file_path, offset, size) for offset, size in chunks])

    return combine_hashes(hash_results)  # Повертаємо фінальний хеш, об'єднуючи всі хеші блоків


def compute_hash_from_file(file_path):
    """Звичайне послідовне обчислення хеша для файлів меншого розміру.

    file_path: шлях до файлу
    """
    # Ініціалізуємо стандартні константи для MD5
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476
    original_bit_len = 0  # Початкова довжина даних у бітах
    buffer = b''  # Буфер для зберігання даних

    # Відкриваємо файл для читання байтами
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(CHUNK_SIZE)  # Зчитуємо блок даних
            if not data:  # Якщо дані закінчилися — виходимо з циклу
                break
            buffer += data  # Додаємо дані до буфера
            original_bit_len += len(data) * 8  # Підраховуємо кількість бітів

            # Обробляємо кожні 64 байти даних
            while len(buffer) >= 64:
                chunk = buffer[:64]  # Вибираємо перші 64 байти
                buffer = buffer[64:]  # Видаляємо їх з буфера
                a, b, c, d = A, B, C, D  # Ініціалізуємо проміжні значення
                M = list(struct.unpack('<16I', chunk))  # Розпаковуємо дані в 16 слів (по 32 біти кожне)

                # Основний цикл MD5
                for i in range(64):
                    if 0 <= i <= 15:  # Перша частина
                        F = (b & c) | (~b & d)
                        g = i
                    elif 16 <= i <= 31:  # Друга частина
                        F = (d & b) | (~d & c)
                        g = (5 * i + 1) % 16
                    elif 32 <= i <= 47:  # Третя частина
                        F = b ^ c ^ d
                        g = (3 * i + 5) % 16
                    else:  # Четверта частина
                        F = c ^ (b | ~d)
                        g = (7 * i) % 16

                    F = (F + a + K[i] + M[g]) & 0xFFFFFFFF  # Обчислюємо F та оновлюємо значення a, b, c, d
                    a, d, c, b = d, c, b, (b + left_rotate(F, S[i])) & 0xFFFFFFFF

                # Оновлюємо основні регістри
                A = (A + a) & 0xFFFFFFFF
                B = (B + b) & 0xFFFFFFFF
                C = (C + c) & 0xFFFFFFFF
                D = (D + d) & 0xFFFFFFFF

    # Додаємо спеціальний байт до кінця даних
    buffer += b'\x80'
    while (len(buffer) * 8) % 512 != 448:  # Заповнюємо до 448 бітів
        buffer += b'\x00'
    buffer += struct.pack('<Q', original_bit_len)  # Додаємо довжину оригінальних даних

    # Остання обробка буфера
    for offset in range(0, len(buffer), 64):
        chunk = buffer[offset:offset + 64]
        a, b, c, d = A, B, C, D
        M = list(struct.unpack('<16I', chunk))

        for i in range(64):  # Повторний основний цикл
            if 0 <= i <= 15:
                F = (b & c) | (~b & d)
                g = i
            elif 16 <= i <= 31:
                F = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                F = c ^ (b | ~d)
                g = (7 * i) % 16

            F = (F + a + K[i] + M[g]) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + left_rotate(F, S[i])) & 0xFFFFFFFF

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    return struct.pack('<4I', A, B, C, D).hex().upper()  # Повертаємо результат у вигляді хешу


def verify_file_integrity(file_path, hash_file_path):
    """Перевірка цілісності файлу шляхом порівняння його MD5-хеша із збереженим хешем.

    file_path: шлях до файлу
    hash_file_path: шлях до файлу з очікуваним хешем
    """
    file_size = os.path.getsize(file_path)  # Отримуємо розмір файлу
    if file_size > PARALLEL_THRESHOLD:  # Якщо файл великий, обчислюємо хеш паралельно
        computed_hash = parallel_compute_file_hash(file_path)
    else:  # Для менших файлів використовуємо звичайне послідовне обчислення хеша
        computed_hash = compute_hash_from_file(file_path)

    # Читаємо очікуваний хеш з файлу
    with open(hash_file_path, 'r') as f:
        original_hash = f.read().strip().upper()

    return computed_hash == original_hash  # Повертаємо результат порівняння хешів
