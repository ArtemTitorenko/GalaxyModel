import math
import sys

from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem

from PyQt5.QtCore import QPointF, Qt, QRectF
from PyQt5.QtGui import QBrush, QPen, QColor

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
        self.setPos(QPointF(0, 0))

    def boundingRect(self):
        return QRectF(0, 0, 2 * self.s_major_axis, 2 * self.s_minor_axis)

    def setPos(self, pos: QPointF):
        dx = self.s_major_axis + self.linear_eccentricity
        dy = self.s_minor_axis
        super().setPos(pos - QPointF(dx, dy))

    def pos(self):
        dx = self.linear_eccentricity + self.s_major_axis
        dy = self.s_minor_axis
        return super().pos() + QPointF(dx, dy)

    def paint(self, painter, options, widget=None):
        pass


class EllipticalOrbitItem(EllipticalItem):

    def __init__(self,
                 eccentricity: float,
                 s_major_axis: float,
                 *args, **kwargs):

        super().__init__(eccentricity,
                         s_major_axis,
                         *args, **kwargs)

        self.rotation = 0
        self.distance = 0

        origin_pos = QPointF(self.s_major_axis + self.linear_eccentricity,
                             self.s_minor_axis)
        self.setTransformOriginPoint(origin_pos)

        radius_sun = 10
        self.sun = SunItem(radius_sun, parent=self)
        self._radius_center_mass = 15

    def paint(self, painter, options, widget=None):
        x, y = self.s_major_axis, self.s_minor_axis
        painter.translate(QPointF(x, y))

        # orbit
        center_point = QPointF(0, 0)
        painter.drawEllipse(center_point,
                            self.s_major_axis,
                            self.s_minor_axis)

        # line apside
        p1 = QPointF(-self.s_major_axis, 0)
        p2 = QPointF(self.s_major_axis, 0)
        painter.drawLine(p1, p2)

        # center_mass
        color_center_mass = Qt.black
        painter.setBrush(color_center_mass)
        pos_center_mass = QPointF(self.linear_eccentricity, 0)
        painter.drawEllipse(pos_center_mass,
                            self._radius_center_mass,
                            self._radius_center_mass)

    def set_rotation(self, rotation: float):
        # degrees
        self.rotation = -math.degrees(rotation)
        self.setRotation(self.rotation)

    def set_distance(self, distance: float):
        pass

    def radius_center(self):
        return self._radius_center_mass


class SunItem(EllipticalItem):

    def __init__(self, radius: float, *args, **kwargs):
        super().__init__(0, radius, *args, **kwargs)

        self.rotation = 0
        self.distance = 0

        self.setPos(QPointF(0, 0))

    def paint(self, painter, options, widget=None):
        x, y = self.s_major_axis, self.s_minor_axis
        painter.translate(QPointF(x, y))

        color_sun = Qt.red
        painter.setBrush(QBrush(color_sun))
        painter.drawEllipse(QPointF(0, 0), self.s_major_axis, self.s_minor_axis)

    def setPos(self, pos: QPointF):
        orbit = self.parentItem()
        dx = orbit.s_major_axis + orbit.linear_eccentricity
        dy = orbit.s_minor_axis

        super().setPos(QPointF(dx, dy) + pos)

    def set_rotation(self, rotation: float):
        self.rotation = -rotation

    def set_distance(self, distance: float):
        self.distance = distance

        x = distance * math.cos(self.rotation)
        y = distance * math.sin(self.rotation)

        self.setPos(QPointF(x, y))

