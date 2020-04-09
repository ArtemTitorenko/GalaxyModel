from random import randint

from PyQt5 import QtWidgets
from PyQt5.QtCore import QBasicTimer, QPointF, pyqtSlot

from graphical_objects import EllipticalOrbit
from motion_controllers import CircularMotionController
from motion_controllers import KeplersMotionController
from scene import SceneWithGrid


class Explorer(QtWidgets.QWidget):

    def __init__(self, parameters: dict, scale: int, parent=None):
        super().__init__(parent=parent)

        self.parameters = parameters
        self.motion_controllers = {}
        self.intersection_controllers = {}
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

        for controller in self.motion_controllers.values():
            controller.set_start_position()

    def update_graphical_objects(self):
        self.add_orbit()
        #self.add_log_spirals()
        #self.add_arch_spirals()

        self.add_controller_orbit()
        #self.add_controller_log_spirals()
        #self.add_controller_arch_spiral()

    @pyqtSlot(dict)
    def update_parameters(self, new_parameters: dict):
        if new_parameters != {}:
            self._update_parameters(new_parameters)
            self.scene.clear()
            self.update_graphical_objects()
            self.restart()

    def _update_parameters(self, new_parameters):
        for name, value in new_parameters.items():
            self.parameters[name] = value

    def timerEvent(self, event):
        self.run()

    def run(self):
        if self.RUN:
            for controller in self.motion_controllers.values():
                controller.motion(self.time)
            self.time += self.time_interval

    def add_orbit(self):
        eccentricity = self.parameters.get('eccentricity', 0.36)
        s_major_axis = self.parameters.get('s_major_axis', 8.44) * self.scale
        self.orbit = EllipticalOrbit(eccentricity, s_major_axis)

        self.orbit.set_center_pos(QPointF(0, 0))
        self.scene.addItem(self.orbit)

    def add_controller_orbit(self):
        orbital_period = self.parameters.get('orbital_period', 222)
        orbital_rotation = self.parameters.get('orbital_rotation', 13)
        orbital_controller = CircularMotionController(self.orbit,
                                                      orbital_period,
                                                      orbital_rotation)

        sun_period = self.parameters.get('sun_period', 250)
        sun_rotation = self.parameters.get('sun_rotation', 90)
        sun_controller = KeplersMotionController(self.orbit,
                                                 sun_period,
                                                 sun_rotation)

        self.motion_controllers['sun_controller'] = sun_controller
        self.motion_controllers['orbital_controller'] = orbital_controller

    @pyqtSlot()
    def start(self):
        self.RUN = True

    @pyqtSlot()
    def stop(self):
        self.RUN = False

