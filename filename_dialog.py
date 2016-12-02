from PyQt4 import QtCore, QtGui

class FileDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)

        self.label = QtGui.QLabel("Enter a file name:")
        self.input = QtGui.QLineEdit()
        layout.addWidget(self.label)
        layout.addWidget(self.input)

        # OK and Cancel buttons
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # get current date and time from the dialog

    @property
    def filename(self):
        return self.input.text()

    # static method to create the dialog and return
    @staticmethod
    def show_dialog(parent = None):
        dialog = FileDialog(parent)
        result = dialog.exec_()
        return (dialog.filename, result == QtGui.QDialog.Accepted)