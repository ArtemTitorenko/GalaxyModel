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
from .intersections_manager import IntersectionsManager

from .graphical_items.spirals import SystemArchimedeanSpirals
from .graphical_items.spirals import SystemLogarithmicSpirals


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
        self.settings_items()

        self.restart()

    def init_ui(self):
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.view)
        self.setLayout(vbox)

    def settings_items(self):
        self.scene.clear()

        self._settings_orbit()
        self._settings_arch_spirals()
        self._settings_log_spirals()

        self._manager = IntersectionsManager(self.parameters, self)

    def _settings_orbit(self):
        eccentricity = self.parameters['orbit']['eccentricity']['value']
        s_major_axis = self.parameters['orbit']['s_major_axis']['value']
        self.orbit = EllipticalOrbitItem(eccentricity,
                                         s_major_axis * self.scale)

        sun_period = self.parameters['orbit']['sun_period']['value']
        sun_rotation = math.radians(self.parameters['orbit']['sun_rotation']['value'])
        self.sun_contoller = EllipticalKeplersMotion(sun_period,
                                                     s_major_axis,
                                                     eccentricity,
                                                     sun_rotation)

        orbit_period = self.parameters['orbit']['orbit_period']['value']
        orbit_rotation = math.radians(self.parameters['orbit']['orbit_rotation']['value'])
        self.orbit_controller = CircularMotion(orbit_period, orbit_rotation)

        self.scene.addItem(self.orbit)

    def _settings_arch_spirals(self):
        ro = self.parameters['arch_spirals']['ro']['value']
        radius_center = self.orbit.radius_center()
        self.arch_spirals = SystemArchimedeanSpirals(ro * self.scale,
                                                     radius_center)

        period = self.parameters['arch_spirals']['period']['value']
        rotation = math.radians(self.parameters['arch_spirals']['rotation']['value'])
        self.arch_spirals_controller = CircularMotion(period, rotation)

        for spiral in self.arch_spirals.items():
            self.scene.addItem(spiral)

    def _settings_log_spirals(self):
        alpha = self.parameters['log_spirals']['alpha']['value']
        r0 = self.parameters['log_spirals']['r0']['value'] * self.scale
        width = self.parameters['log_spirals']['width']['value'] * self.scale
        self.log_spirals = SystemLogarithmicSpirals(alpha, r0, width)

        period = self.parameters['log_spirals']['period']['value']
        rotation = math.radians(self.parameters['log_spirals']['rotation']['value'])
        self.log_spirals_controller = CircularMotion(period, rotation)

        for spiral in self.log_spirals.items():
            self.scene.addItem(spiral)

    def timerEvent(self, event):
        self.run()

    def run(self):
        if self.RUN:
            self._orbit_motion()
            self._arch_spirals_motion()
            self._log_spirals_motion()
            self._update_manager()

            self.time += self.time_interval

    @pyqtSlot()
    def restart(self):
        self.time = 0
        self.RUN = False

        self._orbit_motion()
        self._arch_spirals_motion()
        self._log_spirals_motion()

        self._manager.restart()

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

    def _update_manager(self):
        start_sun_rotation = self.parameters['orbit']['sun_rotation']['value']
        sun_rotation = self.sun_contoller.full_rotation(self.time)
        orbit_rotation = self.orbit_controller.rotation(self.time)
        sun_distance = self.sun_contoller.distance(self.time)

        sun_rotation = sun_rotation + math.degrees(orbit_rotation) - 90
        self._manager.update(self.time, sun_distance, sun_rotation)

    @pyqtSlot(dict)
    def update_parameters(self, new_parameters: dict):
        self.parameters = new_parameters
        self.settings_items()
        self.restart()

    @pyqtSlot()
    def start(self):
        self.RUN = True

    @pyqtSlot()
    def stop(self):
        self.RUN = False

    @pyqtSlot()
    def show_graph(self):
        self._manager.show_graph()

