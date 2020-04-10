from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor, QPen

from math import pi, cos, sin, exp, radians, degrees
from .motion_controllers import CircularMotionController

def drange(start, stop, step):
    val = start
    while val < stop:
        yield val
        val += step


class BaseSpiral(QGraphicsRectItem):

    def __init__(self,
                 color: QColor = Qt.black,
                 thickness: int = 2):

        super().__init__()

        self.color = color
        self.thickness = thickness

        self.height = 2000
        self.width = 2000

        self.setRect(0, 0, self.width, self.height)
        self.set_center_pos(QPointF(0, 0))

    def set_center_pos(self, center: QPointF):
        dx = self.width // 2
        dy = self.height // 2

        self.setTransformOriginPoint(QPointF(dx, dy))
        super().setPos(center - QPointF(dx, dy))

    def add_line(self, x0, y0, x1, y1):
        line = QGraphicsLineItem(self)
        line.setPen(QPen(self.color))
        line.setLine(x0, y0, x1, y1)

class ArchimedeanSpiral(BaseSpiral):

    def __init__(self,
                 ro: float,
                 color: QColor = Qt.black,
                 thickness: int = 2):

        super().__init__(color, thickness)

        self.ro = ro
        self.create_spiral()

    def create_spiral(self):
        X0 = self.width // 2
        Y0 = self.height // 2

        prev_x, prev_y = X0, Y0
        for fi in drange(0, 5.5, 0.05):
            r = self.ro * fi

            x = X0 + r * cos(fi)
            y = Y0 - r * sin(fi)

            self.add_line(prev_x, prev_y, x, y)
            prev_x, prev_y = x, y

class LogarithmicSpiral(BaseSpiral):

    def __init__(self,
                 alpha: float,
                 r0: float,
                 spiral_width: int,
                 color: QColor = Qt.black,
                 thickness: int = 2):

        super().__init__(color, thickness)
        self.alpha = alpha
        self.r0 = r0
        self.spiral_width = spiral_width

        self.create_spiral(self.r0, self.alpha, spiral_width // 2)
        self.create_spiral(self.r0, self.alpha, 0)
        self.create_spiral(self.r0, self.alpha, -spiral_width // 2)


    def create_spiral(self, r0, alpha, delta: int = 0):
        X0 = self.width // 2
        Y0 = self.height // 2

        prev_x, prev_y = X0, Y0
        for fi in drange(0, 6.5, 0.05):
            r = r0 * exp(alpha * fi) + delta

            x = X0 + r * cos(fi)
            y = Y0 - r * sin(fi)

            self.add_line(prev_x, prev_y, x, y)
            prev_x, prev_y = x, y

class SystemArchimedeanSpirals(BaseSpiral):

    def __init__(self, parameters: dict, scale: int):
        ro = parameters.get('ro')
        period = parameters.get('period')
        rotation = parameters.get('rotation')

        self.spirals = []
        self.controllers = []

        count_spirals = 2
        rotation_step = 180
        for i in range(count_spirals):
            spiral = ArchimedeanSpiral(ro * scale)
            controller = CircularMotionController(spiral,
                                                  period,
                                                  rotation + rotation_step * i)
            self.spirals.append(spiral)
            self.controllers.append(controller)

    def motion(self, time: float):
        for controller in self.controllers:
            controller.motion(time)

    def restart(self):
        for controller in self.controllers:
            controller.restart()

    def items(self):
        return self.spirals


class SystemLogarithmicSpirals(BaseSpiral):

    def __init__(self, parameters: dict, scale: int):
        alpha = parameters.get('alpha')
        r0 = parameters.get('r0')
        rotation = parameters.get('rotation')
        period = parameters.get('period')
        spiral_width = parameters.get('width')

        self.spirals = []
        self.controllers = []

        count_spirals = 4
        rotation_step = 90
        for i in range(count_spirals):
            spiral = LogarithmicSpiral(alpha, r0 * scale, spiral_width * scale)
            controller = CircularMotionController(spiral,
                                                  period,
                                                  rotation + i * rotation_step)

            self.spirals.append(spiral)
            self.controllers.append(controller)

    def motion(self, time: float):
        for controller in self.controllers:
            controller.motion(time)

    def restart(self):
        for controller in self.controllers:
            controller.restart()

    def items(self):
        return self.spirals
