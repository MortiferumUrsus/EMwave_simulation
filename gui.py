import tkinter as tk
from tkinter import messagebox
from wave_model import EMWave
from simulation import SimulationEngine

class WaveSimulationGUI:
    """
    GUI для ввода параметров волн (до 3).
    Поля:
      - E0
      - H0
      - ω (omega)
      - ε (epsilon)
      - μ (mu)
      - фаза (phase)
    k вычисляется автоматически из omega и u=c/sqrt(ε*μ).
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ЭМ-волна — Параметры")

        # Выбор числа волн
        self.wave_count_var = tk.IntVar(value=1)
        tk.Label(self.root, text="Количество волн (1-3):").grid(row=0, column=0, sticky="w")
        tk.OptionMenu(self.root, self.wave_count_var, 1, 2, 3,
                      command=self.update_wave_frames).grid(row=0, column=1, sticky="w")

        self.wave_frames = []
        self.wave_entries = []
        self.create_wave_frame(1)

        # Скорость анимации
        tk.Label(self.root, text="Скорость анимации:").grid(row=10, column=0, sticky="w")
        self.sim_speed_entry = tk.Entry(self.root)
        self.sim_speed_entry.insert(0, "1.0")  # по умолчанию
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
        Фрейм для одной волны: E0, H0, omega, epsilon, mu, phase
        """
        frame = tk.LabelFrame(self.root, text=f"Волна {wave_number}")
        frame.grid(row=wave_number, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        entries = {}

        params = [
            ("E0", "1.0"),
            ("H0", "1.0"),
            ("ω (omega)", "0.6e7"), 
            ("ε (epsilon)", "1.0"),
            ("μ (mu)", "1.0"),
            ("фаза (phase)", "0.0")
        ]

        for i, (label_text, default) in enumerate(params):
            tk.Label(frame, text=label_text+":").grid(row=i, column=0, sticky="w")
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
        Перестраивает фреймы под нужное число волн.
        """
        self.clear_wave_frames()
        for i in range(int(count)):
            self.create_wave_frame(i+1)

    def start_simulation(self):
        try:
            wave_list = []
            for entries in self.wave_entries:
                E0_val = float(entries["E0"].get())
                H0_val = float(entries["H0"].get())
                omega_val = float(entries["ω (omega)"].get())
                eps_val = float(entries["ε (epsilon)"].get())
                mu_val = float(entries["μ (mu)"].get())
                phase_val = float(entries["фаза (phase)"].get())

                wave_obj = EMWave(E0_val, H0_val, omega_val, eps_val, mu_val, phase_val)
                wave_list.append(wave_obj)

            sim_speed = float(self.sim_speed_entry.get())
            if sim_speed <= 0:
                raise ValueError("Скорость анимации должна быть > 0")

            # Запуск симуляции
            self.simulation_engine = SimulationEngine(wave_list, sim_speed=sim_speed,
                                                      x_min=0.0, x_max=10.0, num_points=300)
            self.simulation_engine.start()

            # Активируем кнопки
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
        if self.simulation_engine is not None:
            self.pause_simulation()
        self.start_simulation()

    def run(self):
        self.root.mainloop()
