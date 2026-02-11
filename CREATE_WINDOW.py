import tkinter as tk
from itertools import count
from tkinter import ttk
from tkcalendar import DateEntry

import PARAMS
import disabled_widget
from Address import AutoAdress
from TimeEntry import TimeEntry

class СreateInfoWindow(tk.Tk):
    def __init__(self,):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.title('Внесение записи')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ПОМЕЩАЕМ ВСЕ В ОДИН КОНТЕНЕР, РАТЯГИВАЕМ ЕГО И ПОСЛЕ В ЭТОТ КОНТЕНЕР ПОМЕЩАЕМ КАНВАС (ДЛЯ СКРОЛЛА)
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky='nsew')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        canvas = tk.Canvas(container)
        canvas.grid(row=0, column=0, sticky='nsew')

        # ДЕЛАЕМ СКРОЛЛ
        scrollbar_v = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar_v.grid(row=0, column=1, sticky='ns')
        scrollbar_g = ttk.Scrollbar(container, orient='horizontal', command=canvas.xview)
        scrollbar_g.grid(row=1, column=0, sticky='we')
        canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_g.set)

        # ВНУТРИ КАНВАС СОЗДАЕМ ЕЩЕ ОДИН ФРЕЙМ, В КОТОРОМ БУДУТ РАЗМЕЩАТЬСЯ ОСТАЛЬНЫЕ ВИДЖЕТЫ
        root_win = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=root_win, anchor='w')
        # Настройка колонок и строк в root_win для поддержки нескольких колонок и растяжения
        root_win.grid_columnconfigure(0, weight=1)  # Колонка 0: для frame_four
        root_win.grid_columnconfigure(1, weight=1)  # Колонка 1: для frame_five
        root_win.grid_rowconfigure(3, weight=1)  # Строка 3: растяжение по высоте для этих фреймов
        # ОБРАБАТЫВАЕТ ИЗМЕНЕНИЕ ЭКРАНА
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        root_win.bind("<Configure>", on_frame_configure)


        # ПЕРВЫЙ ФРЕЙМ
        frame_one = ttk.Frame(root_win)
        frame_one.grid(row=0, column=0, sticky='ew')

        label = ttk.Label(frame_one, text='Дата вызова:')
        label.grid(row=0, column=0, padx=(20, 5), pady=10, sticky='w')
        date_call = DateEntry(frame_one, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_call.grid(row=0, column=1, padx=(5, 20), pady=10, sticky='w')

        label = ttk.Label(frame_one, text='Район:')
        label.grid(row=0, column=2, padx=(20, 5), pady=10, sticky='w')
        combo_rayon = ttk.Combobox(frame_one, values=PARAMS.RAYONS, width=20)
        combo_rayon.grid(row=0, column=3, padx=(5, 20), pady=10, sticky='w')
        combo_rayon.current(0)  # Выбираем первый элемент по умолчанию

        label = ttk.Label(frame_one, text='Адрес:')
        label.grid(row=0, column=4, padx=(20, 5), pady=10, sticky='w')
        address = AutoAdress( frame_one, width=80)
        address.grid(row=0, column=5, padx=(20, 5), pady=10, sticky='w')

        label = ttk.Label(frame_one, text='ФИО Диспетчера:')
        label.grid(row=0, column=6, padx=(20, 5), pady=10, sticky='w')
        combo_disp = ttk.Combobox(frame_one, values=PARAMS.DISPATCHER, width=20)
        combo_disp.grid(row=0, column=7, padx=(5, 20), pady=10, sticky='w')
        combo_disp.current(0)

        label = ttk.Label(frame_one, text='Номер караула:')
        label.grid(row=0, column=8, padx=(20, 5), pady=10, sticky='w')
        combo_caraul = ttk.Combobox(frame_one, values=PARAMS.CARAUL, width=10)
        combo_caraul.grid(row=0, column=9, padx=(5, 20), pady=10, sticky='w')
        combo_caraul.current(0)

        # ВТОРОЙ ФРЕЙМ
        frame_two = ttk.Frame(root_win)
        frame_two.grid(row=1, column=0)

        label = ttk.Label(frame_two, text='Тип вызова:')
        label.grid(row=0, column=0, padx=(20, 5), pady=10)
        combo_type_call = ttk.Combobox(frame_two, values=PARAMS.TYPE_CALL, width=20)
        combo_type_call.grid(row=0, column=1, padx=(5, 20), pady=10)
        combo_type_call.current(0)

        def fun_type_call(event):
            arr_frame_disabled = [frame_three_three, frame_three_four, frame_three_eight, frame_three_nine, frame_fire_end,]
            if combo_type_call.get() == 'Ложный':
                disabled_widget.frame_state_set(arr_frame_disabled, 'disabled')
            else:
                disabled_widget.frame_state_set(arr_frame_disabled, 'enabled')

        combo_type_call.bind('<<ComboboxSelected>>', fun_type_call)

        label = ttk.Label(frame_two, text='Номер вызова')
        label.grid(row=0, column=2, padx=(20, 5), pady=10)
        combo_number_call = ttk.Combobox(frame_two, values=PARAMS.NUMBER_CALL, width=10)
        combo_number_call.grid(row=0, column=3, padx=(5, 20), pady=10)
        combo_number_call.current(0)

        # ТРЕТИЙ ФРЕЙМ
        frame_three = ttk.Frame(root_win, borderwidth=2, relief='groove')
        frame_three.grid(row=2, column=0, padx=20)

        # ГРУППА ПОКАЗАТЕЛИ ОПЕРАТИВНОГО РЕАГИРОВАНИЯ
        label = ttk.Label(frame_three, text='Показатели оперативного реагирования', font=('Arial',10))
        label.grid(row=0, column=0, columnspan=7, padx=5, pady=5)

        # ПЕРВАЯ РАМКА (СООБЩЕНИЕ)
        frame_three_one = ttk.Frame(frame_three, borderwidth=2, relief='groove')
        frame_three_one.grid(row=1, column=0, padx=5, pady=5)

        label = ttk.Label(frame_three_one, text='Сообщение', font=('Arial', 10))
        label.grid(row=0, column=0, columnspan=2)
        label = ttk.Label(frame_three_one, text='Дата:')
        label.grid(row=1, column=0, padx=5, pady=5 )
        date_msg = DateEntry(frame_three_one, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_msg.grid(row=1, column=1, padx=5, pady=5)
        label = ttk.Label(frame_three_one, text='Время:')
        label.grid(row=2, column=0, padx=5, pady=5)
        time_msg = TimeEntry(frame_three_one, width=13)
        time_msg.grid(row=2, column=1, padx=5, pady=5)

        # ВТОРАЯ РАМКА (ВЫЕЗД)
        frame_three_two = ttk.Frame(frame_three, borderwidth=2, relief='groove')
        frame_three_two.grid(row=1, column=1, padx=5, pady=5)

        label = ttk.Label(frame_three_two, text='Выезд', font=('Arial', 10))
        label.grid(row=0, column=0, columnspan=2)
        label = ttk.Label(frame_three_two, text='Дата:')
        label.grid(row=1, column=0, padx=5, pady=5)
        date_drive = DateEntry(frame_three_two, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_drive.grid(row=1, column=1, padx=5, pady=5)
        label = ttk.Label(frame_three_two, text='Время:')
        label.grid(row=2, column=0, padx=5, pady=5)
        time_drive = TimeEntry(frame_three_two, width=13)
        time_drive.grid(row=2, column=1, padx=5, pady=5)

        # ТРЕТЬЯ РАМКА (ЛОКАЛИЗАЦИЯ)
        frame_three_three = ttk.Frame(frame_three, borderwidth=2, relief='groove')
        frame_three_three.grid(row=2, column=0, padx=5, pady=5)

        label = ttk.Label(frame_three_three, text='Локализация', font=('Arial', 10))
        label.grid(row=0, column=0, columnspan=2)
        label = ttk.Label(frame_three_three, text='Дата:')
        label.grid(row=1, column=0, padx=5, pady=5)
        date_loc = DateEntry(frame_three_three, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_loc.grid(row=1, column=1, padx=5, pady=5)
        label = ttk.Label(frame_three_three, text='Время:')
        label.grid(row=2, column=0, padx=5, pady=5)
        time_loc = TimeEntry(frame_three_three, width=13)
        time_loc.grid(row=2, column=1, padx=5, pady=5)

        # ЧЕТВЕРТАЯ РАМКА (ЛИКВИДАЦИЯ)
        frame_three_four = ttk.Frame(frame_three, borderwidth=2, relief='groove')
        frame_three_four.grid(row=2, column=1, padx=5, pady=5)

        label = ttk.Label(frame_three_four, text='Ликвидация', font=('Arial', 10))
        label.grid(row=0, column=0, columnspan=2)
        label = ttk.Label(frame_three_four, text='Дата:')
        label.grid(row=1, column=0, padx=5, pady=5)
        date_lic = DateEntry(frame_three_four, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_lic.grid(row=1, column=1, padx=5, pady=5)
        label = ttk.Label(frame_three_four, text='Время:')
        label.grid(row=2, column=0, padx=5, pady=5)
        time_lic = TimeEntry(frame_three_four, width=13)
        time_lic.grid(row=2, column=1, padx=5, pady=5)

        # ПЯТАЯ РАМКА (ВЕРНУЛИ С ПУТИ)
        frame_three_five = ttk.Frame(frame_three, borderwidth=2, relief='groove')
        frame_three_five.grid(row=1, column=3, padx=5, pady=5)

        label = ttk.Label(frame_three_five, text='Вернули в пути следования', font=('Arial', 10))
        label.grid(row=0, column=0, columnspan=2)
        # ДЕЛАЕМ ЧЕКБОКС ПРИ СЛУЧАЕ ЧТО ВЕРНУЛИ С ПУТИ
        checkbox_go_back_value = tk.BooleanVar()
        checkbox_go_back = ttk.Checkbutton(frame_three_five, variable=checkbox_go_back_value)
        checkbox_go_back.grid(row=1, column=0, columnspan=2)

        # ОБРАБАТЫВАЕМ ДЕЙСТВИЕ ПРИ НАЖАТИИ ЧЕКБОКСА "ВЕРНУЛИ В ПУТИ СЛЕДОВАНИЯ", ЕСЛИ ОН НАЖАТ ТО БЕРЕМ МАССИВ ФРЕЙМОВ КОТОРЫЕ НУЖНЫ
        # И ОЧИЩАЕМ ИХ И ЗАТЕМ ДЕАКТИВИРУЕМ

        def fun_checkbox_go_back():
            arr_frame_disabled = [frame_three_three, frame_three_four, frame_three_six, frame_three_nine, frame_three_eight, frame_fire_end,]
            if checkbox_go_back_value.get():
                disabled_widget.frame_state_set(arr_frame_disabled, 'disabled')
            else:
                if combo_type_call.get() == 'Ложный':
                    disabled_widget.frame_state_set([frame_three_six], 'enabled')
                else:
                    disabled_widget.frame_state_set(arr_frame_disabled, 'enabled')

        checkbox_go_back.config(command=fun_checkbox_go_back)

        # ШЕСТАЯ РАМКА (ПРИБЫТИЕ)
        frame_three_six = ttk.Frame(frame_three, borderwidth=2, relief='groove')
        frame_three_six.grid(row=1, column=4, padx=5, pady=5)

        label = ttk.Label(frame_three_six, text='Прибытие', font=('Arial', 10))
        label.grid(row=0, column=0, columnspan=2)
        label = ttk.Label(frame_three_six, text='Дата:')
        label.grid(row=1, column=0, padx=5, pady=5)
        date_came = DateEntry(frame_three_six, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_came.grid(row=1, column=1, padx=5, pady=5)
        label = ttk.Label(frame_three_six, text='Время:')
        label.grid(row=2, column=0, padx=5, pady=5)
        time_came = TimeEntry(frame_three_six, width=13)
        time_came.grid(row=2, column=1, padx=5, pady=5)

        # СЕДЬМАЯ РАМКА (ЛИКВИДАЦИЯ ПОСЛЕДСТВИЙ ПОЖАРА)
        frame_three_seven = ttk.Frame(frame_three, borderwidth=2, relief='groove')
        frame_three_seven.grid(row=2, column=3, padx=5, pady=5, columnspan=2, sticky='nsew')

        frame_fire_end = ttk.Frame(frame_three_seven)
        frame_fire_end.place(relx=0.5, rely=0.5, anchor='center')

        label = ttk.Label(frame_fire_end, text='Ликвидация последствий пожара', font=('Arial', 10))
        label.grid(row=0, column=0, columnspan=2)
        label = ttk.Label(frame_fire_end, text='Дата:')
        label.grid(row=1, column=0, padx=5, pady=5)
        date_fire_end = DateEntry(frame_fire_end, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_fire_end.grid(row=1, column=1, padx=5, pady=5)
        label = ttk.Label(frame_fire_end, text='Время:')
        label.grid(row=2, column=0, padx=5, pady=5)
        time_fire_end = TimeEntry(frame_fire_end, width=13)
        time_fire_end.grid(row=2, column=1, padx=5, pady=5)

        # ВОСЬМАЯ РАМКА (ПОТУШЕНО ДО ПРИБЫТИЯ)
        frame_three_eight = ttk.Frame(frame_three, borderwidth=2, relief='groove')
        frame_three_eight.grid(row=1, column=5, padx=5, pady=5)
        label = ttk.Label(frame_three_eight, text='Ликвидация до прибытия', font=('Arial', 10))
        label.grid(row=0, column=0, columnspan=2)
        # ДЕЛАЕМ ЧЕКБОКС ПРИ СЛУЧАЕ ЧТО ВЕРНУЛИ С ПУТИ
        checkbox_before_came_value = tk.BooleanVar()
        checkbox_before_came = ttk.Checkbutton(frame_three_eight, variable=checkbox_before_came_value)
        checkbox_before_came.grid(row=1, column=0, columnspan=2)

        # ОБРАБАТЫВАЕМ ДЕЙСТВИЕ ПРИ НАЖАТИИ ЧЕКБОКСА "ПОТУШЕНО ДО ПРИБЫТИЯ", ЕСЛИ ОН НАЖ ТО БЕРЕМ МАССИВ ФРЕЙМОВ КОТОРЫЕ НУЖНЫ
        # И ОЧИЩАЕМ ИХ И ЗАТЕМ ДЕАКТИВИРУЕМ

        def fun_checkbox_before_came():
            arr_frame_disabled = [frame_three_three, frame_three_four, frame_three_five,
                                  frame_fire_end, frame_three_nine]
            if checkbox_before_came_value.get():
                disabled_widget.frame_state_set(arr_frame_disabled, 'disabled')
            else:
                disabled_widget.frame_state_set(arr_frame_disabled, 'enabled')

        checkbox_before_came.config(command=fun_checkbox_before_came)

        # ДЕВЯТАЯ РАМКА (ПОДАЧА 1-го СТВОЛА)
        frame_three_nine = ttk.Frame(frame_three, borderwidth=2, relief='groove')
        frame_three_nine.grid(row=1, column=6, padx=5, pady=5)

        label = ttk.Label(frame_three_nine, text='Подача первого ствола', font=('Arial', 10))
        label.grid(row=0, column=0, columnspan=2)
        label = ttk.Label(frame_three_nine, text='Дата:')
        label.grid(row=1, column=0, padx=5, pady=5)
        date_fire_barrel = DateEntry(frame_three_nine, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_fire_barrel.grid(row=1, column=1, padx=5, pady=5)
        label = ttk.Label(frame_three_nine, text='Время:')
        label.grid(row=2, column=0, padx=5, pady=5)
        time_fire_barrel = TimeEntry(frame_three_nine, width=13)
        time_fire_barrel.grid(row=2, column=1, padx=5, pady=5)

        # ДЕСЯТАЯ РАМКА (ВОЗВРАЩЕНИЕ В ПОДРАЗДЕЛЕНИЕ)
        frame_three_ten = ttk.Frame(frame_three, borderwidth=2, relief='groove')
        frame_three_ten.grid(row=2, column=5, padx=5, pady=5, columnspan=2, sticky='nsew')

        frame_go_home = ttk.Frame(frame_three_ten)
        frame_go_home.place(relx=0.5, rely=0.5, anchor='center')

        label = ttk.Label(frame_go_home, text='Возвращение в подразделение', font=('Arial', 10))
        label.grid(row=0, column=0, columnspan=2)
        label = ttk.Label(frame_go_home, text='Дата:')
        label.grid(row=1, column=0, padx=5, pady=5)
        date_go_home = DateEntry(frame_go_home, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_go_home.grid(row=1, column=1, padx=5, pady=5)
        label = ttk.Label(frame_go_home, text='Время:')
        label.grid(row=2, column=0, padx=5, pady=5)
        time_go_home = TimeEntry(frame_go_home, width=13)
        time_go_home.grid(row=2, column=1, padx=5, pady=5)
        # КОНЕЦ ГРУППЫ ПОКАЗАТЕЛИ ОПЕРАТИВНОГО РЕАГИРОВАНИЯ

        # ЧЕТВЕРТЫЙ ФРЕЙМ
        # ПРИВЛЕКАЕМАЯ ТЕХНИКА ЧАСТИ
        frame_four = tk.Frame(root_win, borderwidth=2, relief='groove', width=700)
        frame_four.grid(row=3, pady=5, padx=20, sticky = "w")  # Без sticky для центрирования фрейма в окне
        label = ttk.Label(frame_four, text='Привлекаемая техника части', font=('Arial', 10))
        label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        # Настраиваем колонки для равномерности и центрирования (без растяжения)
        num_columns = 2  # Или рассчитайте: num_columns = int(len(PARAMS.FIRECAR) ** 0.5) + 1, но 5 — ваш выбор
        col_width = 345 // num_columns  # Примерно равная ширина на колонку (140px каждая)
        for col in range(num_columns):
            frame_four.grid_columnconfigure(col, weight=0,
                                            minsize=col_width)  # Фиксированная ширина, без weight (чтобы не растягивать)
        count_row = 1
        count_col = 0
        for index, option in enumerate(PARAMS.FIRECAR):
            chk = tk.Checkbutton(frame_four, text=option, anchor='center', relief='sunken')
            chk.grid(row=count_row, column=count_col, padx=5, pady=5, sticky='nsew')
            count_col += 1
            if count_col == 2:
                count_col = 0
                count_row += 1

        # ПЯТЫЙ ФРЕЙМ
        # ПРИМЕНЯЛОСЬ НА ПОЖАРЕ
        frame_five = tk.Frame(root_win, borderwidth=2, relief='groove', width=700)
        frame_five.grid(row=3, column=1, pady=5, padx=20)  # Без sticky для центрирования фрейма в окне
        label = ttk.Label(frame_five, text='Оборудование используемое на пожаре', font=('Arial', 10))
        label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)









if __name__ == '__main__':
    print('hello')
    app = СreateInfoWindow()
    app.mainloop()