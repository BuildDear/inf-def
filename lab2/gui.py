import tkinter as tk  # Імпортуємо модуль tkinter для створення графічного інтерфейсу
from tkinter import filedialog, messagebox  # Імпортуємо модулі для діалогових вікон
from hash_utils import compute_hash_from_string, compute_hash_from_file_1, verify_file_integrity, compute_md5_tree_hash, \
    md5_file_parallel


# Імпортуємо користувацькі функції для обчислення та перевірки MD5-хешів

def create_gui():
    """Функція для створення графічного інтерфейсу користувача (GUI)."""
    root = tk.Tk()  # Створюємо головне вікно програми
    root.title("MD5 Hash Generator and Verifier")  # Встановлюємо заголовок вікна
    root.configure(bg='#FFDAB9')  # Налаштовуємо колір фону вікна (світло-персиковий)

    # Додаємо мітку та поле введення для рядка, який буде хешуватися
    tk.Label(root, text="Enter String:", bg='#FFDAB9').grid(row=0, column=0, padx=10, pady=10)
    string_entry = tk.Entry(root, width=50)  # Поле для введення рядка користувачем
    string_entry.grid(row=0, column=1, padx=10, pady=10)

    # Додаємо мітку та поле для відображення шляху до вибраного файлу
    tk.Label(root, text="Select File:", bg='#FFDAB9').grid(row=1, column=0, padx=10, pady=10)
    file_path_var = tk.StringVar()  # Змінна для зберігання шляху до файлу
    tk.Entry(root, textvariable=file_path_var, width=50).grid(row=1, column=1, padx=10, pady=10)

    def browse_file():
        """Функція для вибору файлу через діалогове вікно."""
        file_path = filedialog.askopenfilename()  # Відкриваємо діалогове вікно для вибору файлу
        file_path_var.set(file_path)  # Встановлюємо шлях до вибраного файлу у відповідне поле

    # Додаємо кнопку для відкриття діалогового вікна вибору файлу
    tk.Button(root, text="Browse", command=browse_file, bg='#FFA07A').grid(row=1, column=2, padx=10, pady=10)

    # Додаємо мітку та текстове поле для виведення обчисленого MD5-хеша
    tk.Label(root, text="MD5 Hash:", bg='#FFDAB9').grid(row=2, column=0, padx=10, pady=10)
    hash_output = tk.Text(root, height=2, width=50)  # Поле для відображення хеш-значення
    hash_output.grid(row=2, column=1, padx=10, pady=10)

    def compute_hash():
        """Функція для обчислення MD5-хеша введеного рядка або вибраного файлу."""
        input_str = string_entry.get()  # Отримуємо введений рядок з відповідного поля
        file_path = file_path_var.get()  # Отримуємо шлях до вибраного файлу
        if file_path:
            # Якщо вибрано файл, обчислюємо його хеш
            try:
                # result1 = compute_md5_tree_hash(file_path)
                result2 = compute_hash_from_file_1(file_path)
                # result3 = md5_file_parallel(file_path)
                hash_output.delete('1.0', tk.END)
                hash_output.insert(tk.END, result2)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            # Обчислюємо хеш введеного рядка, навіть якщо він пустий
            result = compute_hash_from_string(input_str)
            hash_output.delete('1.0', tk.END)
            hash_output.insert(tk.END, result)

    # Додаємо кнопку для запуску обчислення MD5-хеша
    tk.Button(root, text="Compute MD5", command=compute_hash, bg='#FFA07A').grid(row=3, column=1, padx=10, pady=10)

    def save_hash():
        """Функція для збереження обчисленого MD5-хеша у файл."""
        hash_value = hash_output.get('1.0', tk.END).strip()  # Отримуємо обчислений хеш з текстового поля
        if hash_value:  # Перевіряємо, чи є хеш для збереження
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt")  # Відкриваємо діалогове вікно для збереження файлу з хешем
            if save_path:
                with open(save_path, 'w') as f:
                    f.write(hash_value)  # Записуємо хеш у вибраний файл
        else:
            # Виводимо попередження, якщо немає хеша для збереження
            messagebox.showwarning("No Hash",
                                   "No hash value to save.")

    # Додаємо кнопку для збереження хеша у файл
    tk.Button(root, text="Save Hash", command=save_hash, bg='#FFA07A').grid(row=4, column=1, padx=10, pady=10)

    # Додаємо мітку та поле для відображення шляху до файлу з хешем для перевірки
    tk.Label(root, text="Hash File:", bg='#FFDAB9').grid(row=5, column=0, padx=10, pady=10)
    hash_file_var = tk.StringVar()  # Змінна для зберігання шляху до файлу з хешем
    tk.Entry(root, textvariable=hash_file_var, width=50).grid(row=5, column=1, padx=10, pady=10)

    def browse_hash_file():
        """Функція для вибору файлу з хешем через діалогове вікно."""
        hash_file_path = filedialog.askopenfilename()  # Відкриваємо діалогове вікно для вибору файлу з хешем
        hash_file_var.set(hash_file_path)  # Встановлюємо шлях до вибраного файлу з хешем

    # Додаємо кнопку для відкриття діалогового вікна вибору файлу з хешем
    tk.Button(root, text="Browse", command=browse_hash_file, bg='#FFA07A').grid(row=5, column=2, padx=10, pady=10)

    def verify_hash():
        """Функція для перевірки цілісності файлу шляхом порівняння хешів."""
        file_path = file_path_var.get()  # Отримуємо шлях до файлу, який потрібно перевірити
        hash_file_path = hash_file_var.get()  # Отримуємо шлях до файлу з очікуваним хешем
        if file_path and hash_file_path:  # Перевіряємо, чи обидва шляхи задані
            try:
                is_valid = verify_file_integrity(file_path, hash_file_path)  # Перевіряємо цілісність файлу
                if is_valid:
                    # Виводимо інформаційне повідомлення, якщо хеші співпадають
                    messagebox.showinfo("Verification",
                                        "File is intact. Hashes match.")
                else:
                    # Виводимо попередження, якщо хеші не співпадають
                    messagebox.showwarning("Verification",
                                           "File has been altered. Hashes do not match.")
            except Exception as e:
                # Виводимо повідомлення про помилку, якщо виникла виключна ситуація
                messagebox.showerror("Error", str(e))
        else:
            # Виводимо попередження, якщо не задано шлях до файлу або файлу з хешем
            messagebox.showwarning("Input Required",
                                   "Please select both a file and a hash file.")

    # Додаємо кнопку для запуску перевірки цілісності файлу
    tk.Button(root, text="Verify Integrity", command=verify_hash, bg='#FFA07A').grid(row=6, column=1, padx=10, pady=10)

    root.mainloop()  # Запускаємо головний цикл програми для обробки подій GUI


if __name__ == "__main__":
    create_gui()  # Викликаємо функцію створення GUI, якщо скрипт запущено напряму
