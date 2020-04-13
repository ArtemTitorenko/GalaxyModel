import math
from collections import defaultdict
from array import array

from PyQt5 import QtWidgets
from PyQt5.QtCore import QBasicTimer, QPointF, pyqtSlot
from PyQt5.QtGui import QPainter

from .graphical_items.orbit import EllipticalOrbitItem
from .laws_motions import EllipticalKeplersMotion
from .laws_motions import CircularMotion

from .scene import SceneWithGrid

from .graphical_items.spirals import SystemArchimedeanSpirals
from .graphical_items.spirals import SystemLogarithmicSpirals
from .graphical_items.spirals import ArchimedeanSpiral


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
        self.view.setRenderHint(QPainter.Antialiasing)

        self.init_ui()
        self.config_items()

        self.restart()

    def init_ui(self):
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.view)
        self.setLayout(vbox)

    def config_items(self):
        self._config_orbit()
        self._config_arch_spirals()
        self._config_log_spirals()

    def _config_orbit(self):
        eccentricity = self.parameters['orbit']['eccentricity']
        s_major_axis = self.parameters['orbit']['s_major_axis']
        self.orbit = EllipticalOrbitItem(eccentricity,
                                         s_major_axis * self.scale)

        sun_period = self.parameters['orbit']['sun_period']
        sun_rotation = math.radians(self.parameters['orbit']['sun_rotation'])
        self.sun_contoller = EllipticalKeplersMotion(sun_period,
                                                     s_major_axis,
                                                     eccentricity,
                                                     sun_rotation)

        orbit_period = self.parameters['orbit']['orbit_period']
        orbit_rotation = math.radians(self.parameters['orbit']['orbit_rotation'])
        self.orbit_controller = CircularMotion(orbit_period, orbit_rotation)

        self.scene.addItem(self.orbit)

    def _config_arch_spirals(self):
        ro = self.parameters['arch_spirals']['ro']
        radius_center = self.orbit.radius_center()
        self.arch_spirals = SystemArchimedeanSpirals(ro * self.scale,
                                                     radius_center)

        period = self.parameters['arch_spirals']['period']
        rotation = math.radians(self.parameters['arch_spirals']['rotation'])
        self.arch_spirals_controller = CircularMotion(period, rotation)

        for spiral in self.arch_spirals.items():
            self.scene.addItem(spiral)

    def _config_log_spirals(self):
        alpha = self.parameters['log_spirals']['alpha']
        r0 = self.parameters['log_spirals']['r0'] * self.scale
        width = self.parameters['log_spirals']['width'] * self.scale
        self.log_spirals = SystemLogarithmicSpirals(alpha, r0, width)

        period = self.parameters['log_spirals']['period']
        rotation = math.radians(self.parameters['log_spirals']['rotation'])
        self.log_spirals_controller = CircularMotion(period, rotation)

        for spiral in self.log_spirals.items():
            self.scene.addItem(spiral)

    @pyqtSlot()
    def restart(self):
        self.time = 0
        self.RUN = False

        self._orbit_motion()
        self._arch_spirals_motion()
        self._log_spirals_motion()

    def timerEvent(self, event):
        self.run()

    def run(self):
        if self.RUN:
            self._orbit_motion()
            self._arch_spirals_motion()
            self._log_spirals_motion()

            self.time += self.time_interval

    def _orbit_motion(self):
        sun_rotation = self.sun_contoller.rotation(self.time)
        sun_distance = self.sun_contoller.distance(self.time)

        self.orbit.sun.set_rotation(sun_rotation)
        self.orbit.sun.set_distance(sun_distance * self.scale)

        orbit_rotation = self.orbit_controller.rotation(self.time)
        self.orbit.set_rotation(orbit_rotation)

    def _arch_spirals_motion(self):
        rotation = self.arch_spirals_controller.rotation(self.time)
        self.arch_spirals.set_rotation(rotation)

    def _log_spirals_motion(self):
        rotation = self.log_spirals_controller.rotation(self.time)
        self.log_spirals.set_rotation(rotation)

    @pyqtSlot(dict)
    def update_parameters(self, new_parameters: dict):
        if new_parameters != {}:
            self._update_parameters(new_parameters)
            self.scene.clear()
            self.config_items()
            self.restart()

    def _update_parameters(self, new_parameters):
        for group, parameters in new_parameters.items():
            for name, value in parameters.items():
                self.parameters[group][name] = value

    def intersection_with_arch_spirals(self):
        sun_distance = self._distance(self.time) / self.scale

        V0 = self.parameters['arch_spirals']['V0']
        ro = self.parameters['arch_spirals']['ro']
        period = self.parameters['arch_spirals']['period']

        r = V0 * (28 + period / 2 * (self.k - 1) - self.time)
        if sun_distance > r:
            #print(self.time, sun_distance, r)
            self.k += 1

    def intersection_with_log_spirals(self):
        sun_rotation = self.orbit.sun_rotation(self.time) - 180
        sun_distance = self.orbit.sun_distance(self.time) / self.scale

        self.data['sun'].append(sun_distance)
        self.data['time'].append(self.time)

        period = self.parameters['log_spirals']['period']
        r0 = self.parameters['log_spirals']['r0']
        alpha = self.parameters['log_spirals']['alpha']
        arch_spiral_rotation = self.parameters['log_spirals']['rotation']
        omega = 360 / period


        #print(math.radians(sun_rotation) - omega * self.time)
        r = r0 * math.exp(alpha * math.radians(sun_rotation - omega * self.time + arch_spiral_rotation + 360) )
        self.data['log'].append(r)

        if abs(sun_distance - r) < 0.05:
            pass

    @pyqtSlot()
    def start(self):
        self.RUN = True

    @pyqtSlot()
    def stop(self):
        self.RUN = False

