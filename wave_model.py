import numpy as np

C_LIGHT = 3000000  # Скорость света в вакууме, м/с

class EMWave:
    """
    Класс, описывающий одну электромагнитную волну.
    Параметры, которые вводит пользователь:
      - E0      : амплитуда электрического поля
      - H0      : амплитуда магнитного поля
      - omega   : угловая частота (рад/с)
      - epsilon : относительная электрическая проницаемость среды (ε)
      - mu      : относительная магнитная проницаемость среды (μ)
      - phase   : начальная фаза (рад)

    Автоматически вычисляется:
      - u       : фазовая скорость = c / sqrt(epsilon * mu)
      - k       : волновое число = omega / u
    """
    def __init__(self, E0, H0, omega, epsilon, mu, phase=0.0):
        if E0 < 0:
            raise ValueError("Амплитуда E0 должна быть неотрицательной")
        if H0 < 0:
            raise ValueError("Амплитуда H0 должна быть неотрицательной")
        if omega < 0:
            raise ValueError("Угловая частота ω должна быть неотрицательной")
        if epsilon <= 0:
            raise ValueError("Проницаемость ε должна быть > 0")
        if mu <= 0:
            raise ValueError("Проницаемость μ должна быть > 0")

        self.E0 = E0
        self.H0 = H0
        self.omega = omega
        self.epsilon = epsilon
        self.mu = mu
        self.phase = phase

        # Фазовая скорость
        self.u = C_LIGHT / np.sqrt(self.epsilon * self.mu)
        # Волновое число
        self.k = 0.0
        if self.u != 0:
            self.k = self.omega / self.u
