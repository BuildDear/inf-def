import tkinter as tk


def create_gui(root):
    elements = {}

    elements['label_n'] = tk.Label(root, text="Введіть кількість псевдовипадкових чисел:", bg='#F4A261', fg='#2A9D8F',
                                   font=("Arial", 14, "bold"))
    elements['label_n'].pack(pady=10)

    elements['entry_n'] = tk.Entry(root, font=("Arial", 12))
    elements['entry_n'].pack(pady=5)

    elements['label_display_limit'] = tk.Label(root, text="Введіть кількість чисел для відображення:", bg='#F4A261',
                                               fg='#2A9D8F', font=("Arial", 14, "bold"))
    elements['label_display_limit'].pack(pady=10)

    elements['entry_display_limit'] = tk.Entry(root, font=("Arial", 12))
    elements['entry_display_limit'].pack(pady=5)

    elements['button_generate'] = tk.Button(root, text="Генерувати", bg='#E76F51', fg='white',
                                            font=("Arial", 12, "bold"))
    elements['button_generate'].pack(pady=10)

    elements['message_label'] = tk.Label(root, text="", bg='#F4A261', fg='#E76F51', font=("Arial", 12))
    elements['message_label'].pack(pady=5)

    elements['status_label'] = tk.Label(root, text="", bg='#F4A261', fg='#E76F51', font=("Arial", 12, "bold"))
    elements['status_label'].pack(pady=5)

    elements['error_label'] = tk.Label(root, text="", bg='#F4A261', fg='#E63946', font=("Arial", 12, "bold"))
    elements['error_label'].pack(pady=5)

    elements['text_output'] = tk.Text(root, height=15, width=60, font=("Courier", 12), bg='#264653', fg='white')
    elements['text_output'].pack(pady=10)

    elements['button_save'] = tk.Button(root, text="Зберегти у файл", bg='#E76F51', fg='white',
                                        font=("Arial", 12, "bold"))
    elements['button_save'].pack(pady=10)

    return elements


def update_status(label, text):
    label.config(text=text)


def update_message(label, text):
    label.config(text=text)


def show_error(label, text):
    label.config(text=text)
