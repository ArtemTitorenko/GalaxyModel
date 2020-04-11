from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QColor, QPen, QPainter, QPolygonF

from math import pi, cos, sin, exp, radians, degrees
from .motion_controllers import CircularMotionController


class BaseSpiral(QGraphicsItem):

    def __init__(self,
                 color: QColor = Qt.black,
                 thickness: int = 2):

        super().__init__()

        self.color = color
        self.thickness = thickness

        self.height = 800
        self.width = 800

        self.set_center_pos(QPointF(0, 0))

    def set_center_pos(self, center: QPointF):
        dx = self.width / 2
        dy = self.height / 2

        self.setTransformOriginPoint(QPointF(dx, dy))
        super().setPos(center - QPointF(dx, dy))

    def set_size(self, width: int, height: int):
        self.width = width
        self.height = height

    def paint(self, painter, options, widget=None):
        pass

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)


class ArchimedeanSpiral(BaseSpiral):

    def __init__(self,
                 ro: float,
                 radius: float = 0,
                 color: QColor = Qt.black,
                 thickness: int = 2):

        super().__init__(color, thickness)

        self.ro = ro
        self.radius = radius

    def paint(self, painter, options, widget=None):
        points = []

        X0, Y0 = self.width / 2, self.height / 2 - self.radius
        rotation, step_rotation = 0, 0.05
        while True:
            r = self.ro * rotation

            x = X0 + r * cos(rotation)
            y = Y0 + r * sin(rotation)

            if x > self.width or x < 0:
                break
            if y > self.height or y < 0:
                break

            rotation += step_rotation
            points.append(QPointF(x, y))

        painter.drawPolyline(QPolygonF(points))

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

    def paint(self, painter, options, widget):
        self._paint_spiral(painter, self.alpha, self.spiral_width / 2)
        self._paint_spiral(painter, self.alpha, 0)
        self._paint_spiral(painter, self.alpha, -self.spiral_width / 2)

    def _paint_spiral(self, painter, alpha: float, delta: int = 0):
        points = []

        X0, Y0 = self.width / 2, self.height / 2
        rotation, step_rotation = 0, 0.05
        while True:
            r = self.r0 * exp(alpha *  rotation) + delta

            x = X0 + r * cos(rotation)
            y = Y0 + r * sin(rotation)

            if x > self.width or x < 0:
                break
            if y > self.height or y < 0:
                break

            rotation += step_rotation
            points.append(QPointF(x, y))

        painter.drawPolyline(QPolygonF(points))


class SystemArchimedeanSpirals(BaseSpiral):

    def __init__(self, parameters: dict, scale: int, radius: float = 0):
        ro = parameters.get('ro')
        period = parameters.get('period')
        rotation = parameters.get('rotation')

        self.spirals = []
        self.controllers = []

        count_spirals = 2
        rotation_step = 180
        for i in range(count_spirals):
            spiral = ArchimedeanSpiral(ro * scale, radius)
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
