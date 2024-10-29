import tkinter as tk
from threading import Thread
from gui import create_gui, update_status, update_message, show_error
from logic import generate_numbers_background, validate_inputs, save_results_to_file
from utils import read_config


def main():
    root = tk.Tk()
    root.title("Генератор псевдовипадкових чисел")
    root.configure(bg='#F4A261')

    # Зчитування параметрів з файлу config.json
    config_data = read_config()
    if config_data is None:
        root.destroy()

    # Створення інтерфейсу
    elements = create_gui(root)

    # Функція для запуску генерації чисел
    def generate_and_display_numbers():
        n, display_limit = validate_inputs(elements['entry_n'], elements['entry_display_limit'], elements['error_label'], config_data)
        if n is None or display_limit is None:
            return

        update_status(elements['status_label'], "Зачекайте, йде генерація...")
        update_message(elements['message_label'], "Числа ще генеруються, будь ласка зачекайте...")
        root.update()

        # Запуск генерації у фоновому режимі
        thread = Thread(target=generate_numbers_background, args=(n, display_limit, elements, config_data, root))
        thread.start()

    elements['button_generate'].config(command=generate_and_display_numbers)
    elements['button_save'].config(command=lambda: save_results_to_file(elements['text_output']))

    root.mainloop()


if __name__ == '__main__':
    main()
