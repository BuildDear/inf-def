import math


def generate_random_numbers(X0, a, c, m, n):
    """Генерує псевдовипадкові числа за лінійним конгруентним методом."""
    numbers = []
    Xn = X0
    for _ in range(n):
        Xn = calculate_next_number(Xn, a, c, m)
        numbers.append(Xn)
    return numbers


def calculate_next_number(Xn, a, c, m):
    """Обчислює наступне число за формулою лінійного конгруентного методу."""
    return (a * Xn + c) % m


def find_greatest_common_divisor(a, b):
    """Обчислює найбільший спільний дільник (НСД) двох чисел."""
    while b != 0:
        a, b = swap_values(a, b)
    return a


def swap_values(a, b):
    """Повертає b як нове a, а залишок від ділення a на b як нове b."""
    return b, a % b


def calculate_pi_estimate(random_numbers):
    """Оцінює число π за згенерованими псевдовипадковими числами."""
    total_pairs = len(random_numbers) // 2
    coprime_count = count_coprime_pairs(random_numbers, total_pairs)
    return compute_pi_value(coprime_count, total_pairs) if total_pairs > 0 else None


def count_coprime_pairs(numbers, total_pairs):
    """Рахує кількість пар взаємно простих чисел у списку."""
    coprime_count = 0
    for i in range(total_pairs):
        num1, num2 = extract_pair(numbers, i)
        if find_greatest_common_divisor(num1, num2) == 1:
            coprime_count += 1
    return coprime_count


def extract_pair(numbers, index):
    """Витягує пару чисел зі списку за індексом."""
    return numbers[2 * index], numbers[2 * index + 1]


def compute_pi_value(coprime_count, total_pairs):
    """Обчислює оцінку числа π на основі взаємно простих чисел."""
    probability = coprime_count / total_pairs
    return math.sqrt(6 / probability)


def calculate_sequence_period(sequence):
    """Обчислює період повторення послідовності."""
    for i in range(1, len(sequence)):
        if is_period_repeating(sequence, i):
            return i
    return len(sequence)


def is_period_repeating(sequence, period_length):
    """Перевіряє, чи повторюється початкова частина послідовності."""
    return sequence[period_length:] == sequence[:len(sequence) - period_length]
