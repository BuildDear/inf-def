from tkinter import messagebox, filedialog
from multiprocessing import Pool, cpu_count
from generator import generate_random_numbers, calculate_pi_estimate, calculate_sequence_period
from gui import update_status, update_message, show_error
from utils import save_to_file


def validate_inputs(entry_n, entry_display_limit, error_label, config_data):
    """Перевіряє правильність введених даних для кількості генерацій та обмеження відображення чисел."""
    try:
        n = int(entry_n.get())
        display_limit = int(entry_display_limit.get())
    except ValueError:
        show_error(error_label, "Введіть ціле число!")
        return None, None

    if n <= 0:
        show_error(error_label, "Введіть додатнє ціле число для кількості генерацій!")
        return None, None

    if display_limit <= 0 or display_limit > n:
        show_error(error_label, f"Кількість для відображення має бути додатньою і не більше {n}.")
        return None, None

    show_error(error_label, "")
    return n, display_limit


def generate_numbers_background(n, display_limit, elements, config_data, root):
    """Генерує псевдовипадкові числа у фоновому режимі залежно від значення n та передає їх для відображення."""
    if n > 5000:
        random_numbers = generate_random_numbers_parallel(n, config_data)
    else:
        random_numbers = generate_random_numbers(
            X0=config_data['X0'],
            a=config_data['a'],
            c=config_data['c'],
            m=config_data['m'],
            n=n
        )
    root.after(0, display_results, random_numbers, display_limit, elements)


def generate_random_numbers_parallel(n, config_data):
    """Генерує псевдовипадкові числа паралельно, використовуючи кілька процесів."""
    num_cores = min(cpu_count(), 4)
    chunk_size = n // num_cores

    with Pool(processes=num_cores) as pool:
        results = pool.starmap(generate_random_numbers, [
            (config_data['X0'], config_data['a'], config_data['c'], config_data['m'], chunk_size)
            for _ in range(num_cores)
        ])
    return [num for sublist in results for num in sublist]


def display_results(random_numbers, display_limit, elements):
    """Відображає результати генерації чисел, оцінку числа π та період генерації у текстовому полі."""
    clear_text_output(elements['text_output'])
    display_generated_numbers(random_numbers, display_limit, elements['text_output'])
    display_pi_estimate(random_numbers, elements['text_output'])
    display_sequence_period(random_numbers, elements['text_output'])
    update_status(elements['status_label'], "")
    update_message(elements['message_label'], "")


def clear_text_output(text_output):
    """Очищає текстове поле в інтерфейсі від попередніх результатів."""
    text_output.delete(1.0, 'end')


def display_generated_numbers(numbers, display_limit, text_output):
    """Виводить згенеровані псевдовипадкові числа у текстове поле відповідно до ліміту відображення."""
    text_output.insert('end', f"Показано {display_limit} чисел:\n" + str(numbers[:display_limit]) + "\n\n")


def display_pi_estimate(numbers, text_output):
    """Відображає оцінку числа π на основі згенерованих чисел у текстовому полі."""
    pi_estimate = calculate_pi_estimate(numbers)
    if pi_estimate:
        text_output.insert('end', f"Оцінка числа π: {pi_estimate}\n")
    else:
        text_output.insert('end', "Недостатньо даних для оцінки числа π.\n")


def display_sequence_period(numbers, text_output):
    """Виводить період генерації псевдовипадкової послідовності у текстовому полі."""
    period = calculate_sequence_period(numbers)
    text_output.insert('end', f"Період генерації: {period}\n")


def save_results_to_file(text_output):
    """Зберігає результати генерації чисел у файл, обраний користувачем."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        save_to_file(file_path, text_output)