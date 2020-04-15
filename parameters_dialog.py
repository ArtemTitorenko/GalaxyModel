from collections import defaultdict

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog


class FieldParameter(QWidget):

    def __init__(self, name: str, config: dict, *args, **kwargs):
        super().__init__()

        self.config = config
        self.name = name

        self.line_edit = QLineEdit()
        self.label = QLabel()

        self.settings_line_edit()
        self.settings_label()
        self.settings_ui()

    def settings_line_edit(self):
        formatted_value = str(self.config['value'])
        help_str = 'Число в виде 8 или 8.44'

        self.line_edit.setText(formatted_value)
        self.line_edit.setToolTip(help_str)

        self.line_edit.textEdited[str].connect(self.update_value)

    def settings_label(self):
        label = self.config.get('title', self.name)
        measure = self.config.get('measure', '')
        title_pattern = '{} {} ='.format(label, measure)
        self.label.setText(title_pattern)

    def update_value(self, text: str):
        try:
            value = float(text)
        except ValueError:
            return
        else:
            self.config['value'] = value

    def settings_ui(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.label, alignment=QtCore.Qt.AlignLeft)
        hbox.addWidget(self.line_edit, alignment=QtCore.Qt.AlignRight)
        self.setLayout(hbox)

class GroupParameters(QGroupBox):

    def __init__(self, title: str, parameters: dict, *args, **kwargs):
        super().__init__(title)

        self.parameters = parameters
        self.settings_ui()

    def settings_ui(self):
        main_box = QVBoxLayout()
        for name, config in self.parameters.items():
            field = FieldParameter(name, config)
            main_box.addWidget(field)
        self.setLayout(main_box)

class ParametersDialog(QWidget):

    updated_parameters = QtCore.pyqtSignal(dict)

    def __init__(self, parameters: dict, parent=None):
        QWidget.__init__(self, parent=parent)

        self.parameters = parameters.copy()

        self.setWindowFlag(QtCore.Qt.Dialog)
        self.settings_ui()

    def settings_ui(self):
        main_box = QVBoxLayout()

        parameters_groups_box = QHBoxLayout()
        for group, parameters_group in self.parameters.items():
            group_box = GroupParameters(group, parameters_group)
            parameters_groups_box.addWidget(group_box)

        main_box.addLayout(parameters_groups_box)

        buttons_box = QHBoxLayout()

        button_ok = QPushButton('Окей')
        button_ok.clicked.connect(self.clicked_ok)
        buttons_box.addWidget(button_ok)

        button_cancel = QPushButton('Отмена')
        button_cancel.clicked.connect(self.close)
        buttons_box.addWidget(button_cancel)

        main_box.addLayout(buttons_box)
        self.setLayout(main_box)

    def clicked_ok(self):
        self.updated_parameters.emit(self.parameters)
        self.close()

