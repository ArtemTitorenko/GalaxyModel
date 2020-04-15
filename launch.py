import sys
import json

from PyQt5 import QtWidgets
from main_widget import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    parameters = {
            'orbit': {
                's_major_axis': {
                    'value': 8.45,
                    'measure': 'kpk',
                },
                'eccentricity': {
                    'value': 0.36,
                    'measure': '',
                },
                'orbit_period': {
                    'value': 2000,
                    'measure': 'mln. years',
                },
                'sun_period': {
                    'value': 250,
                    'measure': 'mln. years',
                },
                'orbit_rotation': {
                    'value': -10,
                    'measure': 'degrees',
                },
                'sun_rotation': {
                    'value': 100,
                    'measure': 'degrees',
                },
            },
            'log_spirals': {
                'alpha': {
                    'value': 0.218,
                    'measure': '',
                },
                'r0': {
                    'value': 3,
                    'measure': 'kpk',
                },
                'period': {
                    'value': 200,
                    'measure': 'mln. years',
                },
                'rotation': {
                    'value': 45,
                    'measure': 'degrees',
                },
                'width': {
                    'value': 0.7,
                    'measure': 'kpk',
                },
            },

            'arch_spirals': {
                'ro': {
                    'value': 2.48,
                    'measure': '',
                },
                'V0': {
                    'value': 0.31164,
                    'measure': '',
                },
                'period': {
                    'value': 50,
                    'measure': 'mln. years',
                },
                'rotation': {
                    'value': 80,
                    'measure': 'degrees',
                }
            },
    }

    # kpk at pixels
    scale = 25
    window = MainWindow(parameters, scale)
    window.show()

    sys.exit(app.exec_())

