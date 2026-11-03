"""Графический интерфейс генератора паролей (tkinter)."""
import tkinter as tk
from tkinter import messagebox, ttk

from generator import (MAX_LENGTH, MIN_LENGTH, PasswordParamsError,
                       estimate_strength, generate_password)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генератор паролей")
        self.resizable(False, False)

        self.length = tk.IntVar(value=12)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)
        self.password = tk.StringVar()
        self.strength = tk.StringVar(value="Надёжность: —")

        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=15)
        frame.grid()

        ttk.Label(frame, text="Длина пароля:").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(frame, from_=MIN_LENGTH, to=MAX_LENGTH,
                    textvariable=self.length, width=6).grid(row=0, column=1, sticky="w")

        ttk.Checkbutton(frame, text="Строчные буквы (a-z)",
                        variable=self.use_lower).grid(row=1, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(frame, text="Заглавные буквы (A-Z)",
                        variable=self.use_upper).grid(row=2, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(frame, text="Цифры (0-9)",
                        variable=self.use_digits).grid(row=3, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(frame, text="Спецсимволы (!@#$...)",
                        variable=self.use_symbols).grid(row=4, column=0, columnspan=2, sticky="w")

        ttk.Button(frame, text="Сгенерировать",
                   command=self.on_generate).grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Entry(frame, textvariable=self.password, width=36,
                  state="readonly").grid(row=6, column=0, columnspan=2)
        ttk.Label(frame, textvariable=self.strength).grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Копировать",
                   command=self.on_copy).grid(row=8, column=0, columnspan=2)

    def on_generate(self):
        try:
            pwd = generate_password(
                self.length.get(), self.use_lower.get(), self.use_upper.get(),
                self.use_digits.get(), self.use_symbols.get(),
            )
        except (PasswordParamsError, tk.TclError) as err:
            messagebox.showerror("Ошибка", str(err))
            return
        self.password.set(pwd)
        entropy, label = estimate_strength(pwd)
        self.strength.set(f"Надёжность: {label} ({entropy} бит)")

    def on_copy(self):
        if not self.password.get():
            messagebox.showinfo("Копирование", "Сначала сгенерируйте пароль")
            return
        self.clipboard_clear()
        self.clipboard_append(self.password.get())
        messagebox.showinfo("Копирование", "Пароль скопирован в буфер обмена")


if __name__ == "__main__":
    App().mainloop()
