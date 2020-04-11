import sys
import math

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QGraphicsLineItem
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QPointF, QSizeF, QRectF


class Spiral(QGraphicsItem):

    def __init__(self, ro: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ro = ro
        self.width = 500
        self.height = 500

        self.set_center_pos(QPointF(0, 0))

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)

        X0 = self.width // 2
        Y0 = self.height // 2

        points = []
        rotation, step_rotation = 0, 0.01
        while True:
            r = self.ro * rotation
            x = X0 + r * math.cos(rotation)
            y = Y0 - r * math.sin(rotation)

            rotation += step_rotation

            if x > self.width or x < 0:
                break

            if y > self.height or y < 0:
                break

            points.append(QPointF(x, y))

        painter.drawPolyline(QPolygonF(points))
        painter.drawRect(0, 0, self.width, self.height)

    def set_center_pos(self, center: QPointF):
        dx = self.width // 2
        dy = self.height // 2

        self.setTransformOriginPoint(QPointF(dx, dy))
        super().setPos(center - QPointF(dx, dy))

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
        spiral = Spiral(ro=2.48 * 20)
        self.scene.addItem(spiral)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())

