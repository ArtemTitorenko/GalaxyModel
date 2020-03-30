from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene
from PyQt5.QtWidgets import QGridLayout, QGraphicsEllipseItem, QApplication
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtCore import QPointF
from graphical_objects import EllipticalObject, EllipticalOrbit

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.layout = QGridLayout()
        self.layout.addWidget(self.view, 0, 0)
        self.view.setScene(self.scene)
        self.setLayout(self.layout)

        point = QPointF(0, 0)
        self.line = QGraphicsLineItem()
        self.line.setLine(0, -50, 0, 50)
        self.scene.addItem(self.line)

        self.center = EllipticalObject(0, 10)
        self.center.set_center_pos(point)
        self.scene.addItem(self.center)

        self.ellipse = EllipticalOrbit(self.center, 0.6, 200)
        self.scene.addItem(self.ellipse)

        self.update()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

