import math

from abc import ABC, abstractmethod
from graphical_objects import EllipticalObject, EllipticalOrbit
from laws_motions import CircularMotion, EllipticalKeplersMotion
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QPointF


class MotionController(ABC):

    @abstractmethod
    def motion(self, time: float):
        pass

    @abstractmethod
    def set_start_position(self):
        pass

class CircularMotionController(MotionController):

    def __init__(self,
                 graphical_object: QGraphicsItem,
                 period: float,
                 start_rotation: float = 0):

        self.graphical_object = graphical_object
        self.period = period
        self.law_motion = CircularMotion(self.period,
                                         math.radians(start_rotation))

        self.set_start_position()

    def set_start_position(self):
        self.motion(0)

    def motion(self, time: float):
        rotation = math.degrees(self.law_motion.rotation(time))
        self.graphical_object.setRotation(rotation)


class KeplersMotionController(MotionController):

    def __init__(self,
                 orbit: EllipticalOrbit,
                 period: float,
                 start_rotation: float = 0):

        self.center_pos = orbit.center_pos()
        self.graphical_object = orbit.planet

        s_major_axis = orbit.s_major_axis
        eccentricity = orbit.eccentricity
        self.law_motion = EllipticalKeplersMotion(period,
                                                  s_major_axis,
                                                  eccentricity,
                                                  math.radians(start_rotation))
        self.set_start_position()

    def set_start_position(self):
        self.motion(0)

    def motion(self, time: float):
        r = self.law_motion.r(time)
        rotation = self.law_motion.rotation(time)

        x = r * math.cos(rotation)
        y = r * math.sin(rotation)

        pos = self.center_pos + QPointF(x, y)
        self.graphical_object.set_center_pos(pos)

        return r, rotation


