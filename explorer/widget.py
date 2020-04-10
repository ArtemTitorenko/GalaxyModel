from PyQt5 import QtWidgets
from PyQt5.QtCore import QBasicTimer, QPointF, pyqtSlot

from .graphical_objects.orbit import EllipticalOrbit
from .scene import SceneWithGrid
from .graphical_objects.spirals import SystemArchimedeanSpirals
from .graphical_objects.spirals import SystemLogarithmicSpirals


class ExplorerWidget(QtWidgets.QWidget):

    def __init__(self, parameters: dict, scale: int, parent=None):
        super().__init__(parent=parent)

        self.parameters = parameters
        self.scale = scale

        fps = 60
        # msec at sec
        msec = 1000
        self.timer = QBasicTimer()
        self.timer.start(msec // fps, self)

        self.RUN = False

        self.time = 0
        self.time_interval = 0.5

        self.scene = SceneWithGrid()
        self.scene.set_scale(scale)

        self.view = QtWidgets.QGraphicsView(self.scene)

        self.init_ui()
        self.update_graphical_objects()

    def init_ui(self):
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.view)

        self.setLayout(vbox)

    @pyqtSlot()
    def restart(self):
        self.time = 0
        self.RUN = False

        self.orbit.restart()
        self.arch_spirals.restart()
        self.log_spirals.restart()

    def update_graphical_objects(self):
        self.add_orbit()
        self.add_log_spirals()
        self.add_arch_spirals()

    @pyqtSlot(dict)
    def update_parameters(self, new_parameters: dict):
        if new_parameters != {}:
            self._update_parameters(new_parameters)
            self.scene.clear()
            self.update_graphical_objects()
            self.restart()

    def _update_parameters(self, new_parameters):
        for group, parameters in new_parameters.items():
            for name, value in parameters.items():
                self.parameters[group][name] = value

    def timerEvent(self, event):
        self.run()

    def run(self):
        if self.RUN:
            self.orbit.motion(self.time)
            self.arch_spirals.motion(self.time)
            self.log_spirals.motion(self.time)

            self.time += self.time_interval

    def add_orbit(self):
        orbit_parameters = self.parameters['orbit']
        self.orbit = EllipticalOrbit(orbit_parameters, self.scale)
        self.scene.addItem(self.orbit.item)

    def add_log_spirals(self):
        self.log_spirals = SystemLogarithmicSpirals(self.parameters['log_spirals'], self.scale)
        for spiral in self.log_spirals.items():
            self.scene.addItem(spiral)

    def add_arch_spirals(self):
        self.arch_spirals = SystemArchimedeanSpirals(self.parameters['arch_spirals'], self.scale)
        for spiral in self.arch_spirals.items():
            self.scene.addItem(spiral)

    @pyqtSlot()
    def start(self):
        self.RUN = True

    @pyqtSlot()
    def stop(self):
        self.RUN = False

