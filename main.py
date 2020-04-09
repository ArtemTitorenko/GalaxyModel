import sys

from PyQt5 import QtWidgets
from main_window import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    parameters = {
            's_major_axis': 8.44,
            'eccentricity': 0.36,
            'orbital_period': 300,
            'sun_period': 250,
            'orbital_rotation': 0,
            'sun_rotation': 90,
    }

    # kpk at pixels
    scale = 25
    window = MainWindow(parameters, scale)
    window.show()

    sys.exit(app.exec_())

