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

        self.setTransformOriginPoint(self.s_major_axis, self.s_minor_axis)

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
            center: EllipticalObject,
            elliptical_object: EllipticalObject,
            eccentricity: float,
            s_major_axis: float):

        EllipticalObject.__init__(self, eccentricity, s_major_axis)

        self.center = center
        self.elliptical_object = elliptical_object
        self.linear_eccentricity = self.compute_linear_eccentricity()

        self.config_parent_items()
        self.init_pos()
        self.init_line_apsid()

    def config_parent_items(self):
        self.setParentItem(self.center)
        self.elliptical_object.setParentItem(self.center)

    def compute_linear_eccentricity(self):
        a, b = self.s_major_axis, self.s_minor_axis
        return a * self.eccentricity

    def init_pos(self):
        dx = self.center.s_major_axis - self.linear_eccentricity
        dy = self.center.s_minor_axis
        self.set_center_pos(QPointF(dx, dy))

    def init_line_apsid(self):
        line = QGraphicsLineItem()
        line.setParentItem(self)
        line.setLine(0, self.s_minor_axis,
                     2 * self.s_major_axis, self.s_minor_axis)

