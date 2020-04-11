import sys
import math

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, QPointF, QRectF, QPoint

from .motion_controllers import CircularMotionController
from .motion_controllers import KeplersMotionController


def semi_minor_axis(eccentricity, s_major_axis):
    return s_major_axis * math.sqrt(1 - eccentricity ** 2)

def linear_eccentricity(eccentricity, s_major_axis):
    return eccentricity * s_major_axis

class EllipticalItem(QGraphicsItem):

    def __init__(self,
                 eccentricity: float,
                 s_major_axis: float,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.eccentricity = eccentricity
        self.s_major_axis = s_major_axis
        self.s_minor_axis = semi_minor_axis(eccentricity, s_major_axis)
        self.linear_eccentricity = linear_eccentricity(eccentricity,
                                                       s_major_axis)
        self.set_center_pos(QPointF(0, 0))

    def boundingRect(self):
        return QRectF(0, 0, 2 * self.s_major_axis, 2 * self.s_minor_axis)

    def set_center_pos(self, pos: QPointF):
        dx = self.s_major_axis + self.linear_eccentricity
        dy = self.s_minor_axis
        self.setPos(pos - QPointF(dx, dy))

    def center_pos(self) -> QPointF:
        dx = self.s_major_axis + self.linear_eccentricity
        dy = self.s_minor_axis
        left_corner = self.pos()
        return left_corner + QPointF(dx, dy)

    def local_center_pos(self) -> QPointF:
        return QPointF(self.s_major_axis, self.s_minor_axis)


class EllipticalOrbitItem(EllipticalItem):

    def __init__(self,
                 eccentricity: float,
                 s_major_axis: float,
                 *args, **kwargs):

        super().__init__(eccentricity,
                         s_major_axis,
                         *args, **kwargs)

        self._radius_center = 15
        origin_point = QPointF(self.s_major_axis + self.linear_eccentricity,
                               self.s_minor_axis)

        self.setTransformOriginPoint(origin_point)

    def paint(self, painter, options, widget=None):
        # orbit
        geom_center = QPoint(self.s_major_axis, self.s_minor_axis)
        painter.drawEllipse(geom_center, self.s_major_axis, self.s_minor_axis)

        # line apside
        p1 = QPointF(0, self.s_minor_axis)
        p2 = QPointF(2 * self.s_major_axis, self.s_minor_axis)
        painter.drawLine(p1, p2)

        # center
        color_center = Qt.black
        painter.setBrush(color_center)
        center_pos = QPoint(self.s_major_axis + self.linear_eccentricity,
                            self.s_minor_axis)
        painter.drawEllipse(center_pos, self._radius_center, self._radius_center)

    def radius_center(self):
        return self._radius_center

    def local_center_pos(self):
        return QPointF(self.s_major_axis + self.linear_eccentricity,
                       self.s_minor_axis)


class SunItem(EllipticalItem):

    def __init__(self, radius: float, *args, **kwargs):
        super().__init__(0, radius, *args, **kwargs)

    def paint(self, painter, options, widget=None):
        geom_center = QPoint(self.s_major_axis, self.s_minor_axis)
        color_sun = Qt.red
        painter.setBrush(QBrush(color_sun))
        painter.drawEllipse(geom_center, self.s_major_axis, self.s_minor_axis)


class Orbit:

    def __init__(self, parameters: dict, scale: int):
        eccentricity = parameters.get('eccentricity')
        s_major_axis = parameters.get('s_major_axis')
        period_sun = parameters.get('sun_period')
        period_orbit = parameters.get('orbit_period')
        rotation_sun = parameters.get('sun_rotation')
        rotation_orbit = parameters.get('orbit_rotation')

        self.orbit_item = EllipticalOrbitItem(eccentricity,
                                              s_major_axis * scale)
        radius_sun = 15
        self.sun = SunItem(radius_sun, parent=self.orbit_item)

        orbit_contoller = CircularMotionController(self.orbit_item,
                                                   period_orbit,
                                                   rotation_orbit)
        sun_controller = KeplersMotionController(self.sun,
                                                 self.orbit_item,
                                                 period_sun,
                                                 rotation_sun)
        self.controllers = [orbit_contoller, sun_controller]

    def item(self):
        return self.orbit_item

    def motion(self, time: float):
        for controller in self.controllers:
            controller.motion(time)

    def restart(self):
        for controller in self.controllers:
            controller.restart()

    def sun_distance(self):
        sun = 1
        return self.controllers[sun].sun_distance()

    def sun_rotation(self):
        sun = 1
        return self.controllers[sun].sun_rotation()

