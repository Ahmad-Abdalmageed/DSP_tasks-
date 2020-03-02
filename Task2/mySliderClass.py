from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class mySlider(QtWidgets.QSlider):
    # Signal to send to other slots, containing int which identifies the exct type of the sent
    signal = pyqtSignal(int)

    def __init__(self, id, *args):
        super().__init__(*args)
        self.id = id

    def mousePressEvent(self, QMouseEvent):
        super().mousePressEvent(QMouseEvent)
        self.signal.emit(self.id)
