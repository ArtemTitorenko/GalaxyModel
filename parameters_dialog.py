from collections import defaultdict

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog


class ParameterField(QWidget):

    def __init__(self,
                 group: str,
                 name: str,
                 value: float,
                 title: str = None,
                 parent=None):

        QWidget.__init__(self, parent=parent)

        self.group = group
        self.name = name
        self.title = title if title else self.name
        self.value = value

        self.line_edit = QLineEdit()
        self.label = QLabel()

        self.config_label()
        self.config_line_edit()
        self.init_ui()

    def config_label(self):
        title_pattern = '{} ='.format(self.title)
        self.label.setText(title_pattern)

    def config_line_edit(self):
        formatted_value = str(self.value)
        help_str = 'Число в виде 8 или 8.44'

        self.line_edit.setText(formatted_value)
        self.line_edit.setToolTip(help_str)

        self.line_edit.textEdited[str].connect(self.update_value)

    def update_value(self, text: str):
        try:
            value = float(text)
        except ValueError:
            return

        self.value = value

    def init_ui(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.label, alignment=QtCore.Qt.AlignLeft)
        hbox.addWidget(self.line_edit, alignment=QtCore.Qt.AlignRight)
        self.setLayout(hbox)


class ParametersDialog(QWidget):

    updated_parameters = QtCore.pyqtSignal(dict)

    def __init__(self, parameters: dict, parent=None):
        QWidget.__init__(self, parent=parent)

        self.parameters = parameters.copy()
        self.parameters_fields = []

        self.setWindowFlag(QtCore.Qt.Dialog)
        self.init_ui()

    def init_ui(self):
        main_box = QVBoxLayout()

        parameters_groups_box = QHBoxLayout()
        for group, parameters_group in self.parameters.items():
            group_box = self.group_vbox(group, parameters_group)
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

    def group_vbox(self, group: str, parameters: dict):
        group_box = QGroupBox(group)
        box_layout = QVBoxLayout()

        for name, value in parameters.items():
            parameter_field = ParameterField(group, name, value)
            self.parameters_fields.append(parameter_field)
            box_layout.addWidget(parameter_field)
        group_box.setLayout(box_layout)

        return group_box


    def clicked_ok(self):
        new_parameters = self.processing_parameters()
        self.updated_parameters.emit(new_parameters)
        self.close()

    def processing_parameters(self):
        new_parameters = defaultdict(dict)
        for parameter in self.parameters_fields:
            group, name, value = parameter.group, parameter.name, parameter.value
            curr_value = self.parameters[group][name]

            if curr_value != value:
                self.parameters[group][name] = value
                new_parameters[group][name] = value

        return new_parameters

