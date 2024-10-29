import random  # Імпортуємо модуль random для використання системного генератора випадкових чисел.
import math  # Імпортуємо модуль math для математичних операцій, зокрема для обчислення квадратного кореня.

# Клас LemerGenerator реалізує лінійний конгруентний генератор випадкових чисел (LCG).
class LemerGenerator:
    def __init__(self, seed=1, a=48271, c=0, m=2 ** 31):
        self.a = a  # Множник генератора.
        self.c = c  # Доданок генератора.
        self.m = m  # Модуль генератора.
        self.state = seed  # Початкове значення (зерно) генератора.
        self.generated_numbers = []  # Список для зберігання згенерованих чисел.

    def next(self):
        """Generates the next number in the sequence."""
        self.state = (self.a * self.state + self.c) % self.m  # Обчислюємо наступне число в послідовності за формулою LCG.
        self.generated_numbers.append(self.state)  # Зберігаємо згенероване число.
        return self.state  # Повертаємо згенероване число.

    def get_bytes(self, num_bytes):
        """Generates `num_bytes` worth of random data."""
        result = b''  # Ініціалізуємо порожній байтовий рядок.
        while len(result) < num_bytes:
            number = self.next()  # Генеруємо наступне число.
            result += number.to_bytes(4, byteorder='big')  # Перетворюємо число в байти і додаємо до результату.
        return result[:num_bytes]  # Повертаємо тільки необхідну кількість байтів.

    def save_to_file(self, filename):
        """Saves generated numbers to a file."""
        try:
            with open(filename, 'w') as f:
                for num in self.generated_numbers:
                    f.write(f"{num}\n")  # Записуємо кожне згенероване число у файл на новому рядку.
        except IOError as e:
            print(f"Error saving file: {e}")  # Виводимо повідомлення про помилку, якщо файл не вдалося зберегти.

    def find_period(self):
        sequence = self.generated_numbers  # Використовуємо згенеровані числа.
        length = len(sequence)
        for period in range(1, length // 2 + 1):
            if sequence[:period] == sequence[period:2 * period]:  # Шукаємо періодичну послідовність у згенерованих числах.
                return period  # Повертаємо знайдений період.
        return length  # Якщо період не знайдено, повертаємо довжину послідовності.


# Функція gcd обчислює найбільший спільний дільник (НСД) двох чисел за допомогою алгоритму Евкліда.
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a  # Повертаємо НСД.


# Функція estimate_pi оцінює значення π на основі ймовірності того, що дві випадково обрані пари чисел є взаємно простими.
def estimate_pi(num_pairs, rng_function, lemer_gen=None, h=False):
    coprime_count = 0  # Лічильник для взаємно простих пар.
    if h and lemer_gen:
        lemer_gen.l = lemer_gen.generated_numbers.copy()  # Копіюємо згенеровані числа, якщо потрібно.

    for _ in range(num_pairs):
        num1 = rng_function()  # Генеруємо перше число.
        num2 = rng_function()  # Генеруємо друге число.
        if gcd(num1, num2) == 1:
            coprime_count += 1  # Збільшуємо лічильник, якщо числа взаємно прості.

    probability = coprime_count / num_pairs  # Ймовірність того, що пара чисел є взаємно простою.
    pi_estimate = math.sqrt(6 / probability) if probability > 0 else float('inf')  # Обчислюємо оцінку π, якщо ймовірність > 0.
    return pi_estimate  # Повертаємо оцінку π.


# Функція test_random_generators тестує генератори випадкових чисел та оцінює значення π.
def test_random_generators(num_pairs):
    seed = 11  # Початкове значення для генератора Лемера.
    a = 12 ** 3  # Множник для генератора Лемера.
    c = 987  # Доданок для генератора Лемера.
    m = 2 ** 25 - 1  # Модуль для генератора Лемера.

    # Ініціалізуємо генератор Лемера.
    lemer_gen = LemerGenerator(seed=seed, a=a, c=c, m=m)

    # Генеруємо числа.
    for _ in range(num_pairs):
        lemer_gen.next()

    # Зберігаємо згенеровані числа у файл.
    filename = 'output.txt'
    lemer_gen.save_to_file(filename)
    print(f"Згенеровані числа збережено у файл {filename}.")

    # Оцінюємо значення π за допомогою генератора Лемера.
    pi_est_lemer = estimate_pi(num_pairs, lemer_gen.next, lemer_gen, True)
    print(f"Оцінка числа π за допомогою генератора Лемера: {pi_est_lemer}")

    # Знаходимо період генератора Лемера.
    period = lemer_gen.find_period()
    print(f"Період генератора Лемера: {period}")

    # Тестуємо оцінку π за допомогою системного генератора випадкових чисел.
    print("\nТестування з використанням системного генератора псевдовипадкових чисел:")
    pi_est_system = estimate_pi(num_pairs, lambda: random.randint(1, 1000000))
    print(f"Оцінка числа π за допомогою системного генератора: {pi_est_system}")


# Основний блок, який запускає тестування генераторів випадкових чисел.
if __name__ == "__main__":
    num_pairs = int(input("Введіть n: "))  # Вводимо кількість пар чисел для тестування.
    test_random_generators(num_pairs)  # Викликаємо функцію для тестування генераторів.
