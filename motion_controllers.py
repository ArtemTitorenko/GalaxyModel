import math

from abc import ABC, abstractmethod
from graphical_objects import EllipticalObject, EllipticalOrbit
from laws_motions import CircularMotion, EllipticalKeplersMotion
from PyQt5.QtWidgets import QGraphicsItem


class MotionController(ABC):

    def __init__(self, graphical_object: QGraphicsItem):
        self.graphical_object = graphical_object

    @abstractmethod
    def motion(self, time: float):
        pass


class CircularMotionController(MotionController):

    def __init__(self,
            graphical_object: QGraphicsItem,
            period: float,
            start_rotation: float = 0):

        MotionController.__init__(self, graphical_object)

        self.period = period
        self.start_rotation = math.radians(start_rotation)
        self.rotational_speed = self.compute_rotational_speed()

        self.law_motion = CircularMotion(self.period, self.start_rotation)

        self.set_start_rotation()

    def compute_rotational_speed(self):
        return 2 * math.pi / self.period

    def set_start_rotation(self):
        self.graphical_object.setRotation(self.start_rotation)
