# Функція pad_data додає заповнення (padding) до даних, щоб їх довжина стала кратною розміру блоку.
def pad_data(data, block_size):
    padding_len = block_size - len(
        data) % block_size  # Обчислюємо кількість байтів для доповнення (padding), щоб зробити довжину data кратною block_size.
    padding = bytes([
                        padding_len] * padding_len)  # Створюємо байти заповнення, кожен з яких має значення, рівне довжині доповнення (padding_len).
    return data + padding  # Додаємо заповнення до кінця даних і повертаємо результат.


# Функція unpad_data видаляє заповнення (padding) з даних після розшифрування.
def unpad_data(data, block_size):
    padding_len = data[-1]  # Знаходимо значення останнього байта, яке вказує на кількість байтів доповнення.

    # Перевіряємо, чи кількість байтів доповнення коректна.
    if padding_len < 1 or padding_len > block_size:
        raise ValueError(
            "Invalid padding")  # Якщо значення padding_len поза межами 1 і block_size, то доповнення некоректне.

    # Перевіряємо, чи всі останні байти рівні значенню padding_len.
    if data[-padding_len:] != bytes([padding_len] * padding_len):
        raise ValueError(
            "Invalid padding")  # Якщо останні байти не збігаються зі значенням padding_len, доповнення некоректне.

    return data[:-padding_len]  # Видаляємо доповнення і повертаємо дані без останніх padding_len байтів.
