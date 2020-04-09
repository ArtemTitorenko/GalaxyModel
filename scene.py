from PyQt5 import QtWidgets
from PyQt5.QtCore import QPointF


class SceneWithGrid(QtWidgets.QGraphicsScene):

    def __init__(self, *args, **kwargs):
        QtWidgets.QGraphicsScene.__init__(self, *args, **kwargs)
        self.scale = 20
        self.count_marks = 17
        self.center = QPointF(0, 0)

        self.draw()

    def draw(self):
        super().clear()
        self.add_grid()
        self.add_axis()

    def add_grid(self):
        for i in range(1, self.count_marks + 1):
            circle = self._create_cirlce(i * self.scale)
            self.addItem(circle)

    def _create_cirlce(self, radius: float):
        circle = QtWidgets.QGraphicsEllipseItem()
        circle.setRect(0, 0, 2 * radius, 2 * radius)
        circle.setPos(-radius, -radius)

        return circle

    def add_axis(self):
        line_length = self.scale * self.count_marks

        x_min, x_max = -line_length, line_length
        y = self.center.y()
        line_x = QtWidgets.QGraphicsLineItem()
        line_x.setLine(x_min, y, x_max, y)

        y_min, y_max = -line_length, line_length
        x = self.center.x()
        line_y = QtWidgets.QGraphicsLineItem()
        line_y.setLine(x, y_min, x, y_max)

        self.addItem(line_x)
        self.addItem(line_y)

    def set_scale(self, scale: int):
        self.scale = scale
        self.draw()

    def set_center(self, center: QPointF):
        if isinstance(center, QPointF):
            self.center = center
            sefl.draw()

    def clear(self):
        self.draw()
