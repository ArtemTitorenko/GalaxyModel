import math

from abc import ABC, abstractmethod
from functools import lru_cache


class LawMotion(ABC):

    @abstractmethod
    def __init__(self):
        pass

class CircularMotion(LawMotion):

    def __init__(self, period: float, start_rotation: float = 0):
        self.period = period
        self.start_rotation = start_rotation
        self.rotational_speed = 2 * math.pi / period

    def rotation(self, time: float = 0):
        rotation = self.rotational_speed * time + self.start_rotation
        return round(rotation, 5)


class EllipticalKeplersMotion(LawMotion):

    def __init__(self,
            period: float,
            s_major_axis: float,
            eccentricity: float,
            start_rotation: float = 0):

        self.period = period
        self.s_major_axis = s_major_axis
        self.eccentricity = eccentricity
        self.start_rotation = start_rotation

        self.n = self.compute_n()
        self.tau = self.compute_tau()

    def compute_n(self):
        return 2 * math.pi / self.period

    def compute_tau(self):
        f = self.start_rotation
        e = self.eccentricity
        n = self.n

        tmp = math.sqrt( (1 + e) / (1 - e) )
        E = 2 * math.atan( math.tan(f / 2) / tmp)
        M = E - e * math.sin(E)
        tau = - M / n

        return tau

    def mean_anomaly(self, time: float):
        return self.n * (time - self.tau)

    def eccentric_anomaly(self, mean_anomaly: float):
        E = mean_anomaly
        for i in range(10):
            E = mean_anomaly + self.eccentricity * math.sin(E)
        return E

    def true_anomaly(self, eccentric_anomaly: float):
        e = self.eccentricity
        E = eccentric_anomaly
        tmp = math.sqrt( (1 + e) / (1 - e) )

        f = 2 * math.atan(tmp * math.tan(E / 2))
        return f

    def distance(self, time: float = 0):
        M = self.mean_anomaly(time)
        E = self.eccentric_anomaly(M)
        a, e = self.s_major_axis, self.eccentricity

        return a * (1 - e * math.cos(E))

    def rotation(self, time: float = 0):
        M = self.mean_anomaly(time)
        E = self.eccentric_anomaly(M)
        f = round(self.true_anomaly(E), 5)

        return round(f, 5)

    def full_rotation(self, time: float):
        rotation = math.degrees(self.rotation(time))
        if rotation < 0:
            rotation += 360
        rotation = rotation + (time - self.tau) // self.period * 360
        return rotation

