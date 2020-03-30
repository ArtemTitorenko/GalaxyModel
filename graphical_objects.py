from PyQt5.QtWidgets import QGraphicsEllipseItem
import math

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

    def set_center_pos(self, center: QPointF):
        dx, dy = self.s_major_axis, self.s_minor_axis

        QGraphicsEllipseItem.setPos(self, center - QPointF(dx, dy))

    def center_pos(self):
        pos = self.pos()
        dx, dy = self.s_major_axis, self.s_minor_axis

        return pos + QPointF(dx, dy)

class EllipticalOrbit(EllipticalObject):

    def __init__(self,
            center: EllipticalObject,
            eccentricity: float,
            s_major_axis: float):

        EllipticalObject.__init__(self, eccentricity, s_major_axis)

        self.center = center
        self.linear_eccentricity = self.compute_linear_eccentricity()

        self.init_pos()

    def compute_linear_eccentricity(self):
        a, b = self.s_major_axis, self.s_minor_axis
        return math.sqrt(math.pow(a, 2) - math.pow(b, 2))

    def init_pos(self):
        dx, dy = self.linear_eccentricity, 0
        center_pos = self.center.center_pos()

        self.set_center_pos(center_pos - QPointF(dx, dy))

