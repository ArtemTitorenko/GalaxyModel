import math

from abc import ABC, abstractmethod
from graphical_objects import EllipticalObject, EllipticalOrbit
from laws_motions import CircularMotion, EllipticalKeplersMotion
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QPointF


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
        self.law_motion = CircularMotion(self.period,
                                         math.radians(start_rotation))

        self.set_start_rotation()

    def set_start_rotation(self):
        self.motion(0)

    def motion(self, time: float):
        rotation = math.degrees(self.law_motion.rotation(time))
        self.graphical_object.setRotation(rotation)


class KeplersMotionController(MotionController):

    def __init__(self,
                 elliptical_orbit: EllipticalOrbit,
                 period: float,
                 start_rotation: float = 0):

        self.center = elliptical_orbit.center
        self.center_pos = QPointF(self.center.s_major_axis,
                                  self.center.s_minor_axis)

        elliptical_object = elliptical_orbit.elliptical_object
        MotionController.__init__(self, elliptical_object)

        s_major_axis = elliptical_orbit.s_major_axis
        eccentricity = elliptical_orbit.eccentricity
        start_rotation = math.radians(start_rotation)

        self.law_motion = EllipticalKeplersMotion(period,
                                                  s_major_axis,
                                                  eccentricity,
                                                  start_rotation)
        self.set_start_rotation()

    def set_start_rotation(self):
        self.motion(0)

    def motion(self, time: float):
        r = self.law_motion.r(time)
        rotation = self.law_motion.rotation(time)

        x = r * math.cos(rotation)
        y = r * math.sin(rotation)

        pos = self.center_pos + QPointF(x, y)
        self.graphical_object.set_center_pos(pos)

