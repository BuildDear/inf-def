import tkinter as tk  # Імпортуємо tkinter для створення графічного інтерфейсу
from tkinter import filedialog, messagebox, \
    simpledialog  # Імпортуємо компоненти для роботи з файлами, повідомленнями та діалогами
from tkinter.scrolledtext import ScrolledText  # Імпортуємо ScrolledText для створення текстової області з прокруткою
from aMD5 import MD5  # Імпортуємо клас MD5 з вашого файлу amain
from RC5CBCPadLogic import RC5CBCPad  # Імпортуємо клас RC5CBCPad для шифрування та дешифрування
from LemerGen import LemerGenerator  # Імпортуємо генератор Лемера для створення вектора ініціалізації (IV)


# Головний клас програми для шифрування та дешифрування
class EncryptionApp:
    def __init__(self, root):
        self.root = root  # Зберігаємо головне вікно програми (корінь)
        self.root.title("RC5 CBC Pad Encryption/Decryption")  # Встановлюємо заголовок вікна
        self.root.geometry("1000x800")  # Встановлюємо розміри вікна

        # Налаштування кольорової схеми для інтерфейсу
        self.root.configure(bg="#ffa386")  # Встановлюємо фон вікна в теплих кольорах

        self.saved_password = None  # Перемінна для збереження введеного пароля

        # Створюємо мітку (label) для інструкції користувачу з введення пароля
        self.passcode_label = tk.Label(root, text="Enter the password for encryption/decryption:", bg="#FFFAF0",
                                       fg="#000000")
        self.passcode_label.pack(pady=10)  # Додаємо відступ між елементами інтерфейсу

        # Створюємо поле введення (entry) для пароля, символи виводяться як '*'
        self.passcode_entry = tk.Entry(root, show='*', bg="#FFF5EE", fg="#8B4513")
        self.passcode_entry.pack()

        # Створюємо кнопку для шифрування тексту
        self.encrypt_text_button = tk.Button(root, text="Encrypt Text", command=self.encrypt_text, bg="#CD5C5C",
                                             fg="white")
        self.encrypt_text_button.pack(pady=10)

        # Створюємо кнопку для дешифрування тексту
        self.decrypt_text_button = tk.Button(root, text="Decrypt Text", command=self.decrypt_text, bg="#F08080",
                                             fg="white")
        self.decrypt_text_button.pack(pady=10)

        # Створюємо кнопку для шифрування файлу
        self.encrypt_file_button = tk.Button(root, text="Encrypt a File", command=self.encrypt_file, bg="#FF7F50",
                                             fg="white")
        self.encrypt_file_button.pack(pady=10)

        # Створюємо кнопку для дешифрування файлу
        self.decrypt_file_button = tk.Button(root, text="Decrypt a File", command=self.decrypt_file, bg="#FF6347",
                                             fg="white")
        self.decrypt_file_button.pack(pady=10)

        # Створюємо мітку для виведення результатів
        self.output_label = tk.Label(root, text="Output:", bg="#FFFAF0", fg="#8B4513")
        self.output_label.pack(pady=10)

        # Створюємо текстову область з прокруткою для виведення результатів
        self.output_text = ScrolledText(root, wrap=tk.WORD, height=20, bg="#FFF5EE", fg="#8B4513")
        self.output_text.pack()

    # Метод для отримання екземпляру RC5 з введеним паролем
    def get_rc5_instance(self):
        passcode = self.passcode_entry.get()  # Отримуємо пароль з поля введення
        if not passcode:  # Якщо пароль не введено
            messagebox.showerror("Error", "Please enter a password.")  # Виводимо повідомлення про помилку
            return None  # Повертаємо None, оскільки неможливо продовжити без пароля
        self.saved_password = passcode  # Зберігаємо пароль для подальшого використання
        md5_service = MD5()  # Створюємо екземпляр класу MD5
        key = md5_service.hexdigest().encode('utf-8')[:16]  # Створюємо 16-байтовий ключ для шифрування
        return RC5CBCPad(key, word_size=16,
                         num_rounds=20)  # Створюємо екземпляр RC5CBCPad з параметрами w=16, r=20, b=16

    # Метод для шифрування файлу
    def encrypt_file(self):
        rc5 = self.get_rc5_instance()  # Отримуємо екземпляр RC5
        if rc5:
            # Відкриваємо діалогове вікно для вибору файлу для шифрування
            input_filename = filedialog.askopenfilename(title="Select File to Encrypt")
            if not input_filename:  # Якщо файл не вибрано
                return

            # Відкриваємо діалогове вікно для збереження зашифрованого файлу
            output_filename = filedialog.asksaveasfilename(title="Save Encrypted File As")
            if not output_filename:  # Якщо файл для збереження не вибрано
                return

            try:
                # Викликаємо метод шифрування файлу
                rc5.encrypt_file(input_filename, output_filename)
                # Виводимо результат у текстову область
                self.output_text.insert(tk.END, f"File '{input_filename}' encrypted to '{output_filename}'\n")
                messagebox.showinfo("Success",
                                    "Password has been saved and file is encrypted.")  # Виводимо повідомлення про успіх
            except Exception as e:  # Якщо виникла помилка
                messagebox.showerror("Error", str(e))  # Виводимо повідомлення про помилку

    # Метод для дешифрування файлу
    def decrypt_file(self):
        # Відкриваємо діалогове вікно для вибору файлу для дешифрування
        input_filename = filedialog.askopenfilename(title="Select File to Decrypt")
        if not input_filename:  # Якщо файл не вибрано
            return

        # Відкриваємо діалогове вікно для збереження дешифрованого файлу
        output_filename = filedialog.asksaveasfilename(title="Save Decrypted File As")
        if not output_filename:  # Якщо файл для збереження не вибрано
            return

        # Перевіряємо, чи є збережений пароль
        if not self.saved_password:
            messagebox.showerror("Error",
                                 "No password has been saved for decryption.")  # Виводимо повідомлення про помилку
            return

        # Запитуємо пароль для дешифрування
        entered_passcode = simpledialog.askstring("Password Check", "Enter the password to decrypt:")
        if entered_passcode != self.saved_password:  # Якщо пароль невірний
            messagebox.showerror("Error", "Incorrect password.")  # Виводимо повідомлення про помилку
            return

        # Отримуємо екземпляр RC5 після успішної перевірки пароля
        rc5 = self.get_rc5_instance()
        if rc5:
            try:
                # Викликаємо метод дешифрування файлу
                rc5.decrypt_file(input_filename, output_filename)
                # Виводимо результат у текстову область
                self.output_text.insert(tk.END, f"File '{input_filename}' decrypted to '{output_filename}'\n")
            except Exception as e:  # Якщо виникла помилка
                messagebox.showerror("Error", str(e))  # Виводимо повідомлення про помилку

    # Метод для шифрування тексту
    def encrypt_text(self):
        rc5 = self.get_rc5_instance()  # Отримуємо екземпляр RC5
        if rc5:
            # Запитуємо у користувача текст для шифрування
            plaintext = tk.simpledialog.askstring("Input", "Enter plaintext to encrypt:")
            if not plaintext:  # Якщо текст не введено
                return

            try:
                # Створюємо seed для генератора Лемера
                seed = rc5.generate_seed()
                lemer_generator = LemerGenerator(seed)  # Створюємо екземпляр генератора Лемера
                iv = lemer_generator.get_bytes(8)  # Отримуємо 8 байтів для IV
                ciphertext = rc5.encrypt_console(plaintext.encode('utf-8'), iv)  # Шифруємо текст

                # Виводимо зашифрований текст у текстову область
                self.output_text.insert(tk.END, f'Encrypted text (hex): {(iv + ciphertext).hex()}\n')
                messagebox.showinfo("Success",
                                    "Password has been saved and text is encrypted.")  # Виводимо повідомлення про успіх
            except Exception as e:  # Якщо виникла помилка
                messagebox.showerror("Error", str(e))  # Виводимо повідомлення про помилку

    # Метод для дешифрування тексту
    def decrypt_text(self):
        if not self.saved_password:  # Перевіряємо, чи є збережений пароль
            messagebox.showerror("Error",
                                 "No password has been saved for decryption.")  # Виводимо повідомлення про помилку
            return

        # Запитуємо пароль для дешифрування
        entered_passcode = simpledialog.askstring("Password Check", "Enter the password to decrypt:")
        if entered_passcode != self.saved_password:  # Якщо пароль невірний
            messagebox.showerror("Error", "Incorrect password.")  # Виводимо повідомлення про помилку
            return

        rc5 = self.get_rc5_instance()  # Отримуємо екземпляр RC5
        if rc5:
            # Запитуємо у користувача шифротекст для дешифрування
            ciphertext_input = tk.simpledialog.askstring("Input", "Enter ciphertext to decrypt (hex string):")
            if not ciphertext_input:  # Якщо шифротекст не введено
                return

            try:
                ciphertext = bytes.fromhex(ciphertext_input)  # Перетворюємо шифротекст у байти
                iv = ciphertext[:8]  # Отримуємо IV (перші 8 байтів)
                ciphertext_body = ciphertext[8:]  # Отримуємо решту шифротексту
                decrypted = rc5.decrypt_console(ciphertext_body, iv)  # Дешифруємо текст
                # Виводимо дешифрований текст у текстову область
                self.output_text.insert(tk.END, f'Decrypted text: {decrypted.decode("utf-8")}\n')
            except ValueError as e:  # Якщо виникла помилка перетворення
                messagebox.showerror("Error", f"Decryption failed: {e}")  # Виводимо повідомлення про помилку
            except Exception as e:  # Інші можливі помилки
                messagebox.showerror("Error", str(e))  # Виводимо повідомлення про помилку


# Створюємо і запускаємо головне вікно програми
if __name__ == "__main__":
    root = tk.Tk()  # Створюємо головне вікно
    app = EncryptionApp(root)  # Створюємо екземпляр нашого класу з головним вікном
    root.mainloop()  # Запускаємо головний цикл програми
