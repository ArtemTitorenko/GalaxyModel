import math

from array import array
from collections import defaultdict
from pyqtgraph import PlotWidget, mkPen


class IntersectionsManager:

    def __init__(self, parameters: dict, parent=None):
        self.parameters = parameters
        self.parent = parent

        self.graph_widget = PlotWidget()
        self._settings_graph_widget()

        self.restart()

    def _settings_graph_widget(self):
        self.graph_widget.setBackground('w')

        size_labels = 30
        self.graph_widget.setLabel('left', 'Расстояние до центра Галактики, кпк', size=size_labels)
        self.graph_widget.setLabel('bottom', 'Время, млн. лет', size=size_labels)

        plot_item = self.graph_widget.getPlotItem()

        axis = plot_item.getAxis('bottom')
        x_max, count_ticks = 600, 10
        ticks = reversed([x_max // count_ticks * i for i in range(0, x_max + 1)])
        #axis.setTicks([[(i, str(i)) for i in ticks]])

        plot_item.showGrid(x=True, y=True)
        plot_item.setXRange(0, 600)
        plot_item.setYRange(0, 16)
        plot_item.invertX(True)

    def update(self,
               time: float,
               sun_distance: float,
               sun_rotation: float):

        self.data_sun['x'].append(time)
        self.data_sun['y'].append(sun_distance)

        self.intersection_arch_spirals(time, sun_distance, sun_rotation)
        self.intersection_log_spirals(time, sun_distance, sun_rotation)

    def intersection_arch_spirals(self, time, sun_distance, sun_rotation):
        ro = self.parameters['arch_spirals']['ro']['value']
        period = self.parameters['arch_spirals']['period']['value']
        V0 = self.parameters['arch_spirals']['V0']['value']

        r_spiral = V0 * (28 + period / 2 * self.k - time)
        if sun_distance > r_spiral:
            self.data_arch_spirals['x'].append(time)
            self.data_arch_spirals['y'].append(sun_distance)
            self.k += 1

    def intersection_log_spirals(self, time, sun_distance, sun_rotation):
        r0 = self.parameters['log_spirals']['r0']['value']
        alpha = self.parameters['log_spirals']['alpha']['value']
        period = self.parameters['log_spirals']['period']['value']
        start_rotation = self.parameters['log_spirals']['rotation']['value']

        omega = 360 / period

        fi = math.radians(sun_rotation - omega * time + start_rotation - 90 + 360)
        r_spiral1 = r0 * math.exp(alpha * fi)

        fi = math.radians(sun_rotation - omega * time + start_rotation - 180 + 360)
        r_spiral2 = r0 * math.exp(alpha * fi)

        fi = math.radians(sun_rotation - omega * time + start_rotation + 360)
        r_spiral3 = r0 * math.exp(alpha * fi)

        fi = math.radians(sun_rotation - omega * time + start_rotation + 90 + 360)
        r_spiral4 = r0 * math.exp(alpha * fi)

        self.data_log_spirals['x'].append(time)
        self.data_log_spirals['y1'].append(r_spiral1)
        self.data_log_spirals['y2'].append(r_spiral2)
        self.data_log_spirals['y3'].append(r_spiral3)
        self.data_log_spirals['y4'].append(r_spiral4)

    def show_graph(self):
        self.graph_widget.clear()

        # sun trajectory
        x, y = self.data_sun['x'], self.data_sun['y']
        pen = mkPen(width=5)
        self.graph_widget.plot(x, y, pen=pen)

        # arch
        x, y = self.data_arch_spirals['x'], self.data_arch_spirals['y']
        self.graph_widget.plot(x, y, pen=None, symbol='+', symbolSize=10, symbolPen='b')

        # log
        x, y = self.data_log_spirals['x'], self.data_log_spirals['y1']
        pen = mkPen(width=5)
        self.graph_widget.plot(x, y, pen=pen)

        x, y = self.data_log_spirals['x'], self.data_log_spirals['y2']
        pen = mkPen(width=5)
        self.graph_widget.plot(x, y, pen=pen)

        x, y = self.data_log_spirals['x'], self.data_log_spirals['y3']
        pen = mkPen(width=5)
        self.graph_widget.plot(x, y, pen=pen)

        x, y = self.data_log_spirals['x'], self.data_log_spirals['y4']
        pen = mkPen(width=5)
        self.graph_widget.plot(x, y, pen=pen)

        self.graph_widget.show()

    def restart(self):
        self.k = 0
        self.graph_widget.clear()

        self.data_sun = defaultdict(list)
        self.data_arch_spirals = defaultdict(list)
        self.data_log_spirals = defaultdict(list)

