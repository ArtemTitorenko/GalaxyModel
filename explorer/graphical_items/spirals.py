import math

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QColor, QPen, QPainter, QPolygonF


class BaseSpiral(QGraphicsItem):

    def __init__(self,
                 color: QColor = Qt.black,
                 thickness: int = 2,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.pen = QPen()
        self.pen.setWidth(thickness)
        self.pen.setColor(color)

        self.height = 800
        self.width = 800

        self.setPos(QPointF(0, 0))
        self._update_origin_point()

    def _update_origin_point(self):
        self.setTransformOriginPoint(QPointF(self.width / 2, self.height / 2))

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def setPos(self, pos: QPointF):
        dx = self.width / 2
        dy = self.height / 2
        super().setPos(pos - QPointF(dx, dy))

    def pos(self):
        dx = self.width / 2
        dy = self.height / 2
        return self.pos() + QPointF(dx, dy)

    def set_size(self, width: int, height: int):
        self.width = width
        self.height = height
        self._update_origin_point()

    def paint(self, painter, options, widget=None):
        painter.setPen(self.pen)


class ArchimedeanSpiral(BaseSpiral):

    def __init__(self,
                 ro: float,
                 radius: float = 0,
                 color: QColor = Qt.black,
                 thickness: int = 2,
                 *args, **kwargs):

        super().__init__(color, thickness, *args, **kwargs)

        self.ro = ro
        self.radius = radius

    def paint(self, painter, options, widget=None):
        super().paint(painter, options, widget)

        x = self.width / 2
        y = self.height / 2 + self.radius
        painter.translate(QPointF(x, y))

        points = []
        rotation, step_rotation = 0, 0.05
        while True:
            r = self.ro * rotation

            x = r * math.cos(rotation)
            y = r * math.sin(rotation)

            if x > self.width / 2 or x < -self.width / 2:
                break
            if y > self.height / 2 or y < -self.height / 2:
                break

            rotation += step_rotation
            points.append(QPointF(x, -y))

        painter.drawPolyline(QPolygonF(points))

class LogarithmicSpiral(BaseSpiral):

    def __init__(self,
                 alpha: float,
                 r0: float,
                 spiral_width: int,
                 color: QColor = Qt.black,
                 thickness: int = 2,
                 *args, **kwargs):

        super().__init__(color, thickness, *args, **kwargs)

        self.alpha = alpha
        self.r0 = r0
        self.spiral_width = spiral_width

    def paint(self, painter, options, widget):
        super().paint(painter, options, widget)

        x, y = self.width / 2, self.height / 2
        painter.translate(QPointF(x, y))

        self._paint_spiral(painter, self.alpha, self.spiral_width / 2)
        self._paint_spiral(painter, self.alpha, 0)
        self._paint_spiral(painter, self.alpha, -self.spiral_width / 2)

    def _paint_spiral(self, painter, alpha: float, delta: int = 0):
        points = []
        rotation, step_rotation = 0, 0.05
        while True:
            r = self.r0 * math.exp(alpha *  rotation) + delta

            x = r * math.cos(rotation)
            y = r * math.sin(rotation)

            if x > self.width / 2 or x < -self.width / 2:
                break
            if y > self.height / 2 or y < -self.height / 2:
                break

            rotation += step_rotation
            points.append(QPointF(x, -y))

        painter.drawPolyline(QPolygonF(points))


class SystemArchimedeanSpirals(BaseSpiral):

    def __init__(self, ro: float, radius: float = 0):

        self.spirals = []

        count_spirals = 2
        self.rotation_step = 180
        colors = [Qt.black, Qt.green]
        for i in range(count_spirals):
            spiral = ArchimedeanSpiral(ro, radius, color=colors[i])
            self.spirals.append(spiral)

    def set_rotation(self, rotation: float):
        # radians
        rotation = -math.degrees(rotation)
        for num, spiral in enumerate(self.spirals):
            spiral.setRotation(num * self.rotation_step + rotation)

    def items(self):
        return self.spirals


class SystemLogarithmicSpirals(BaseSpiral):

    def __init__(self, alpha: float, r0: float, width: float):

        self.spirals = []

        count_spirals = 4
        self.rotation_step = 90
        colors = [Qt.yellow, Qt.black, Qt.red, Qt.blue]
        for i in range(count_spirals):
            spiral = LogarithmicSpiral(alpha, r0, width, color=colors[i])
            self.spirals.append(spiral)

    def set_rotation(self, rotation: float):
        # radians
        rotation = -math.degrees(rotation)
        for num, spiral in enumerate(self.spirals):
            spiral.setRotation(num * self.rotation_step + rotation)

    def items(self):
        return self.spirals

