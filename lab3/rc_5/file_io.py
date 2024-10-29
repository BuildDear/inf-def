# Функція encrypt_file виконує шифрування файлу.
def encrypt_file(input_filename, output_filename, rc5_instance):
    rc5_instance.encrypt_file(input_filename,
                              output_filename)  # Викликаємо метод encrypt_file класу RC5CBCPad для шифрування файлу
    # з назвою input_filename і збереження результату в output_filename.


# Функція decrypt_file виконує розшифрування файлу.
def decrypt_file(input_filename, output_filename, rc5_instance):
    rc5_instance.decrypt_file(input_filename,
                              output_filename)  # Викликаємо метод decrypt_file класу RC5CBCPad для розшифрування
    # файлу з назвою input_filename і збереження результату в output_filename.
