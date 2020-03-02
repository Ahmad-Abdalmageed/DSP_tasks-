from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class Sliders(QWidget):
    def __init__(self):
        super().__init__()
        self.sliderList = []
        self.layout = QVBoxLayout()
        self.ctr = 0
        for i in range(10):

            slider = QSlider()
            slider.setMinimum(-5)
            slider.setMaximum(5)
            slider.setPageStep(1)
            slider.setOrientation(Qt.Vertical)
            slider.setTickPosition(QSlider.TicksBelow)
            self.sliderList.append(slider)
            slider.valueChanged.connect(lambda: self.valueChanged(self.ctr))
            self.ctr += 1
            self.layout.addWidget(slider)


        self.setLayout(self.layout)
        self.show()


    def valueChanged(self, i):
        print("Slider {} is changing".format(i))





if __name__ == "__main__" :
    app = QApplication(sys.argv)
    win = Sliders()
    sys.exit(app.exec_())
