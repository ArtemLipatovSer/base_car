import tkinter as tk
from tkinter import ttk

class TimeEntry(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind('<KeyRelease>', self.format_time)

    def format_time(self, event):
        text = self.get()
        # Удаляем все нецифровые символы
        digits = ''.join(c for c in text if c.isdigit())
        if len(digits) >= 3:
            formatted = digits[:2] + ':' + digits[2:4]
        elif len(digits) == 2:
            formatted = digits + ':'
        else:
            formatted = digits
        self.delete(0, tk.END)
        self.insert(0, formatted[:5])  # Ограничить до 5 символов

