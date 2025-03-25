import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from wave_model import EMWave

class SimulationEngine:
    """
    Класс, отвечающий за анимацию электромагнитных волн.
    
    Идея визуализации:
    - Распространение вдоль оси X 
    - Е колеблется вдоль оси Y 
    - M колеблется вдоль оси Z 
    - Для каждой волны создаём две линии:
        красную (E) и синюю (H).
    - Если несколько волн, отображаем их отдельно (каждая волна = 2 линии).
    
    Аргументы конструктора:
    - wave_list: список объектов EMWave.
    - sim_speed: коэффициент, влияющий на скорость анимации (больше = быстрее).
    - x_min, x_max: границы по оси X, внутри которых рисуем.
    - num_points: число точек вдоль оси X.
    """
    def __init__(self, wave_list, sim_speed=1.0, x_min=0.0, x_max=10.0, num_points=200):
        self.wave_list = wave_list
        self.sim_speed = sim_speed
        self.x_min = x_min
        self.x_max = x_max
        self.num_points = num_points
        
        # Сетка вдоль оси X
        self.x = np.linspace(self.x_min, self.x_max, self.num_points)
        self.t = 0.0  # начальное время
        
        # Создаём 3D-график
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(-2, 2)  # границы по оси Y (E)
        self.ax.set_zlim(-2, 2)  # границы по оси Z (H)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('E (ось Y)')
        self.ax.set_zlabel('H (ось Z)')
        self.ax.set_title("Анимация ЭМ-волн")

        # Для каждой волны делаем 2 линии: E и H
        self.lines_e = []
        self.lines_h = []
        for i, wave in enumerate(self.wave_list):
            # Красная линия для электрического поля i-й волны
            line_e, = self.ax.plot([], [], [], color='red', label=f'E {i+1}')
            # Синяя линия для магнитного поля i-й волны
            line_h, = self.ax.plot([], [], [], color='blue', label=f'H {i+1}')
            self.lines_e.append(line_e)
            self.lines_h.append(line_h)

        # Чтобы легенда не дублировалась, показываем её только один раз
        self.ax.legend(loc='upper right')

    def init_func(self):
        """
        Инициализация анимации.
        Сбрасываем все линии в пустое состояние.
        """
        for line_e in self.lines_e:
            line_e.set_data_3d([], [], [])
        for line_h in self.lines_h:
            line_h.set_data_3d([], [], [])
        return self.lines_e + self.lines_h

    def update(self):
        """
        Вызывается для каждого кадра анимации.
        Увеличиваем время, пересчитываем E и H для каждой волны, перерисовываем линии.
        """
        self.t += 0.05 * self.sim_speed

        # Для каждой волны рассчитываем её собственные E(x,t) и H(x,t)
        # и устанавливаем их в соответствующие линии.
        for i, wave in enumerate(self.wave_list):
            # Фаза φ = ωt - kx
            phase = wave.omega * self.t - wave.k * self.x

            # E = A cos(φ), колебания вдоль Y
            e_val = wave.amplitude * np.cos(phase)

            # H = (A/c) cos(φ), колебания вдоль Z
            h_val = (wave.amplitude / wave.c) * np.cos(phase)

            # Линию для E ставим на (x, e_val, z=0)
            self.lines_e[i].set_data_3d(self.x, e_val, np.zeros_like(self.x))

            # Линию для H ставим на (x, y=0, h_val)
            self.lines_h[i].set_data_3d(self.x, np.zeros_like(self.x), h_val)

        # Возвращаем список всех линий, чтобы FuncAnimation их обновил
        return self.lines_e + self.lines_h

    def start(self):
        """
        Запускает анимацию.
        """
        self.anim = FuncAnimation(self.fig,
                                  self.update,
                                  init_func=self.init_func,
                                  frames=200,
                                  interval=50,
                                  blit=True)
        plt.show()

    def pause(self):
        """
        Ставит анимацию на паузу.
        """
        if self.anim and self.anim.event_source:
            self.anim.event_source.stop()

    def resume(self):
        """
        Возобновляет анимацию после паузы.
        """
        if self.anim and self.anim.event_source:
            self.anim.event_source.start()
