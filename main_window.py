import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from explorer import Explorer
from parameters_dialog import ParametersDialog

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parameters, scale, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parameters = parameters
        self.scale = scale
        self.explorer = Explorer(self.parameters, self.scale)

        self.parameters_dialog = ParametersDialog(self.parameters)
        self.parameters_dialog.updated_parameters[dict].connect(self.explorer.update_parameters)

        self.setCentralWidget(self.explorer)

        self.create_toolbar()
        self.create_menubar()

    def create_toolbar(self):
        toolbar = self.addToolBar('toolbar')

        start_icon = QIcon('./resources/icons/start.png')
        start_action = toolbar.addAction(start_icon, 'start')

        stop_icon = QIcon('./resources/icons/stop.png')
        stop_action = toolbar.addAction(stop_icon, 'stop')

        restart_icon = QIcon('./resources/icons/restart.png')
        restart_action = toolbar.addAction(restart_icon, 'restart')

        toolbar.setIconSize(QSize(15, 15))

        start_action.triggered.connect(self.explorer.start)
        stop_action.triggered.connect(self.explorer.stop)
        restart_action.triggered.connect(self.explorer.restart)

    def create_menubar(self):
        menu = self.menuBar()
        menu.setNativeMenuBar(False)

        parameters_menu = menu.addMenu('Параметры')

        update_parameters = parameters_menu.addAction('Изменить')
        update_parameters.triggered.connect(self.open_parameters_dialog)

        save_parameters = parameters_menu.addAction('Сохранить')
        load_parameters = parameters_menu.addAction('Загрузить')

        plot_menu = menu.addMenu('График')

        show_plot = plot_menu.addAction('Показать')
        save_plot = plot_menu.addAction('Сохранить')

    def create_statusbar(self):
        pass

    def open_parameters_dialog(self):
        self.parameters_dialog.show()

