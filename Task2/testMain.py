# Importing Packages
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
import sounddevice as sd
import testGUI as ss
from helpers import *
from popupWindow import Ui_OtherWindow


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
    # Window Mode
    windowMode = "Rectangle"

    def __init__(self, starterWindow):
        """
        Main loop of the UI
        :param mainWindow: QMainWindow Object
        """
        super(equalizerApp, self).setupUi(starterWindow)
        # Set Main View
        self.tabWidget.setCurrentIndex(0)

        # Setup popup Window
        self.popup_window = QtWidgets.QMainWindow()
        self.pop_ui = Ui_OtherWindow()
        self.pop_ui.setupUi(self.popup_window)

        # Initializations
        self.signalFile = ...  # the file loaded ---> data, Sampling Rate
        self.signalDataType = ...  # contains the data type of the signal
        self.signalFourier = ...  # fourier transform of the signal file data
        self.signalBands = ...  # Contains the signal bands
        self.signalBandsCopy = ...  # contains a copy of the signal bands for modification purposes
        self.signalModification = ...  # Contains the signal with the modified data
        self.signalModificationInv = ...  # Contains the data to be played and writen to wave
        self.filename = ...  # contains the file path
        self.format = ...  # contains the file format
        self.loadThread = loaderThread()  # contains the loader thread
        self.sliderValuesClicked = {0:..., 1:..., 2:..., 3:..., 4:..., 5:..., 6:..., 7:..., 8:..., 9:...}  # list contains the last pressed values
        self.results = {1:[], 2:[]}
        self.resultCounter = 1

        # encapsulations
        self.sliders = [self.verticalSlider, self.verticalSlider_2, self.verticalSlider_3, self.verticalSlider_4,
                        self.verticalSlider_5, self.verticalSlider_6, self.verticalSlider_7, self.verticalSlider_8,
                        self.verticalSlider_9, self.verticalSlider_10]

        # Widgets encapsulations
        self.frontWidgets = [self.inputSignalGraph, self.sliderChangedGraph]
        self.outputWidgets = [self.inputTimeOriginal, self.outputTimeModified, self.inputFourierOriginal, self.outputFourierModified]
        self.compareWidgets = [self.result1Plot, self.result2Plot]
        self.differenceWidgets = [self.pop_ui.timeDifference, self.pop_ui.fourierDifference]

        self.allWidgets = [self.frontWidgets, self.outputWidgets, self.compareWidgets, self.differenceWidgets]
        # buttons encapsulations
        self.playerButtons = [self.playButton, self.stopButton]
        self.outputButtons = [self.resetBands, self.showResult, self.playResult]
        self.saveButtons = [self.saveFile_btn, self.showDifference_btn, self.saveResult_btn, self.compareResult_btn]
        self.resultButtons = {1: [self.playCompare, self.stopCompare], 2: [self.playCompare_2, self.stopCompare_2]}
        self.windows = [self.rectangle, self.hanning, self.hamming]

        # Top Titles
        self.widgetTitles = ["Original Signal", "Changes Applied"]
        self.outputWidgetsTitles = ["Original Signal in Time", "Output Signal in Time", "Original Signal Fourier", "Output Signal Fourier"]
        self.compareTitles = ["First Result", "Second Result"]
        self.differenceTitles = ["Time Difference", "Fourier Difference"]

        self.allTitles = [self.widgetTitles, self.outputWidgetsTitles, self.compareTitles, self.differenceTitles]
        # Bottom Titles
        self.widgetsBottomLabels = ["No. of Samples", "Frequencies"]
        self.outputWidgetsBottomLabels = ["No. of Samples", "No. of Samples", "Frequencies", "Frequencies"]
        self.compareBottomLabels = ["Frequencies", "Frequencies"]
        self.differenceBottomLabels = ["No. of Samples", "Frequencies"]

        self.allButtomLabels = [self.widgetsBottomLabels, self.outputWidgetsBottomLabels, self.compareBottomLabels,
                                self.differenceBottomLabels]
        # pens configurations (Plot Colors)
        self.pens = [pg.mkPen(color=(255, 0, 0)), pg.mkPen(color=(0, 255, 0)),
                     pg.mkPen(color=(0, 0, 255)), pg.mkPen(color=(200, 87, 125)),
                     pg.mkPen(color=(123, 34, 203))]

        for encap in zip(self.allWidgets, self.allTitles, self.allButtomLabels):
            for widget, title, label in zip(encap[0], encap[1], encap[2]):
                widget.plotItem.setTitle(title)
                widget.plotItem.showGrid(True, True, alpha=0.8)
                widget.plotItem.setLabel("bottom", text=label)

        # Setup Y Range in Time Plot widgets
        for i in range(0, 2):
            self.outputWidgets[i].setYRange(-30000, 30000)

        self.inputSignalGraph.setYRange(-30000, 30000)

        # CONNECTIONSx
        self.actionload.triggered.connect(self.loadFile)
        for slider in self.sliders:
            slider.id = self.sliders.index(slider)
            slider.signal.connect(self.sliderChanged)

        self.playButton.clicked.connect(lambda : sd.play(self.signalFile["data"] ,  self.signalFile['frequency']))
        self.stopButton.clicked.connect(lambda : sd.stop())
        self.playResult.clicked.connect(lambda : sd.play(self.signalModificationInv.astype(self.signalDataType), self.signalFile['frequency']))
        self.resetBands.clicked.connect(self.resetAllBands)

        # Save Output Buttons
        self.showResult.clicked.connect(self.showResultOutput)
        self.saveFile_btn.clicked.connect(lambda: self.saveWaveFile(self.signalFile['frequency'], self.signalModificationInv))

        # Difference Button
        self.showDifference_btn.clicked.connect(self.showDifferenceWindow)

        #Compare Results
        self.saveResult_btn.clicked.connect(self.saveResult)
        self.compareResult_btn.clicked.connect(self.compareResults)
        self.playCompare.clicked.connect(lambda : sd.play(self.results[1][1].astype(self.signalDataType), self.signalFile['frequency']))
        self.playCompare_2.clicked.connect(lambda : sd.play(self.results[2][1].astype(self.signalDataType), self.signalFile['frequency']))
        self.stopCompare.clicked.connect(lambda : sd.stop())
        self.stopCompare_2.clicked.connect(lambda : sd.stop())

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
            self.loadThread.filepath = self.filename
            self.loadThread.start()
            self.loadThread.signal.connect(self.loadFileConfiguration)
            for btn in zip(self.playerButtons, self.outputButtons):
                btn[0].setEnabled(True)
                btn[1].setEnabled(True)

            self.outputButtons[2].setEnabled(True)

    def loadFileConfiguration(self, fileName):
        """
        takes the file from loadFile and plot the fourier transform of the signal and the original signal
        :param fileName: file path ... string
        :return: none
        """
        self.signalFile = fileName
        self.signalModificationInv = self.signalFile['data']
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
        try:
            if len(self.signalFile['dim']) == 2 :
                self.inputSignalGraph.plotItem.plot(self.signalFile['data'][:, 0], pem=self.pens[0]) # if 2d print one channel
                self.plotFourier(self.sliderChangedGraph, self.signalFourier['transformedData'][:, 0], pen=self.pens[1])
            else:
                # plotting
                self.inputSignalGraph.plotItem.plot(self.signalFile['data'], pem=self.pens[0])
                self.plotFourier(self.sliderChangedGraph, self.signalFourier['transformedData'], pen=self.pens[1])
        except:
            pass


    def sliderChanged(self, indx, val):
        """
        detects the changes in the sliders and plot these changes using the indx to the band given by th slider
        and the slider value which is the gain
        :param indx: int
        :param val: int
        :return: none
        """
        try:
            self.sliderChangedGraph.plotItem.clear()
            if val < 0 and not 0:
                self.sliderValuesClicked[indx] = 1/abs(val)
            else:
                self.sliderValuesClicked[indx] = val
            self.getWindow()
            self.signalModification = applyWindowFunction(indx, self.sliderValuesClicked, self.signalBandsCopy, equalizerApp.windowMode)
            try:
                 self.plotFourier(self.sliderChangedGraph, self.signalModification, self.pens[2])
            except:
                    print("failed")
                    pass
            self.signalModificationInv = inverseFourierTransform(self.signalModification, self.signalFile['dim'])
        except:
            pass

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

    def plotFourier(self, widgetName, data, pen):
        """
        plot the fourier transform of the data
        :data: the data to be plotted
        :return:
        """
        try:
            N = len(data)
            # Normalization
            yplot = 2* np.abs(data[: N//2]) / N
            widgetName.plotItem.plot(self.signalFourier['dataFrequencies'][: N//2], yplot, pen= pen)
        except:
            pass
    def resetAllBands(self):
        """
        resets al equalizer processes
        :return:
        """
        try:
            for slider in self.sliders:
                slider.setValue(1)
            self.sliderChangedGraph.plotItem.clear()
            self.plotUsingDimension()
            for slider, value in self.sliderValuesClicked.items():
                self.sliderValuesClicked[slider] = ...
            self.signalModification = ...
            self.signalModificationInv = self.signalFile['data']
        except :
            pass


    def showResultOutput(self):
        self.tabWidget.setCurrentIndex(1)

        for btn in self.saveButtons:
            btn.setEnabled(True)
        for widget in self.outputWidgets:
            widget.plotItem.clear()

        # Plot Original signal in inputTimeOriginal Widget
        self.inputTimeOriginal.plotItem.plot(self.signalFile['data'])

        # Plot Inverse of Original in outputTimeOriginal Widget
        self.outputTimeModified.plotItem.plot(self.signalModificationInv)

        # Plot Original Signal in inputFourierOriginal Widget
        self.plotFourier(self.inputFourierOriginal, self.signalFourier['transformedData'], pen=self.pens[2])

        #  Plot Fourier of Original in outputFourierOriginal Widget
        self.plotFourier(self.outputFourierModified, self.signalModification, pen=self.pens[3])

    def compareResults(self):
        """
        compares the two results saved by the user
        """
        self.tabWidget.setCurrentIndex(2)
        print(self.results[2])
        try:
            self.plotFourier(self.result1Plot, self.results[1][0], self.pens[4])
            for btn in self.resultButtons[1]:
                btn.setEnabled(True)
            self.plotFourier(self.result2Plot, self.results[2][0], self.pens[4])
            for btn in self.resultButtons[2]:
                btn.setEnabled(True)

        except IndexError:
            self.showMessage("Warning", "You can compare two results please choose and save the second result", QMessageBox.Ok, QMessageBox.Warning)


    def saveResult(self):
        if self.resultCounter > 2:
            print("No more yala")
        else:
            self.results[self.resultCounter].extend([self.signalModification, self.signalModificationInv])
            self.resultCounter +=1
        print(self.results)


    def saveWaveFile(self, rate, data):
        # dialog = QInputDialog()
        # text, okPressed = dialog.getText(dialog, "Save File", "File name:", QLineEdit.Normal, "")
        #
        # text = "results/" + text + ".wav"

        text = QtGui.QFileDialog.getSaveFileName(None, 'Save File', self.filename)[0]

        wavfile.write(text, rate, data.astype(self.signalDataType))


    def showDifferenceWindow(self):
        self.popup_window.show()
        self.pop_ui.timeDifference.plotItem.clear()
        self.pop_ui.fourierDifference.plotItem.clear()

        # Difference of signals in Time
        self.signalDiffInTime = self.signalModificationInv - self.signalFile['data']

        self.pop_ui.timeDifference.plotItem.plot(self.signalDiffInTime)

        # Difference of signals in Fourier
        self.signalDiffInFourier = self.signalModification - self.signalFourier['transformedData']
        self.plotFourier(self.pop_ui.fourierDifference, self.signalDiffInFourier, pen=self.pens[3])


    def showMessage(self, header,message, button, icon):
        msg = QMessageBox()
        msg.setWindowTitle(header)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(button)
        x = msg.exec_()


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

