# Importing Packages
import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
# from pyqtgraph import PlotWidget
import pandas as pd
import sounddevice as sd

import testGUI as ss
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
        self.signalFile = ... # the file loaded ---> data, Sampling Rate
        self.signalDataType = ... # contains the data type of the signal
        self.signalFourier = ... # fourier transform of the signal file data
        self.signalBands = ... # Contains the signal bands
        self.signalModification = ... # Contains the signal with the modified data
        self.signalModificationInv = ... # Contains the data to be played and writen to wave
        self.filename = ... # contains the file path
        self.format = ... # contains the file format

        self.sliders = [self.verticalSlider, self.verticalSlider_2, self.verticalSlider_3, self.verticalSlider_4,
                        self.verticalSlider_5, self.verticalSlider_6, self.verticalSlider_7, self.verticalSlider_8,
                        self.verticalSlider_9, self.verticalSlider_10]

        self.playerButtons = [self.playButton, self.pauseButton, self.stopButton]
        self.windows = [self.rectangle, self.hanning, self.hamming]
        self.frontWidgets = [self.inputSignalGraph, self.sliderChangedGraph]


        self.widgetTitels = ["Original Signal", "Changes Applied"]
        self.widgetsBottomLabels = ["No. of Samples", "Frequencies"]

        # pens configurations (Plot Colors)
        self.pens = [pg.mkPen(color=(255, 0, 0)), pg.mkPen(color=(0, 255, 0)),
                     pg.mkPen(color=(0, 0, 255)), pg.mkPen(color=(200, 87, 125)),
                     pg.mkPen(color=(123, 34, 203))]

        # Setuo windger configurations
        for i in self.frontWidgets:
            i.plotItem.setTitle(self.widgetTitels[self.frontWidgets.index(i)])
            i.plotItem.showGrid(True, True, alpha=0.8)
            i.plotItem.setLabel("bottom", text=self.widgetsBottomLabels[self.frontWidgets.index(i)])
            # i.setXRange(min = 0, max = 1000)
            # i.plotItem.hideButtons()

        # CONNECTIONS
        self.actionload.triggered.connect(self.loadFile)
        for i in self.sliders:
            i.id = self.sliders.index(i)
            i.signal.connect(self.sliderChanged)
        self.playButton.clicked.connect(lambda : sd.play(self.signalFile["data"] ,  self.signalFile['frequency']))
        self.stopButton.clicked.connect(lambda : sd.stop())
        self.pauseButton.clicked.connect(lambda : sd.wait())
        # self.playResult.clicked.connect(lambda : sd.play(self.signalModificationInv.astype(self.signalDataType), self.signalFile['frequency']))
        self.playResult.clicked.connect(self.playResultFile)

    def loadFile(self):
        """
        Load the File from User and add it to files dictionary
        :return:
        """
        # Open File
        self.filename, self.format = QtWidgets.QFileDialog.getOpenFileName(None, "Load Signal", "/home",
                                                                           "*.wav;;")
        # check if file not loaded (cancel loading....etc.)
        if self.filename == "":
            pass
        else:
            self.loadFileConfiguration(self.filename)

    def loadFileConfiguration(self, fileName):
        """
        takes the file path from loadFile and plot the fourier transform of the signal and the original signal
        :param fileName: file path ... string
        :return: none
        """
        self.signalFile = loadAudioFile(fileName)
        self.signalDataType = self.signalFile['data'].dtype
        self.plotSignalLoaded()

    def plotSignalLoaded(self):
        """
        used by loadFileConfiguration to plot the signal
        :return: none
        """
        self.signalFourier = fourierTransform(self.signalFile)
        self.signalBands = createBands(self.signalFourier)

        # on loading a new file
        for i in self.frontWidgets:
            i.plotItem.clear()

        # check the dimensions of the signal and plot using best method
        if len(self.signalFile['dim']) == 2 : # TODO NOTE: not DRY
            self.inputSignalGraph.plotItem.plot(self.signalFile['data'][:, 0], pem=self.pens[0]) # if 2d print one channel
            self.sliderChangedGraph.plotItem.plot(np.abs(self.signalFourier['transformedData'][:, 0])*2/len(self.signalFourier['transformedData'][:, 0]),
                                                  pen =self.pens[1])
        else:
            # plotting
            self.inputSignalGraph.plotItem.plot(self.signalFile['data'], pem=self.pens[0])
            self.sliderChangedGraph.plotItem.plot(2.0 / np.abs(self.signalFourier['transformedData'][: len(self.signalFourier['transformedData'])//2]), pen =self.pens[1])

    def sliderChanged(self, indx, val):
        """
        detects the changes in the sliders and plot these changes using the indx to the band given by th slider
        and the slider value which is the gain
        :param indx: int
        :param val: int
        :return: none
        """
        print("slider %s value = %s"%(indx, val))
        self.sliderChangedGraph.plotItem.clear()
        self.getWindow()
        if val != 0:
            self.signalModification = applyWindowFunction(indx+1, val, self.signalBands, equalizerApp.windowMode)
            self.signalModificationInv = inverseFourierTransform(self.signalModification, self.signalFile['dim'])
        try:
            print("this ", self.signalModification)
            self.sliderChangedGraph.plotItem.plot(np.real(self.signalModification), pen= self.pens[2])
        except:
            print("failed")
            pass

    def getWindow(self):
        """
        identifies the seleted window
        :return: none
        """
        for i in self.windows:
            if i.isChecked():
                equalizerApp.windowMode = i.text()

    def playResultFile(self):
        if len(self.signalFile['dim']) == 2:
            self.dataType = type(self.signalFile['data'][0, 0])
        else:
            self.dataType = type(self.signalFile['data'][0])
        self.fourierArrayModified = np.copy(self.signalFourier['transformedData'])

        self.newInverse = inverseFourierTransform(self.fourierArrayModified, self.signalFile['dim'])
        sd.play(self.newInverse.astype(self.dataType), self.signalFile['frequency'])
        print(self.signalFile['frequency'])


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
