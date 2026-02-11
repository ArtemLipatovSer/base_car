import tkinter as tk

# Создаем основное окно
app = tk.Tk()
app.geometry("600x400")
app.title("Несколько колонок с grid")

# Создаем фрейм внутри окна
frame = tk.Frame(app)
frame.pack(expand=True, fill='both', padx=10, pady=10)

# Конфигурируем grid фрейма: 3 колонки с равным весом
num_columns = 3
for col in range(num_columns):
    frame.grid_columnconfigure(col, weight=1, uniform="col")

# Для строк зададим вес, чтобы они тоже растягивались
# Количество строк зависит от количества элементов и колонок
options = [f"Вариант {i+1}" for i in range(20)]
num_rows = (len(options) + num_columns - 1) // num_columns
for row in range(num_rows):
    frame.grid_rowconfigure(row, weight=1)

# Добавляем чекбоксы в сетку
for index, option in enumerate(options):
    row = index // num_columns
    col = index % num_columns
    chk = tk.Checkbutton(frame, text=option)
    # sticky='nsew' растягивает чекбокс по ширине и высоте ячейки
    chk.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

app.mainloop()
