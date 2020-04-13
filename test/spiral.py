import sys
import math

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QGraphicsLineItem
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QPointF, QSizeF, QRectF

class BaseSpiral(QGraphicsItem):

    def __init__(self,
                 color: QColor = Qt.black,
                 thickness: int = 2):

        super().__init__()

        self.color = color
        self.thickness = thickness

        self.height = 800
        self.width = 800

        self.setPos(QPointF(0, 0))

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

        self.setTransFormOriginPoint(QPointF(width / 2, height / 2))

    def paint(self, painter, options, widget=None):
        pass


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
        x = self.width / 2
        y = self.height / 2 - self.radius
        painter.translate(QPointF(self.width / 2, self.height / 2 - self.radius))

        points = []
        rotation, step_rotation = 0, 0.05
        while True:
            r = self.ro * rotation

            x = r * math.cos(rotation)
            y = r * math.sin(rotation)

            if x > self.width / 2 or x < -self.width / 2:
                break
            if y > self.height / 2  or y < -self.height / 2:
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
            points.append(QPointF(x, y))

        painter.drawPolyline(QPolygonF(points))


class MyWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        main_box = QVBoxLayout()
        main_box.addWidget(self.view)
        self.setLayout(main_box)

        self.add_axis()
        self.add_spiral()

    def add_axis(self):
        line_x = QGraphicsLineItem()
        line_x.setLine(-1000, 0, 1000, 0)
        self.scene.addItem(line_x)

        line_y = QGraphicsLineItem()
        line_y.setLine(0, 1000, 0, -1000)
        self.scene.addItem(line_y)

    def add_spiral(self):
        spiral = LogarithmicSpiral(0.215, 10, 5)
        spiral.setPos(QPointF(10, 10))
        self.scene.addItem(spiral)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())

