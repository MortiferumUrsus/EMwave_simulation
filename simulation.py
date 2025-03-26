import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from wave_model import EMWave

class SimulationEngine:
    """
    Класс анимации: для каждой волны рисуется пара линий:
      - E(x) (кривая вдоль оси Y)
      - H(x) (кривая вдоль оси Z)
    Распространение идёт вдоль оси X.
    """
    def __init__(self, wave_list, sim_speed=1.0,
                 x_min=0.0, x_max=10.0, num_points=300):
        self.wave_list = wave_list
        self.sim_speed = sim_speed
        self.x_min = x_min
        self.x_max = x_max
        self.num_points = num_points
        
        # Сетка X
        self.x = np.linspace(self.x_min, self.x_max, self.num_points)
        self.t = 0.0
        
        # Настраиваем 3D-график
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(-2, 2)
        self.ax.set_zlim(-2, 2)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('E')
        self.ax.set_zlabel('H')
        self.ax.set_title("Бегущие ЭМ-волны")

        # Для каждой волны: 2 линии (E и H)
        self.lines_e = []
        self.lines_h = []

        # Цвета, чтобы отличать волны
        color_list = ['red', 'blue', 'green', 'orange', 'magenta', 'cyan']

        for i, _ in enumerate(self.wave_list):
            c_e = color_list[(2*i) % len(color_list)]
            c_h = color_list[(2*i+1) % len(color_list)]
            
            line_e, = self.ax.plot([], [], [], color=c_e, label=f"E_{i+1}")
            line_h, = self.ax.plot([], [], [], color=c_h, label=f"H_{i+1}")
            self.lines_e.append(line_e)
            self.lines_h.append(line_h)

        self.ax.legend()

    def init_func(self):
        """
        Инициализация (для FuncAnimation).
        """
        for le, lh in zip(self.lines_e, self.lines_h):
            le.set_data_3d([], [], [])
            lh.set_data_3d([], [], [])
        return self.lines_e + self.lines_h

    def update(self, frame):
        """
        Вызывается на каждом кадре анимации.
        Для каждой волны вычисляем:
          E(t,x) = E0*cos(ωt - kx + phase)
          H(t,x) = H0*cos(ωt - kx + phase)
        """
        self.t += 0.001 * self.sim_speed  # Шаг времени

        for i, wave in enumerate(self.wave_list):
            phase_arg = wave.omega * self.t - wave.k * self.x + wave.phase
            E_vals = wave.E0 * np.cos(phase_arg)
            H_vals = wave.H0 * np.cos(phase_arg)

            # E вдоль оси Y, H вдоль оси Z
            self.lines_e[i].set_data_3d(self.x, E_vals, np.zeros_like(self.x))
            self.lines_h[i].set_data_3d(self.x, np.zeros_like(self.x), H_vals)

        return self.lines_e + self.lines_h

    def start(self):
        """
        Запуск анимации.
        """
        self.anim = FuncAnimation(self.fig, self.update,
                                  init_func=self.init_func,
                                  frames=200, interval=50, blit=True)
        plt.show()

    def pause(self):
        """
        Пауза анимации.
        """
        if self.anim and self.anim.event_source:
            self.anim.event_source.stop()

    def resume(self):
        """
        Возобновление анимации.
        """
        if self.anim and self.anim.event_source:
            self.anim.event_source.start()
