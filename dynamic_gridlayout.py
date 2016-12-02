from PyQt4 import QtGui, QtCore


class GridLayout(QtGui.QGridLayout):
    def __init__(self, position_format):
        super(self.__class__, self).__init__(None)

        self.rows, self.columns, self.x_gap, self.y_gap = position_format
        self.positions = list(reversed([(i,j) for i in range(self.rows) for j in range(self.columns)]))

    def addWidget(self, QWidget, p_int=None, p_int_1=None, *__args):
        try:
            next_position = self.positions.pop()
        except IndexError:
            raise IndexError, "Too many widgets for GridLayout!"
        super(self.__class__, self).addWidget(QWidget, *next_position)

    def addLayout(self, QLayout):
        widget = QtGui.QWidget()
        widget.setLayout(QLayout)
        self.addWidget(widget)
