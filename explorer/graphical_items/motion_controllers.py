import math
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QPointF

from .laws_motions import CircularMotion, EllipticalKeplersMotion


class MotionController(ABC):

    @abstractmethod
    def motion(self, time: float):
        pass

    @abstractmethod
    def restart(self):
        pass

class CircularMotionController(MotionController):

    def __init__(self,
                 item: QGraphicsItem,
                 period: float,
                 start_rotation: float = 0):

        self.graphical_object = item
        self.period = period
        self.law_motion = CircularMotion(self.period,
                                         math.radians(start_rotation))

        self.restart()

    def restart(self):
        self.motion(0)

    def motion(self, time: float):
        rotation = math.degrees(self.law_motion.rotation(time))
        self.graphical_object.setRotation(rotation)


class KeplersMotionController(MotionController):

    def __init__(self,
                 item: QGraphicsItem,
                 orbit,
                 period: float,
                 start_rotation: float = 0):

        self.center_pos = orbit.local_center_pos()
        self.graphical_object = item

        s_major_axis = orbit.s_major_axis
        eccentricity = orbit.eccentricity
        self.law_motion = EllipticalKeplersMotion(period,
                                                  s_major_axis,
                                                  eccentricity,
                                                  math.radians(start_rotation))
        self.restart()

    def restart(self):
        self.motion(0)

    def motion(self, time: float):
        r = self.sun_distance(time)
        rotation = self.sun_rotation(time)

        x = r * math.cos(rotation)
        y = r * math.sin(rotation)

        pos = self.center_pos + QPointF(x, y)
        self.graphical_object.set_center_pos(pos)

    def sun_distance(self, time: float):
        r = self.law_motion.r(time)
        return r

    def sun_rotation(self, time: float):
        rotation = self.law_motion.rotation(time)
        return rotation

