import customtkinter as ctk
from tkcalendar import DateEntry  # DateEntry из tkcalendar остается, так как CustomTkinter его не имеет
import PARAMS
import disabled_widget
from Address import AutoAdress  # Предполагаю, что это кастомный виджет, адаптируйте если нужно
from TimeEntry import TimeEntry  # Предполагаю, что это кастомный виджет, адаптируйте если нужно

# Устанавливаем тему CustomTkinter (опционально, можно выбрать 'dark' или 'light')
ctk.set_appearance_mode("light")  # "system", "dark" или "light"
ctk.set_default_color_theme("blue")  # Цветовая тема


class CreateInfoWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Внесение записи')
        self.geometry("1200x800")  # Фиксированный размер, можно адаптировать под экран

        # Создаем скроллируемый фрейм (упрощает код по сравнению с Canvas + Scrollbar)
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True)

        # Храним виджеты в словарях для удобства доступа
        self.frames = {}
        self.widgets = {}

        # Создаем секции
        self.create_first_frame()
        self.create_second_frame()
        self.create_third_frame()

    def create_date_time_frame(self, parent, title, row, column):
        """Вспомогательная функция для создания рамки с датой и временем"""
        frame = ctk.CTkFrame(parent, border_width=2)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

        label = ctk.CTkLabel(frame, text=title, font=("Arial", 10, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=5)

        date_label = ctk.CTkLabel(frame, text="Дата:")
        date_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        date_entry = DateEntry(frame, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        time_label = ctk.CTkLabel(frame, text="Время:")
        time_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        time_entry = TimeEntry(frame, width=13)
        time_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        return frame, date_entry, time_entry

    def create_checkbox_frame(self, parent, title, row, column, command_func):
        """Вспомогательная функция для рамки с чекбоксом"""
        frame = ctk.CTkFrame(parent, border_width=2)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

        label = ctk.CTkLabel(frame, text=title, font=("Arial", 10, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=5)

        checkbox_var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(frame, variable=checkbox_var, text="", command=command_func)
        checkbox.grid(row=1, column=0, columnspan=2)

        return frame, checkbox_var

    def create_first_frame(self):
        """Первый фрейм: Дата вызова, Район, Адрес и т.д."""
        frame_one = ctk.CTkFrame(self.scrollable_frame)
        frame_one.pack(fill="x", padx=20, pady=10)

        # Дата вызова
        date_call_label = ctk.CTkLabel(frame_one, text="Дата вызова:")
        date_call_label.grid(row=0, column=0, padx=(20, 5), pady=10, sticky="w")
        date_call = DateEntry(frame_one, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_call.grid(row=0, column=1, padx=(5, 20), pady=10, sticky="w")
        self.widgets['date_call'] = date_call

        # Район
        rayon_label = ctk.CTkLabel(frame_one, text="Район:")
        rayon_label.grid(row=0, column=2, padx=(20, 5), pady=10, sticky="w")
        combo_rayon = ctk.CTkComboBox(frame_one, values=PARAMS.RAYONS, width=200)
        combo_rayon.grid(row=0, column=3, padx=(5, 20), pady=10, sticky="w")
        combo_rayon.set(PARAMS.RAYONS[0])  # Выбираем первый по умолчанию
        self.widgets['combo_rayon'] = combo_rayon

        # Адрес
        address_label = ctk.CTkLabel(frame_one, text="Адрес:")
        address_label.grid(row=0, column=4, padx=(20, 5), pady=10, sticky="w")
        address = AutoAdress(frame_one, width=400)  # Адаптируйте ширину
        address.grid(row=0, column=5, padx=(20, 5), pady=10, sticky="w")
        self.widgets['address'] = address

        # ФИО Диспетчера
        disp_label = ctk.CTkLabel(frame_one, text="ФИО Диспетчера:")
        disp_label.grid(row=0, column=6, padx=(20, 5), pady=10, sticky="w")
        combo_disp = ctk.CTkComboBox(frame_one, values=PARAMS.DISPATCHER, width=200)
        combo_disp.grid(row=0, column=7, padx=(5, 20), pady=10, sticky="w")
        combo_disp.set(PARAMS.DISPATCHER[0])
        self.widgets['combo_disp'] = combo_disp

        # Номер караула
        caraul_label = ctk.CTkLabel(frame_one, text="Номер караула:")
        caraul_label.grid(row=0, column=8, padx=(20, 5), pady=10, sticky="w")
        combo_caraul = ctk.CTkComboBox(frame_one, values=PARAMS.CARAUL, width=100)
        combo_caraul.grid(row=0, column=9, padx=(5, 20), pady=10, sticky="w")
        combo_caraul.set(PARAMS.CARAUL[0])
        self.widgets['combo_caraul'] = combo_caraul

    def create_second_frame(self):
        """Второй фрейм: Тип вызова, Номер вызова"""
        frame_two = ctk.CTkFrame(self.scrollable_frame)
        frame_two.pack(fill="x", padx=20, pady=10)

        # Тип вызова
        type_call_label = ctk.CTkLabel(frame_two, text="Тип вызова:")
        type_call_label.grid(row=0, column=0, padx=(20, 5), pady=10, sticky="w")
        combo_type_call = ctk.CTkComboBox(frame_two, values=PARAMS.TYPE_CALL, width=200)
        combo_type_call.grid(row=0, column=1, padx=(5, 20), pady=10, sticky="w")
        combo_type_call.set(PARAMS.TYPE_CALL[0])
        self.widgets['combo_type_call'] = combo_type_call

        # Номер вызова
        number_call_label = ctk.CTkLabel(frame_two, text="Номер вызова:")
        number_call_label.grid(row=0, column=2, padx=(20, 5), pady=10, sticky="w")
        combo_number_call = ctk.CTkComboBox(frame_two, values=PARAMS.NUMBER_CALL, width=100)
        combo_number_call.grid(row=0, column=3, padx=(5, 20), pady=10, sticky="w")
        combo_number_call.set(PARAMS.NUMBER_CALL[0])
        self.widgets['combo_number_call'] = combo_number_call

    def create_third_frame(self):
        """Третий фрейм: Показатели оперативного реагирования"""
        frame_three = ctk.CTkFrame(self.scrollable_frame, border_width=2)
        frame_three.pack(fill="x", padx=20, pady=10)

        # Заголовок
        label = ctk.CTkLabel(frame_three, text="Показатели оперативного реагирования", font=("Arial", 10, "bold"))
        label.grid(row=0, column=0, columnspan=7, padx=5, pady=5)

        # Рамки с датой и временем
        self.frames['three_one'], self.widgets['date_msg'], self.widgets['time_msg'] = self.create_date_time_frame(
            frame_three, "Сообщение", 1, 0)
        self.frames['three_two'], self.widgets['date_drive'], self.widgets['time_drive'] = self.create_date_time_frame(
            frame_three, "Выезд", 1, 1)
        self.frames['three_three'], self.widgets['date_loc'], self.widgets['time_loc'] = self.create_date_time_frame(
            frame_three, "Локализация", 2, 0)
        self.frames['three_four'], self.widgets['date_lic'], self.widgets['time_lic'] = self.create_date_time_frame(
            frame_three, "Ликвидация", 2, 1)
        self.frames['three_six'], self.widgets['date_came'], self.widgets['time_came'] = self.create_date_time_frame(
            frame_three, "Прибытие", 1, 4)
        self.frames['three_nine'], self.widgets['date_fire_barrel'], self.widgets[
            'time_fire_barrel'] = self.create_date_time_frame(frame_three, "Подача первого ствола", 1, 6)

        # Специальные рамки
        # Вернули в пути следования (чекбокс)
        self.frames['three_five'], self.checkbox_go_back_value = self.create_checkbox_frame(frame_three,
                                                                                            "Вернули в пути следования",
                                                                                            1, 3,
                                                                                            self.fun_checkbox_go_back)

        # Ликвидация последствий пожара
        fire_frame = ctk.CTkFrame(frame_three, border_width=2)
        fire_frame.grid(row=2, column=3, padx=5, pady=5, columnspan=2, sticky="nsew")
        self.frames['fire_end'], self.widgets['date_fire_end'], self.widgets[
            'time_fire_end'] = self.create_date_time_frame(fire_frame, "Ликвидация последствий пожара", 0, 0)

        # Ликвидация до прибытия (чекбокс)
        self.frames['three_eight'], self.checkbox_before_came_value = self.create_checkbox_frame(frame_three,
                                                                                                 "Ликвидация до прибытия",
                                                                                                 1, 5,
                                                                                                 self.fun_checkbox_before_came)

        # Возвращение в подразделение
        home_frame = ctk.CTkFrame(frame_three, border_width=2)
        home_frame.grid(row=2, column=5, padx=5, pady=5, columnspan=2, sticky="nsew")
        self.frames['go_home'], self.widgets['date_go_home'], self.widgets[
            'time_go_home'] = self.create_date_time_frame(home_frame, "Возвращение в подразделение", 0, 0)

    def fun_checkbox_go_back(self):
        """Обработчик чекбокса 'Вернули в пути следования'"""
        arr_frame_disabled = [self.frames['three_three'], self.frames['three_four'], self.frames['three_six'],
                              self.frames['three_eight'], self.frames['fire_end']]
        if self.checkbox_go_back_value.get():
            disabled_widget.frame_state_set(arr_frame_disabled, 'disabled')
        else:
            disabled_widget.frame_state_set(arr_frame_disabled, 'enabled')

    def fun_checkbox_before_came(self):
        """Обработчик чекбокса 'Ликвидация до прибытия'"""
        arr_frame_disabled = [self.frames['three_three'], self.frames['three_four'], self.frames['three_five'],
                              self.frames['fire_end'], self.frames['three_nine']]
        if self.checkbox_before_came_value.get():
            disabled_widget.frame_state_set(arr_frame_disabled, 'disabled')
        else:
            disabled_widget.frame_state_set(arr_frame_disabled, 'enabled')


if __name__ == '__main__':
    app = CreateInfoWindow()
    app.mainloop()
