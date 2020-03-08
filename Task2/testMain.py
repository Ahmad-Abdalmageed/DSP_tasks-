# Importing Packages
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
import sounddevice as sd
import testGUI as ss
from helpers import *
import threading
from scipy import signal as si


class loaderThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        super(loaderThread, self).__init__()
        self.filepath = ...
        self.file = ...

    def run(self):
        self.file = loadAudioFile(self.filepath)
        self.signal.emit(self.file)


class equalizerApp(ss.Ui_MainWindow):
    selectedSlider = 0
    windowMode = "Rectangle"

    def __init__(self, starterWindow):
        """
        Main loop of the UI
        :param mainwindow: QMainWindow Object
        """
        super(equalizerApp, self).setupUi(starterWindow)
        # Initializations
        self.signalFile = ... # the file loaded ---> data, Sampling Rate
        self.signalDataType = ... # contains the data type of the signal
        self.signalFourier = ... # fourier transform of the signal file data
        self.signalBands = ... # Contains the signal bands
        self.signalBandsCopy = ... # contains a copy of the signal bands for modification purposes
        self.signalModification = ... # Contains the signal with the modified data
        self.signalModificationInv = ... # Contains the data to be played and writen to wave
        self.filename = ... # contains the file path
        self.format = ... # contains the file format
        self.plotInputThread = ... # contains the plotter Thread for input signal
        self.plotFourierThread = ... # contains the plotter Thread for input signal fourier
        self.loadThread = loaderThread()# contains the loader thread
        self.sliderValuesClicked = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]} # list contains the last pressed values

        # encapsulations
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

        # Setup widget configurations
        for widget in self.frontWidgets:
            widget.plotItem.setTitle(self.widgetTitels[self.frontWidgets.index(widget)])
            widget.plotItem.showGrid(True, True, alpha=0.8)
            widget.plotItem.setLabel("bottom", text=self.widgetsBottomLabels[self.frontWidgets.index(widget)])



        # CONNECTIONS
        self.actionload.triggered.connect(self.loadFile)
        for slider in self.sliders:
            slider.id = self.sliders.index(slider)
            slider.signal.connect(self.sliderChanged)

        self.playButton.clicked.connect(lambda : sd.play(self.signalFile["data"] ,  self.signalFile['frequency']))
        self.stopButton.clicked.connect(lambda : sd.stop())
        # self.pauseButton.clicked.connect(lambda : sd.wait())
        self.playResult.clicked.connect(lambda : sd.play(self.signalModificationInv.astype(self.signalDataType), self.signalFile['frequency']))
        # self.playResult.clicked.connect(self.playResultFile)
        self.resetBands.clicked.connect(self.resetAllBands)

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
            # threading.Thread(target=self.loadFileConfiguration, args=(self.filename,)).start()
            self.loadThread.filepath = self.filename
            self.loadThread.start()
            self.loadThread.signal.connect(self.loadFileConfiguration)

    def loadFileConfiguration(self, fileName):
        """
        takes the file from loadFile and plot the fourier transform of the signal and the original signal
        :param fileName: file path ... string
        :return: none
        """
        self.signalFile = fileName
        self.signalDataType = self.signalFile['data'].dtype
        self.plotSignalLoaded()

    def plotSignalLoaded(self):
        """
        used by loadFileConfiguration to plot the signal
        :return: none
        """
        self.signalFourier = fourierTransform(self.signalFile)
        self.signalBands = createBands(self.signalFourier)
        self.signalBandsCopy = np.copy(self.signalBands)

        # on loading a new file
        for widget in self.frontWidgets:
            widget.plotItem.clear()
        self.plotUsingDimension()

    def plotUsingDimension(self):
        """
        used to plot the data from the specified fourier attribute to the specified graph
        :return: none
        """
       # check the dimensions of the signal and plot using best method
        if len(self.signalFile['dim']) == 2 : # TODO NOTE: not DRY
            self.inputSignalGraph.plotItem.plot(self.signalFile['data'][:, 0], pem=self.pens[0]) # if 2d print one channel
            self.plotFourier(self.signalFourier['transformedData'][:, 0], pen=self.pens[1])
        else:
            # plotting
            self.inputSignalGraph.plotItem.plot(self.signalFile['data'], pem=self.pens[0])
            self.plotFourier(self.signalFourier['transformedData'], pen=self.pens[1])



    def sliderChanged(self, indx, val):
        """
        detects the changes in the sliders and plot these changes using the indx to the band given by th slider
        and the slider value which is the gain
        :param indx: int
        :param val: int
        :return: none
        """
        print("slider %s value = %s"%(indx, val))
        if val in self.sliderValuesClicked[indx]:
            pass
        else:
            self.sliderChangedGraph.plotItem.clear()
            self.sliderValuesClicked[indx].append(val)
            self.getWindow()

            self.signalModification = applyWindowFunction(indx+1, val, self.signalBandsCopy, equalizerApp.windowMode)
            try:
                 self.plotFourier(self.signalModification, self.pens[2])
            except:
                print("failed")
                pass
            self.signalModificationInv = inverseFourierTransform(self.signalModification, self.signalFile['dim'])

    def getWindow(self):
        """
        identifies the seleted window
        :return: none
        """
        for window in self.windows:
            if window.isChecked():
                equalizerApp.windowMode = window.text()

    def playResultFile(self):
        """
        play the results from the sliders while checking the dimensions of the file
        :return:
        """
        if len(self.signalFile['dim']) == 2:
            self.dataType = type(self.signalFile['data'][0, 0])
        else:
            self.dataType = type(self.signalFile['data'][0])
        self.fourierArrayModified = np.copy(self.signalFourier['transformedData'])
        self.newInverse = inverseFourierTransform(self.fourierArrayModified, self.signalFile['dim'])
        sd.play(self.newInverse.astype(self.dataType), self.signalFile['frequency'])
        print(self.signalFile['frequency'])

    def plotFourier(self, data, pen):
        """
        plot the fourier transform of the data
        :data: the data to be plotted
        :return:
        """
        # T = 1 /
        N = len(data)
        # x = np.linspace(0.0, 1.0/2.0 * T, )
        yplot = 2.0 / N * np.abs(data[: N//2])
        self.sliderChangedGraph.plotItem.plot(yplot, pen= pen)

    def resetAllBands(self):
        """
        resets al equalizer processes
        :return:
        """
        for slider in self.sliders:
            slider.setValue(1)
        self.sliderChangedGraph.plotItem.clear()
        self.plotUsingDimension()
        for valueList in self.sliderValuesClicked.values():
            valueList[:] = []
        self.signalModificationInv = self.signalFile['data']

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

