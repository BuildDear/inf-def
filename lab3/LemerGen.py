import random
import math


class LemerGenerator:
    def __init__(self, seed=1, a=48271, c=0, m=2 ** 31):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed
        self.generated_numbers = []

    def next(self):
        """Generates the next number in the sequence."""
        self.state = (self.a * self.state + self.c) % self.m
        self.generated_numbers.append(self.state)
        return self.state

    def get_bytes(self, num_bytes):
        """Generates `num_bytes` worth of random data."""
        result = b''
        while len(result) < num_bytes:
            number = self.next()
            result += number.to_bytes(4, byteorder='big')
        return result[:num_bytes]

    def save_to_file(self, filename):
        """Saves generated numbers to a file."""
        try:
            with open(filename, 'w') as f:
                for num in self.generated_numbers:
                    f.write(f"{num}\n")
        except IOError as e:
            print(f"Error saving file: {e}")

    def find_period(self):
        sequence = self.generated_numbers  # Using the generated numbers
        length = len(sequence)
        for period in range(1, length // 2 + 1):
            if sequence[:period] == sequence[period:2 * period]:
                return period
        return length


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def estimate_pi(num_pairs, rng_function, lemer_gen=None, h=False):
    coprime_count = 0
    if h and lemer_gen:
        lemer_gen.l = lemer_gen.generated_numbers.copy()

    for _ in range(num_pairs):
        num1 = rng_function()
        num2 = rng_function()
        if gcd(num1, num2) == 1:
            coprime_count += 1

    probability = coprime_count / num_pairs
    pi_estimate = math.sqrt(6 / probability) if probability > 0 else float('inf')
    return pi_estimate


def test_random_generators(num_pairs):
    seed = 11
    a = 12 ** 3
    c = 987
    m = 2 ** 25 - 1

    # Initialize Lemer generator
    lemer_gen = LemerGenerator(seed=seed, a=a, c=c, m=m)

    # Generate numbers
    for _ in range(num_pairs):
        lemer_gen.next()

    # Save generated numbers to file
    filename = 'output.txt'
    lemer_gen.save_to_file(filename)
    print(f"Згенеровані числа збережено у файл {filename}.")

    # Estimate pi using Lemer generator
    pi_est_lemer = estimate_pi(num_pairs, lemer_gen.next, lemer_gen, True)
    print(f"Оцінка числа π за допомогою генератора Лемера: {pi_est_lemer}")

    # Find period of Lemer generator
    period = lemer_gen.find_period()
    print(f"Період генератора Лемера: {period}")

    # Testing with system's random number generator
    print("\nТестування з використанням системного генератора псевдовипадкових чисел:")
    pi_est_system = estimate_pi(num_pairs, lambda: random.randint(1, 1000000))
    print(f"Оцінка числа π за допомогою системного генератора: {pi_est_system}")


if __name__ == "__main__":
    num_pairs = int(input("Введіть n: "))
    test_random_generators(num_pairs)
