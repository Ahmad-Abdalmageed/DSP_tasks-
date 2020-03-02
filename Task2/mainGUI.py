# Importing Packages
import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
# from pyqtgraph import PlotWidget
import pandas as pd
import sounddevice as sd

import playground as ss
from mySliderClass import mySlider
from helpers import *


class equalizerApp(ss.Ui_MainWindow):
    selectedSlider = 0
    windowMode = "Rectangle"

    def __init__(self, starterWindow):
        """
        Main loop of the UI
        :param mainwindow: QMainWindow Object
        """
        super(equalizerApp, self).setupUi(starterWindow)

        self.sliderConfiguration()
        self.radioBoxesConfiguration()
        self.widgetsConfiguration()
        self.loadFileConfiguration()
        
        #Media Player Config.
        self.PlayAudio.clicked.connect(lambda : sd.play(self.audioFile["data"] ,  44100))
        self.StopAudio.clicked.connect(lambda: sd.stop())
        #self.PauseAudio.clicked.connect(lambda : sd.wait())

        # sliderBars Configurations #TODO Convert it to loop (DRY!!)
        self.sliderBars[0].valueChanged.connect(lambda: self.sliderChanged(0))
        self.sliderBars[1].valueChanged.connect(lambda: self.sliderChanged(1))
        self.sliderBars[2].valueChanged.connect(lambda: self.sliderChanged(2))
        self.sliderBars[3].valueChanged.connect(lambda: self.sliderChanged(3))
        self.sliderBars[4].valueChanged.connect(lambda: self.sliderChanged(4))
        self.sliderBars[5].valueChanged.connect(lambda: self.sliderChanged(5))
        self.sliderBars[6].valueChanged.connect(lambda: self.sliderChanged(6))
        self.sliderBars[7].valueChanged.connect(lambda: self.sliderChanged(7))
        self.sliderBars[8].valueChanged.connect(lambda: self.sliderChanged(8))
        self.sliderBars[9].valueChanged.connect(lambda: self.sliderChanged(9))

        # State of radioButtons
        for i in range(len(self.windowButtons)):
            self.windowButtons[i].toggled.connect(self.getWindowMode)

        # Connect of SlideBars
        for i in range(10):
            self.sliderBars[i].signal.connect(self.receiveSliderData)


        # Apply Fourier Transform
        self.fourierDictionary =  fourierTransform(self.audioFile)
        # print(self.fourierDictionary['transformedData'])
        # print(self.fourierDictionary['dataFrequencies'])

        # Apply Inverse Fourier Transform
        # self.inverseFourierDictionary = inverseFourierTransform()

        # pens configurations (Plot Colors)
        self.pens = [
            pg.mkPen(color=(255, 0, 0)),
            pg.mkPen(color=(0, 255, 0)),
            pg.mkPen(color=(0, 0, 255)),
            pg.mkPen(color=(200, 87, 125)),
            pg.mkPen(color=(123, 34, 203)),
        ]

        self.signalBands = createBands(self.fourierDictionary)
        # print(self.signalBands)

        # self.fourierArrayModified = applyWindowFunction(2, 4, self.signalBands)
        # print(self.fourierArrayModified)
        print("dataFrequencies Length: ", len(self.fourierDictionary['dataFrequencies']))

        self.widget1.plotItem.plot(self.audioArray, pen=self.pens[0])
        self.widget2.plotItem.plot(self.fourierDictionary['dataFrequencies'], self.fourierDictionary['transformedData'], pen=self.pens[1])
        # self.widget3.plotItem.plot(self.fourierArrayModified, pen=self.pens[2])

        print("Original: ", len(self.audioArray))
        print("Fourier: ", len(self.fourierDictionary['transformedData']))
        # print("Modified Fourier: ", len(self.fourierArrayModified))

        # Buttons Configuration
        # Reset Button
        self.resetButton.clicked.connect(self.resetSliders)

    def receiveSliderData(self, data):
        print("Slider Number: ", data)
        equalizerApp.selectedSlider = data

    def widgetsConfiguration(self):
        """
        Sets the plotting configurations
        :return:
        """
        # Channel 1
        # Setting ranges of the x and y axis
        self.widget1.setMinimumSize(QtCore.QSize(300, 200))
        self.widget1.plotItem.setTitle("Original Signal")
        self.widget1.plotItem.showGrid(True, True, alpha=0.8)
        self.widget1.plotItem.setLabel("bottom", text="No. Of Samples")

        self.widget2.setMinimumSize(QtCore.QSize(300, 200))
        self.widget2.plotItem.setTitle("Fourier Transform")
        self.widget2.plotItem.showGrid(True, True, alpha=0.8)
        self.widget2.plotItem.setLabel("bottom", text="Frequencies")

        self.widget3.setMinimumSize(QtCore.QSize(300, 200))
        self.widget3.enableAutoRange('y', True)
        self.widget3.plotItem.setTitle("Rectangle Window")
        self.widget3.plotItem.showGrid(True, True, alpha=0.8)
        self.widget3.plotItem.setLabel("bottom", text="Frequencies")

    def sliderConfiguration(self):
        # Initialize empty list of sliderBars
        self.sliderBars = []
        for i in range(10):
            self.sliderBars.append("self.sliderBar" + str(i+1))

        # Create instance for each slider
        for i in range(10):
            self.sliderBars[i] = mySlider(i+1, self.horizontalLayoutWidget)

        # Configure each slider
        for i in range(10):
            self.sliderBars[i].setMinimum(-5)
            self.sliderBars[i].setMaximum(5)
            self.sliderBars[i].setPageStep(1)
            self.sliderBars[i].setOrientation(QtCore.Qt.Vertical)
            self.sliderBars[i].setTickPosition(QtWidgets.QSlider.TicksBelow)
            self.sliderBars[i].setObjectName("slider" + str(i))
            self.horizontalLayout.addWidget(self.sliderBars[i])

    def loadFileConfiguration(self):
        # Load Wav File
        self.audioFile = loadAudioFile('audio/Casio-MT-45-16-Beat.wav')

        # Convert array of arrays To one array
        self.audioArray = np.concatenate(self.audioFile['data'])

        # Add it back to the original Dictionary
        self.audioFile['data'] = self.audioArray

        # Convert the array to series to plot it
        self.audioArray = pd.array(self.audioArray)

    def sliderChanged(self, sliderID):
        sliderValue = self.sliderBars[sliderID].value()
        self.getWindowMode()
        print(equalizerApp.windowMode)
        # tempArray = np.copy(self.fourierArrayModified)
        # print(type(tempArray))

        self.widget3.plotItem.clear()
        if sliderValue != 0:
            self.fourierArrayModified = applyWindowFunction(sliderID, sliderValue, self.signalBands, windowType=equalizerApp.windowMode)
        self.widget3.plotItem.plot(self.fourierArrayModified, pen=self.pens[2])
        # self.fourierArrayModified = tempArray

        #TODO Return the array to normal state before multiplying

    def radioBoxesConfiguration(self):
        self.windowButtons = [self.windowButton1, self.windowButton2, self.windowButton3]

    def getWindowMode(self):
        """
        get Window Type Choosed by user
        :return: windowMode
        """
        for i in range(len(self.windowButtons)):
            if self.windowButtons[i].isChecked():
                equalizerApp.windowMode = self.windowButtons[i].text()

        return equalizerApp.windowMode

    def resetSliders(self):
        for i in range(10):
            self.sliderBars[i].setValue(0)

        self.widget3.plotItem.clear()
        # self.widget3.plotItem.plot(self.fourierArrayModified, pen=self.pens[2])
        #TODO Need more handling

def main():
    """
    the application startup functions
    :return:
    """
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = equalizerApp(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
