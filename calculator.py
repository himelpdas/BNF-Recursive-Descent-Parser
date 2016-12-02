from PyQt4 import QtGui

class Calculator:

    def __init__(self, app, widget):
        self.app = app
        self.widget = widget
        self.input1 = self.output = self.input2 = None
        self.radio_input1 = self.radio_input2 = None

        self.set_q_line_edits()
        self.set_q_radio_buttons()

        self.set_q_button_events()

    def set_q_line_edits(self):
        q_line_edits = []
        for widget in self.app.allWidgets():
            if isinstance(widget, QtGui.QLineEdit):
                if widget.property("id").toPyObject():  # http://stackoverflow.com/questions/9257422/how-to-get-the-original-python-data-from-qvariant
                    q_line_edits.append(widget)

        # no guarantee it's in order
        q_line_edits = sorted(q_line_edits, key=lambda e: e.property("id").toPyObject())

        self.input1, self.output, self.input2 = q_line_edits
        self.input1.setDisabled(True)
        self.output.setDisabled(True)
        self.input2.setDisabled(True)

    def set_q_radio_buttons(self):
        q_radio_buttons = []

        for widget in self.app.allWidgets():
            if isinstance(widget, QtGui.QRadioButton):
                if widget.property("id").toPyObject():  # http://stackoverflow.com/questions/9257422/how-to-get-the-original-python-data-from-qvariant
                    q_radio_buttons.append(widget)

        q_radio_buttons = sorted(q_radio_buttons, key=lambda e: e.property("id").toPyObject())

        self.radio_input1, self.radio_input2 = q_radio_buttons
        self.radio_input1.setChecked(True)

    def set_q_button_events(self):
        for widget in self.app.allWidgets():
            if isinstance(widget, QtGui.QPushButton):
                widget.clicked.connect(self.q_button_handler)

    def q_button_handler(self):
        pressed = self.widget.sender()
        pressed_text = str(pressed.text())
        if pressed_text in "+-x/":
            operator = pressed_text.replace("x", "*")
            try:
                input1 = float(self.input1.text())
                input2 = float(self.input2.text())
            except ValueError:
                self.output.setText("INPUT ERROR")
            else:
                try:
                    out = eval("%s%s%s"%(input1, operator, input2))
                    self.output.setText(str(out))
                except ZeroDivisionError:
                    self.output.setText("ZERO DIVISION")
        elif pressed_text in "0123456789BC":
            input = self.input1 if self.radio_input1.isChecked() else self.input2
            if pressed_text == "B":
                input.backspace()
            elif pressed_text == "C":
                input.setText("")
            else:
                input.insert(pressed_text)