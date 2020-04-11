import math
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem

from PyQt5.QtCore import QPointF, Qt, QRectF
from PyQt5.QtGui import QBrush, QPen, QColor

from .motion_controllers import KeplersMotionController
from .motion_controllers import CircularMotionController


class EllipticalItem(QGraphicsEllipseItem):

    def __init__(self,
            eccentricity: float,
            s_major_axis: float,
            parent=None):

        QGraphicsEllipseItem.__init__(self, parent=parent)
        self.eccentricity = eccentricity
        self.s_major_axis = s_major_axis
        self.s_minor_axis = self.compute_minor_axis() // 2

        self.init_rect()

    def compute_minor_axis(self):
        major_axis = 2 * self.s_major_axis
        return major_axis * math.sqrt(1 - math.pow(self.eccentricity, 2))

    def init_rect(self):
        major_axis = 2 * self.s_major_axis
        minor_axis = 2 * self.s_minor_axis

        rect = QRectF(0, 0, major_axis, minor_axis)
        QGraphicsEllipseItem.setRect(self, rect)

    def center_pos(self):
        left_corner = QGraphicsEllipseItem.pos(self)
        dx, dy = self.s_major_axis, self.s_minor_axis
        return left_corner + QPointF(dx, dy)

    def set_center_pos(self, center_pos: QPointF):
        dx, dy = self.s_major_axis, self.s_minor_axis
        QGraphicsEllipseItem.setPos(self, center_pos - QPointF(dx, dy))


class EllipticalOrbitItem(EllipticalItem):

    def __init__(self,
            eccentricity: float,
            s_major_axis: float):

        EllipticalItem.__init__(self, eccentricity, s_major_axis)

        center_size = s_major_axis // 20
        sun_size = s_major_axis // 20

        circle_eccentricity = 0

        self.center = EllipticalItem(circle_eccentricity, center_size, parent=self)
        self.center.setBrush(QBrush(Qt.black))
        self.sun = EllipticalItem(circle_eccentricity, sun_size, parent=self)
        self.sun.setBrush(QBrush(Qt.red))

        self.linear_eccentricity = self.compute_linear_eccentricity()

        self.init_positions()
        self.init_line_apsid()

    def compute_linear_eccentricity(self):
        a, b = self.s_major_axis, self.s_minor_axis
        return a * self.eccentricity

    def init_positions(self):
        dx = self.s_major_axis + self.linear_eccentricity
        dy = self.s_minor_axis

        self.center.set_center_pos(QPointF(dx, dy))
        self.setTransformOriginPoint(QPointF(dx, dy))

    def set_center_pos(self, position: QPointF):
        dx = self.s_major_axis + self.linear_eccentricity
        dy = self.s_minor_axis
        QGraphicsEllipseItem.setPos(self, position - QPointF(dx, dy))

    def center_pos(self):
        return self.center.center_pos()

    def init_line_apsid(self):
        line = QGraphicsLineItem()
        line.setParentItem(self)
        line.setLine(0, self.s_minor_axis,
                     2 * self.s_major_axis, self.s_minor_axis)


class EllipticalOrbit:

    def __init__(self,
                 parameters: dict,
                 scale: int):

        eccentricity = parameters.get('eccentricity')
        s_major_axis = parameters.get('s_major_axis')
        sun_period = parameters.get('sun_period')
        orbit_period = parameters.get('orbit_period')
        sun_rotation = parameters.get('sun_rotation')
        orbit_rotation = parameters.get('orbit_rotation')

        self.item = EllipticalOrbitItem(eccentricity, s_major_axis * scale)

        self.contoller = CircularMotionController(self.item,
                                                  orbit_period,
                                                  orbit_rotation)

        self.sun_controller = KeplersMotionController(self.item,
                                                      sun_period,
                                                      sun_rotation)
        self.item.set_center_pos(QPointF(0, 0))

    def restart(self):
        self.contoller.restart()
        self.sun_controller.restart()

    def motion(self, time: float):
        self.contoller.motion(time)
        self.sun_controller.motion(time)

    def sun_distance(self, time: float):
        return self.sun_controller.sun_distance(time)

    def sun_rotation(self, time: float):
        return self.sun_controller.sun_rotation(time)

