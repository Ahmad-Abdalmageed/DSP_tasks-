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
        self.signalFourier = ... # fourier transform of the signal file data
        self.signalBands = ... # Contains the signal bands
        self.filename = ... # contains the file path
        self.format = ... # contains the file format

        self.sliders = [self.verticalSlider, self.verticalSlider_2, self.verticalSlider_3, self.verticalSlider_4,
                        self.verticalSlider_5, self.verticalSlider_6, self.verticalSlider_7, self.verticalSlider_8,
                        self.verticalSlider_9,]

        self.playerButtons = [self.playButton, self.pauseButton, self.stopButton]
        self.frontWidgets = [self.inputSignalGraph, self.inputSignalFourier, self.sliderChangedGraph]

        self.windgetTitels = ["Original Signal", "Fourier Transform", "Changes Applied"]
        self.widgetsBottomLabels = ["No. of Samples", "Frequencies", "Frequencies"]
        # pens configurations (Plot Colors)
        self.pens = [pg.mkPen(color=(255, 0, 0)), pg.mkPen(color=(0, 255, 0)),
                     pg.mkPen(color=(0, 0, 255)), pg.mkPen(color=(200, 87, 125)),
                     pg.mkPen(color=(123, 34, 203)),]

        for i in self.frontWidgets:
            i.plotItem.setTitle(self.windgetTitels[self.frontWidgets.index(i)])
            i.plotItem.showGrid(True, True, alpha=0.8)
            i.plotItem.setLabel("bottom", text=self.widgetsBottomLabels[self.frontWidgets.index(i)])
            i.setXRange(min = 0, max = 1000)

        self.actionload.triggered.connect(self.loadFile)

    # Load File
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
        self.signalFile = loadAudioFile(fileName)
        self.plotSignalLoaded()

    def plotSignalLoaded(self):
        self.signalFourier = fourierTransform(self.signalFile)

        # on loading a new file
        for i in self.frontWidgets:
            i.plotItem.clear()

        if len(self.signalFile['dim']) == 2 :
            print("2Dimensional shit")
            pass
        # plotting
        self.inputSignalGraph.plotItem.plot(self.signalFile['data'], pem=self.pens[0])
        # self.inputSignalFourier.plotItem.plot(self.signalFourier['dataFrequencies'],
        # np.abs(self.signalFourier['transformedData'])*2/len(self.signalFourier['transformedData']), pen =self.pens[1])




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
