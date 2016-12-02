from ast import literal_eval

import sys
from PyQt4 import QtGui
from flowlayout import FlowLayout
from dynamic_gridlayout import GridLayout
from calculator import Calculator
from filename_dialog import FileDialog


class Parser(QtGui.QWidget):
    reserved = ["Window", "Button", "Flow", "Grid", "End", "Panel", "Textfield", "Label", "Radio", "Group",
                "Layout", ":", ";", "."]

    def centered_window_size(self, size):
        x, y = size
        screen_resolution = self.app.desktop().screenGeometry()
        w, h = screen_resolution.width(), screen_resolution.height()
        return (w-x)/2, (h-y)/2, x, y

    def __init__(self, data, app):
        self._data = data
        self.tokens = []
        self.tokenizer()
        self._cursor = -1

        self.app = app
        super(self.__class__, self).__init__()

        self.start()

    def tokenizer(self):
        token = ""
        for current in self._data:
            if current.isspace():
                continue
            token += current
            if token in self.reserved:
                self.tokens.append(token)
                token = ""
            elif len(token) > 1 and '"' == token[0] == token[-1]:
                self.tokens.append(token[1:-1])
                token = ""
            elif "(" == token[0] and ")" == token[-1]:
                self.tokens.append(literal_eval(token))
                token = ""
            elif self.tokens and self.tokens[-1] == "Textfield":
                if token[-1] == ";":
                    self.tokens.append(int(token[:-1]))
                    self.tokens.append(token[-1])
                    token = ""

    def _next(self):
        self._cursor += 1

    @property
    def _current(self):
        try:
            print self.tokens[self._cursor]
            return self.tokens[self._cursor]
        except IndexError:
            return None

    def start(self):
        self.gui()
        self.show()

    def string(self):
        self._next()
        assert self._current not in self.reserved, "Reserved keyword cannot be <string>"  # do something
        return self._current.replace("&nbsp;", " ")

    def tuple(self, length):
        self._next()
        assert type(self._current) == tuple, "Expected <tuple>"
        assert len(self._current) == length, "Expected <tuple> of size %s" % length
        return self._current

    def number(self):
        self._next()
        assert type(self._current) == int, "Expected <int>"
        return self._current

    def window(self):
        self._next()
        assert self._current == "Window", "expected Window"

    def gui(self):
        self.window()
        self.setWindowTitle(self.string())
        self.setGeometry(*self.centered_window_size(self.tuple(2)))
        self.widgets(self.layout_(self))
        self.end()
        self.period()

    def widgets(self, parent):
        # _next = self.tokens[self._cursor+1]
        self.widget(parent)
        try:
            self.widgets(parent)
        except AssertionError:
            self._cursor -= 1  # reached a non-widget, rollback

    def radio(self):
        self._next()
        assert self._current == "Radio", "expected Radio"

    def radio_button(self):
        self.radio()
        name = self.string()
        self.semicolon()
        return QtGui.QRadioButton(name)

    def radio_buttons(self, group, parent):
        # _next = self.tokens[self._cursor+1]
        button = self.radio_button(); button.setProperty("id", self._cursor)
        parent.addWidget(button)
        group.addButton(button)
        try:
            self.radio_buttons(group, parent)
        except AssertionError, e:
            self._cursor -= 1  # reached a non-radio_button, rollback

    def widget(self, parent):
        self._next()
        if self._current == "Button":
            button = QtGui.QPushButton(self.string())
            parent.addWidget(button)
            self.semicolon()
        elif self._current == "Group":
            group = QtGui.QButtonGroup()
            self.radio_buttons(group, parent)
            self.end()
            self.semicolon()
        elif self._current == "Label":
            label = QtGui.QLabel(self.string())
            parent.addWidget(label)
            self.semicolon()
        elif self._current == "Panel":
            self.widgets(self.layout_(parent))
            self.end()
            self.semicolon()
        elif self._current == "Textfield":
            line = QtGui.QLineEdit(); line.setProperty("id", self._cursor)  # set an id to differentiate later # http://stackoverflow.com/questions/8600205/qlineedit-is-there-an-elegant-solution-to-tell-multiple-qlineedit-widgets-apart
            line.setMinimumWidth(self.number())
            parent.addWidget(line)
            self.semicolon()
        else:
            raise AssertionError, "Expected Button, Group, Label, Panel, or Textfield"

    def colon(self):
        self._next()
        assert self._current == ":", "expected ':'"

    def semicolon(self):
        self._next()
        assert self._current == ";", "expected ';'"

    def period(self):
        self._next()
        assert self._current == ".", "expected '.'"

    def end(self):
        self._next()
        assert self._current == "End", "expected End"

    def layout__(self):
        self._next()
        assert self._current == "Layout", "expected Layout"

    def layout_(self, parent):
        self.layout__()
        layout = self.layout_type(parent)
        self.colon()
        return layout

    def addLayout(self, QLayout):
        self.setLayout(QLayout)

    def layout_type(self, parent):
        self._next()
        if self._current == "Flow":
            flow_layout = FlowLayout()
            parent.addLayout(flow_layout)
            return flow_layout
        if self._current == "Grid":
            position_format = (0,0,0,0)
            try:
                position_format = self.tuple(4)
            except AssertionError:
                self._cursor -= 1
                try:
                    position_format = self.tuple(2) + (0, 0)
                except AssertionError:
                    raise AssertionError, "Expected type of size 2 or 4, got neither"
            grid_layout = GridLayout(position_format)
            parent.addLayout(grid_layout)
            return grid_layout
        else:
            raise AssertionError, "expected Flow or Grid"


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    dialog = FileDialog()
    filename, accepted = dialog.show_dialog()

    if accepted:
        f = open(filename, "r")
        string = f.read()

        x = Parser(string, app)
        calc = Calculator(app, x)
        sys.exit(app.exec_())
