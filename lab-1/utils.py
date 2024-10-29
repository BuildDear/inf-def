import json
from tkinter import messagebox


def read_config(filename='config.json'):
    """Зчитує параметри з файлу конфігурації."""
    try:
        with open(filename, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        messagebox.showerror("Помилка", f"Файл {filename} не знайдено.")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Помилка", "Помилка у форматі JSON файлу.")
        return None


def save_to_file(file_path, text_output):
    """Записує результати у файл."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_output.get(1.0, "end"))
        messagebox.showinfo("Збережено", "Результати збережено у файл.")
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка під час збереження: {e}")
