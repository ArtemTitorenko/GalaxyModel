import sys
import json

from PyQt5 import QtWidgets
from main_widget import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    parameters = {
            'orbit': {
                's_major_axis': 8.45,
                'eccentricity': 0.36,
                'orbit_period': 2000,
                'sun_period': 250,
                'orbit_rotation': -10,
                'sun_rotation': 100,
            },

            'log_spirals': {
                'alpha': 0.218,
                'r0': 3,
                'period': 200,
                'rotation': 45,
                'width': 0.7,
            },

            'arch_spirals': {
                'ro': 2.48,
                'V0': 0.31164,
                'period': 50,
                'rotation': 80,
            },
    }

    # kpk at pixels
    scale = 25
    window = MainWindow(parameters, scale)
    window.show()

    sys.exit(app.exec_())

