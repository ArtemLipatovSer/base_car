import tkinter as tk
from tkinter import ttk
import requests
import threading

                                # АВТОМАТИЧЕСКИЕ ПОДСКАЗКИ ВВОДА АДРЕСА
class AutoAdress(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = "5da87d9142e255c5afdc7f7d962cf4979e57bc71"
        self.var = tk.StringVar()
        self["textvariable"] = self.var

        self.var.trace('w', self.changed)
        self.bind("<Down>", self.move_down)
        self.bind("<Return>", self.on_enter)
        self.bind("<Escape>", self.close_listbox)

        self.listbox_up = False
        self.search_timer = None
        self.search_delay = 0.5
        self.programmatic_change = False  # Флаг для отслеживания программных изменений

    def changed(self, name, index, mode):
        # Игнорируем изменения, сделанные программно
        if self.programmatic_change:
            return

        # Отменяем предыдущий таймер
        if self.search_timer:
            self.search_timer.cancel()

        # Запускаем новый таймер
        if self.var.get(): # Если есть введенное значение, в поле Var

            self.search_timer = threading.Timer(self.search_delay, self.fetch_suggestions)
            self.search_timer.start()
        else:
            self.close_listbox()

    def fetch_suggestions(self):
        query = self.var.get()
        if not query:
            return

        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Token {self.api_key}'
            }

            data = {
                "query": query,
                "count": 5,
                "locations_boost": [{
                    "kladr_id": "33"
                }]
            }

            response = requests.post(
                'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address',
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                suggestions = response.json()['suggestions']
                addresses = [s['value'] for s in suggestions]
                self.after(0, self.update_listbox, addresses)
        except Exception as e:
            print(f"Ошибка при получении подсказок: {e}")

    def update_listbox(self, addresses):
        if addresses:
            if not self.listbox_up:
                self.open_listbox()
            self.listbox.delete(0, tk.END)
            for addr in addresses:
                self.listbox.insert(tk.END, addr)
        else:
            self.close_listbox()

    # Обрабатывание команд нажатия клавиш
    def selection(self, event):
        if self.listbox_up:
            selection = self.listbox.curselection() # Выбираем элемент, который выбрали в listbox
            if selection:
                # Временно отключаем отслеживание изменений
                self.programmatic_change = True
                self.var.set(self.listbox.get(selection[0]))
                self.programmatic_change = False
                self.close_listbox()
                if event.keysym == 'Return':
                    return "break"
                self.focus_set()
                self.icursor(tk.END)

    def move_down(self, event):
        if self.listbox_up:
            self.listbox.focus()
            if self.listbox.size() > 0:
                self.listbox.selection_set(0)
                self.listbox.activate(0)
        return 'break'

    def on_enter(self, event):
        if self.listbox_up:
            selection = self.listbox.curselection()
            if selection:
                # Временно отключаем отслеживание изменений
                self.programmatic_change = True
                self.var.set(self.listbox.get(selection[0]))
                self.programmatic_change = False
                self.close_listbox()
            else:
                self.close_listbox()
        return 'break'

    def open_listbox(self):
        if not self.listbox_up:
            self.listbox = tk.Listbox(width=self["width"])

            self.listbox.bind("<ButtonRelease-1>", self.selection)
            self.listbox.bind("<Return>", self.selection)
            self.listbox.bind("<Escape>", self.close_listbox)

            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            self.listbox.config(height=5)
            self.listbox.place(x=x, y=y)

            self.listbox_up = True

    def close_listbox(self, event=None):
        if self.listbox_up:
            self.listbox.destroy()
            self.listbox_up = False
        return 'break'
