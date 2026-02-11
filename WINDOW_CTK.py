import customtkinter as ctk
from tkcalendar import DateEntry  # DateEntry из tkcalendar остается, так как CustomTkinter его не имеет
import PARAMS
import disabled_widget
from Address import AutoAdress  # Предполагаю, что это кастомный виджет, адаптируйте если нужно
from TimeEntry import TimeEntry  # Предполагаю, что это кастомный виджет, адаптируйте если нужно


class CreateInfoWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.title('Внесение записи')

        self.basic_frame = ctk.CTkScrollableFrame(self)
        self.basic_frame.pack(fill="both", expand=True)

        frame_one = ctk.CTkFrame(self.basic_frame)
        frame_one.grid(row=0, column=0, sticky='ew')

        label = ctk.CTkLabel(frame_one, text='Дата вызова:')
        label.grid(row=0, column=0, padx=(20, 5), pady=10, sticky='w')
        date_call = DateEntry(frame_one, date_pattern='dd.mm.yyyy', locale='ru_RU')
        date_call.grid(row=0, column=1, padx=(5, 20), pady=10, sticky='w')
        # # Храним виджеты в словарях для удобства доступа
        # self.frames = {}
        # self.widgets = {}

        # Создаем секции
        # self.create_first_frame()
        # self.create_second_frame()
        # self.create_third_frame()


if __name__ == '__main__':
    app = CreateInfoWindow()
    app.mainloop()