import math
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem

from PyQt5.QtCore import QPointF, Qt, QRectF
from PyQt5.QtGui import QBrush, QPen, QColor


class EllipticalObject(QGraphicsEllipseItem):

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


class EllipticalOrbit(EllipticalObject):

    def __init__(self,
            eccentricity: float,
            s_major_axis: float):

        EllipticalObject.__init__(self, eccentricity, s_major_axis)

        center_size = 0.1 * s_major_axis
        planet_size = 0.05 * s_major_axis
        circle_eccentricity = 0

        self.center = EllipticalObject(circle_eccentricity, center_size, parent=self)
        self.planet = EllipticalObject(circle_eccentricity, planet_size, parent=self)

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

