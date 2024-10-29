import os
import struct
import tkinter as tk
from tkinter import filedialog, messagebox
import binascii
import math
import multiprocessing

CHUNK_SIZE = 1024 * 1024  # 1 MB or adjust as needed

# Constants for MD5
S = [
        7, 12, 17, 22,  # Round 1
    ] * 4 + [
        5, 9, 14, 20,  # Round 2
    ] * 4 + [
        4, 11, 16, 23,  # Round 3
    ] * 4 + [
        6, 10, 15, 21  # Round 4
    ] * 4

K = [int(abs(math.sin(i + 1)) * (2 ** 32)) & 0xFFFFFFFF for i in range(64)]


def left_rotate(x, c):
    """Left rotate a 32-bit integer x by c bits."""
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF


def md5(message):
    """Compute MD5 hash of a message."""
    # Initialize variables:
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

    # Pre-processing
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack('<Q', original_bit_len)

    # Process the message in successive 512-bit chunks
    for offset in range(0, len(message), 64):
        a, b, c, d = A, B, C, D
        chunk = message[offset:offset + 64]
        M = list(struct.unpack('<16I', chunk))

        for i in range(64):
            if 0 <= i <= 15:
                f = (b & c) | (~b & d)
                g = i
            elif 16 <= i <= 31:
                f = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7 * i) % 16

            f = (f + a + K[i] + M[g]) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + left_rotate(f, S[i])) & 0xFFFFFFFF

        # Add this chunk's hash to result so far
        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    # Produce the final hash value
    return struct.pack('<4I', A, B, C, D).hex().upper()


def compute_hash_from_string(input_str):
    message = input_str.encode('utf-8')
    return md5(message)


def compute_hash_from_file(file_path):

    # Ініціалізація для малих файлів
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476
    original_bit_len = 0
    buffer = b''

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            buffer += data
            original_bit_len += len(data) * 8

            # Обробляємо тільки повні блоки 64 байти
            while len(buffer) >= 64:
                chunk = buffer[:64]
                buffer = buffer[64:]
                a, b, c, d = A, B, C, D
                M = list(struct.unpack('<16I', chunk))

                for i in range(64):
                    if 0 <= i <= 15:
                        F = (b & c) | (~b & d)
                        g = i
                    elif 16 <= i <= 31:
                        F = (d & b) | (~d & c)
                        g = (5 * i + 1) % 16
                    elif 32 <= i <= 47:
                        F = b ^ c ^ d
                        g = (3 * i + 5) % 16
                    else:
                        F = c ^ (b | ~d)
                        g = (7 * i) % 16

                    F = (F + a + K[i] + M[g]) & 0xFFFFFFFF
                    a, d, c, b = d, c, b, (b + left_rotate(F, S[i])) & 0xFFFFFFFF

                A = (A + a) & 0xFFFFFFFF
                B = (B + b) & 0xFFFFFFFF
                C = (C + c) & 0xFFFFFFFF
                D = (D + d) & 0xFFFFFFFF

    # Додаємо паддінг до буфера, якщо він не порожній
    buffer += b'\x80'
    while (len(buffer) * 8) % 512 != 448:
        buffer += b'\x00'

    buffer += struct.pack('<Q', original_bit_len)

    # Обробляємо залишковий буфер
    for offset in range(0, len(buffer), 64):
        chunk = buffer[offset:offset + 64]
        a, b, c, d = A, B, C, D
        M = list(struct.unpack('<16I', chunk))

        for i in range(64):
            if 0 <= i <= 15:
                F = (b & c) | (~b & d)
                g = i
            elif 16 <= i <= 31:
                F = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                F = c ^ (b | ~d)
                g = (7 * i) % 16

            F = (F + a + K[i] + M[g]) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + left_rotate(F, S[i])) & 0xFFFFFFFF

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    return struct.pack('<4I', A, B, C, D).hex().upper()


def verify_file_integrity(file_path, hash_file_path):
    computed_hash = compute_hash_from_file(file_path)
    with open(hash_file_path, 'r') as f:
        original_hash = f.read().strip().upper()
    return computed_hash == original_hash


# Tkinter GUI

def create_gui():
    root = tk.Tk()
    root.title("MD5 Hash Generator and Verifier")
    root.configure(bg='#FFDAB9')  # Warm peach color

    # String Input
    tk.Label(root, text="Enter String:", bg='#FFDAB9').grid(row=0, column=0, padx=10, pady=10)
    string_entry = tk.Entry(root, width=50)
    string_entry.grid(row=0, column=1, padx=10, pady=10)

    # File Input
    tk.Label(root, text="Select File:", bg='#FFDAB9').grid(row=1, column=0, padx=10, pady=10)
    file_path_var = tk.StringVar()
    tk.Entry(root, textvariable=file_path_var, width=50).grid(row=1, column=1, padx=10, pady=10)

    def browse_file():
        file_path = filedialog.askopenfilename()
        file_path_var.set(file_path)

    tk.Button(root, text="Browse", command=browse_file, bg='#FFA07A').grid(row=1, column=2, padx=10, pady=10)

    # Hash Output
    tk.Label(root, text="MD5 Hash:", bg='#FFDAB9').grid(row=2, column=0, padx=10, pady=10)
    hash_output = tk.Text(root, height=2, width=50)
    hash_output.grid(row=2, column=1, padx=10, pady=10)

    def compute_hash():
        input_str = string_entry.get()
        file_path = file_path_var.get()
        print(f"File path: {file_path}")  # Debugging print
        if input_str:
            result = compute_hash_from_string(input_str)
            hash_output.delete('1.0', tk.END)
            hash_output.insert(tk.END, result)
        elif file_path:
            try:
                result = compute_hash_from_file(file_path)
                hash_output.delete('1.0', tk.END)
                hash_output.insert(tk.END, result)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Required", "Please enter a string or select a file.")

    tk.Button(root, text="Compute MD5", command=compute_hash, bg='#FFA07A').grid(row=3, column=1, padx=10, pady=10)

    # Save Hash
    def save_hash():
        hash_value = hash_output.get('1.0', tk.END).strip()
        if hash_value:
            save_path = filedialog.asksaveasfilename(defaultextension=".txt")
            if save_path:
                with open(save_path, 'w') as f:
                    f.write(hash_value)
                messagebox.showinfo("Saved", f"Hash saved to {save_path}")
        else:
            messagebox.showwarning("No Hash", "No hash value to save.")

    tk.Button(root, text="Save Hash", command=save_hash, bg='#FFA07A').grid(row=4, column=1, padx=10, pady=10)

    # Verify Integrity
    tk.Label(root, text="Hash File:", bg='#FFDAB9').grid(row=5, column=0, padx=10, pady=10)
    hash_file_var = tk.StringVar()
    tk.Entry(root, textvariable=hash_file_var, width=50).grid(row=5, column=1, padx=10, pady=10)

    def browse_hash_file():
        hash_file_path = filedialog.askopenfilename()
        hash_file_var.set(hash_file_path)

    tk.Button(root, text="Browse", command=browse_hash_file, bg='#FFA07A').grid(row=5, column=2, padx=10, pady=10)

    def verify_hash():
        file_path = file_path_var.get()
        hash_file_path = hash_file_var.get()
        if file_path and hash_file_path:
            try:
                is_valid = verify_file_integrity(file_path, hash_file_path)
                if is_valid:
                    messagebox.showinfo("Verification", "File is intact. Hashes match.")
                else:
                    messagebox.showwarning("Verification", "File has been altered. Hashes do not match.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Required", "Please select both a file and a hash file.")

    tk.Button(root, text="Verify Integrity", command=verify_hash, bg='#FFA07A').grid(row=6, column=1, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()