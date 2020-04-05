from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog


class ParameterField(QWidget):

    def __init__(self, name: str, value: float, title: str = None, parent=None):
        QWidget.__init__(self, parent=parent)

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

        self.parameters_values = parameters.copy()
        self.parameters_fields = []

        self.setWindowFlag(QtCore.Qt.Dialog)
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

        for name, value in self.parameters_values.items():
            parameter_field = ParameterField(name, value)
            self.parameters_fields.append(parameter_field)
            vbox.addWidget(parameter_field)

        button_ok = QPushButton('Окей')
        button_ok.clicked.connect(self.clicked_ok)

        vbox.addWidget(button_ok)
        self.setLayout(vbox)

    def clicked_ok(self):
        new_parameters = self.processing_parameters()
        self.updated_parameters.emit(new_parameters)
        self.close()

    def processing_parameters(self):
        new_parameters = {}
        for parameter in self.parameters_fields:
            name, value = parameter.name, parameter.value
            curr_value = self.parameters_values[name]

            if curr_value != value:
                self.parameters_values[name] = value
                new_parameters[name] = value

        return new_parameters

