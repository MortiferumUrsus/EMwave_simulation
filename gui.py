import tkinter as tk
from tkinter import messagebox
from wave_model import EMWave
from simulation import SimulationEngine

class WaveSimulationGUI:
    """
    Класс, отвечающий за графический интерфейс:
    - Позволяет выбрать число волн (1-3).
    - Для каждой волны ввести параметры (амплитуда, ω, k, c и т.д.).
    - Нажать кнопку "Запустить" и увидеть анимацию.
    - Можно нажать "Пауза", "Продолжить" и "Обновить" (перезапуск с новыми параметрами).
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Параметры ЭМ-волн")

        # Поле для выбора количества волн
        self.wave_count_var = tk.IntVar(value=1)
        tk.Label(self.root, text="Количество волн (1-3):").grid(row=0, column=0, sticky="w")
        tk.OptionMenu(self.root, self.wave_count_var, 1, 2, 3, command=self.update_wave_frames).grid(row=0, column=1, sticky="w")

        # Списки для хранения фреймов и полей ввода
        self.wave_frames = []
        self.wave_entries = []
        self.create_wave_frame(1)  # по умолчанию одна волна

        # Поле для ввода скорости анимации
        tk.Label(self.root, text="Скорость анимации:").grid(row=10, column=0, sticky="w")
        self.sim_speed_entry = tk.Entry(self.root)
        self.sim_speed_entry.insert(0, "1.0")
        self.sim_speed_entry.grid(row=10, column=1, sticky="w")

        # Кнопки управления
        self.start_button = tk.Button(self.root, text="Запустить", command=self.start_simulation)
        self.start_button.grid(row=11, column=0, columnspan=2, pady=5)

        self.pause_button = tk.Button(self.root, text="Пауза", command=self.pause_simulation, state=tk.DISABLED)
        self.pause_button.grid(row=12, column=0, columnspan=2, pady=5)

        self.resume_button = tk.Button(self.root, text="Продолжить", command=self.resume_simulation, state=tk.DISABLED)
        self.resume_button.grid(row=13, column=0, columnspan=2, pady=5)

        self.update_button = tk.Button(self.root, text="Обновить", command=self.update_simulation, state=tk.DISABLED)
        self.update_button.grid(row=14, column=0, columnspan=2, pady=5)

        self.simulation_engine = None

    def create_wave_frame(self, wave_number):
        """
        Создаёт фрейм для параметров i-й волны.
        """
        frame = tk.LabelFrame(self.root, text=f"Волна {wave_number}")
        frame.grid(row=wave_number, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        entries = {}
        # Список полей ввода с подписями
        params = [
            ("Амплитуда", "1.0"),
            ("Угловая частота (ω)", "1.0"),
            ("Волновое число (k)", "1.0"),
            ("Направление dx", "1.0"),  # фактически не используем
            ("Направление dy", "0.0"),  # фактически не используем
            ("Направление dz", "0.0"),  # фактически не используем
            ("Скорость c", "1.0")
        ]
        for i, (label_text, default) in enumerate(params):
            tk.Label(frame, text=label_text + ":").grid(row=i, column=0, sticky="w")
            entry = tk.Entry(frame)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky="w")
            entries[label_text] = entry

        self.wave_entries.append(entries)
        self.wave_frames.append(frame)

    def clear_wave_frames(self):
        for frame in self.wave_frames:
            frame.destroy()
        self.wave_frames = []
        self.wave_entries = []

    def update_wave_frames(self, count):
        """
        Удаляем старые фреймы и пересоздаём нужное количество.
        """
        self.clear_wave_frames()
        wave_count = int(count)
        for i in range(wave_count):
            self.create_wave_frame(i+1)

    def start_simulation(self):
        """
        Считываем параметры, создаём объекты EMWave, создаём движок SimulationEngine и запускаем анимацию.
        """
        try:
            wave_list = []
            for entries in self.wave_entries:
                amplitude = float(entries["Амплитуда"].get())
                omega = float(entries["Угловая частота (ω)"].get())
                k = float(entries["Волновое число (k)"].get())
                dx = float(entries["Направление dx"].get())  # не используется
                dy = float(entries["Направление dy"].get())  # не используется
                dz = float(entries["Направление dz"].get())  # не используется
                c_val = float(entries["Скорость c"].get())

                wave_obj = EMWave(amplitude, omega, k, [dx, dy, dz], c_val)
                wave_list.append(wave_obj)

            sim_speed = float(self.sim_speed_entry.get())
            if sim_speed <= 0:
                raise ValueError("Скорость анимации должна быть > 0")

            self.simulation_engine = SimulationEngine(wave_list, sim_speed=sim_speed)
            self.simulation_engine.start()

            self.pause_button.config(state=tk.NORMAL)
            self.update_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Ошибка ввода", str(e))

    def pause_simulation(self):
        if self.simulation_engine is not None:
            self.simulation_engine.pause()
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)

    def resume_simulation(self):
        if self.simulation_engine is not None:
            self.simulation_engine.resume()
            self.resume_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)

    def update_simulation(self):
        """
        Перезапуск анимации с новыми параметрами (при этом ставим текущую на паузу).
        """
        if self.simulation_engine is not None:
            self.pause_simulation()
        self.start_simulation()

    def run(self):
        self.root.mainloop()
