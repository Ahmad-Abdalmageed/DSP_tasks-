from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
import startstop3 as ss
#import run as ss
import pandas as pd
from scipy.io import loadmat
import sys



class signalViewer(ss.Ui_MainWindow):
    i = 0 # counter represents the chunks size of data to be loaded
    filenames = dict()
    channels = dict()
    chunks = dict()
    graphs = dict()
    channel = -1  # Current Channel
    numOfPanels = 0


    def __init__(self, mainwindow, speed):
        '''
        Main loop of the UI
        :param mainwindow: QMainWindow Object
        '''
        super(signalViewer, self).setupUi(mainwindow)
        self.speed = speed
        self.filename, self.format = None, None
        self.widget_2 = None
        self.widget_3 = None
        self.widget_4 = None
        self.widget_5 = None
        self.widgets = [self.widget, self.widget_2, self.widget_3, self.widget_4, self.widget_5]

        self.pens = [pg.mkPen(color=(255, 0, 0)),pg.mkPen(color=(0, 255, 0)),
                     pg.mkPen(color=(0, 0, 255)), pg.mkPen(color=(200, 87, 125)),
                     pg.mkPen(color=(123, 34, 203))]

        # Plot Configurations
        self.plot_conf()
        # Load Button connectorchecked
        self.actionAdd.triggered.connect(self.addNewPanel)
        self.channel1_chk.toggled.connect(self.hideChannel_1)
        self.channel2_chk.toggled.connect(self.hideChannel_2)
        self.channel3_chk.toggled.connect(self.hideChannel_3)
        self.channel4_chk.toggled.connect(self.hideChannel_4)
        self.channel5_chk.toggled.connect(self.hideChannel_5)
        self.actionReset.triggered.connect(self.resetAllPanels)
        self.actionLoad.triggered.connect(self.load_file)
        self.timer()
        self.view = self.widget.plotItem.getViewBox()
        self.zoom.clicked.connect(self.zoomf)

        print(self.view)


    def zoomf(self):
        self.view.scaleBy(0.3)

    def load_file(self):
        """
        Load the File from User and add it to files dictionary
        :return:
        """
        signalViewer.i = 0
        print("Adding new panel..")
        # Reset the dict to accept new file
        signalViewer.chunks = dict()
        # Stop timer for waiting to upload new file
        self.timer.stop()
        # Open File
        self.filename , self.format= QtWidgets.QFileDialog.getOpenFileName(None, 'Load Signal','/home', "*.csv;;"
                                                                                                        " *.txt;;"
                                                                                                        "*.mat")
        if self.filename == '' :
            pass
        else: signalViewer.channel += 1

        if self.filename in signalViewer.filenames:
            print("You Already choosed that file ")
        else:
            signalViewer.filenames[self.filename] = self.format
        self.checkFileExt(signalViewer.filenames)

    def plot_conf(self):
        """
        Sets the plotting configurations
        :return:
        """
        # Channel 1
        # Setting ranges of the x and y axis
        self.widget.setXRange(min=0, max=4000)
        self.widget.setYRange(min=-1, max=1)
        self.widget.setMouseEnabled(x=False, y=False)
        self.widget.plotItem.setTitle("Main Window")
        self.widget.plotItem.addLegend(size=(2, 3))
        self.widget.plotItem.showGrid(True, True, alpha=0.8)
        self.widget.plotItem.setLabel('bottom', text='Time (ms)')


    # Reading Files Functions
    def load_csv_data(self, file_name):
        """
        load the data from user if the file format is a .csv format
        :param file_name: file path ... string
        :return:
        """
        if file_name in signalViewer.channels :
            print("You Already Loaded this file1")
        else:
            # Return dataFrame (data)
            signalViewer.channels[file_name] = pd.read_csv(file_name)

            # Return y chunk (data line)
            signalViewer.chunks[file_name] = signalViewer.channels[file_name].iloc[:1,1]

            # Plot chunk
            self.plot(file_name, signalViewer.chunks[file_name])

    def load_mat_data(self, file_name):
        """
        load the data from user if the file format is a .mat format
        :param file_name: file path ... string
        :return:
        """
        if file_name in signalViewer.channels:
            print("You already loaded this file2")
        else:
            mat_file = loadmat(file_name)
            signalViewer.channels[file_name] = pd.DataFrame(mat_file['F'])
            signalViewer.chunks[file_name] = signalViewer.channels[file_name].iloc[:1, 1]
            self.plot(file_name, signalViewer.chunks[file_name])

    def load_txt_data(self, file_name):
        """
        load the data from user if the file format is a .txt format
        :param file_name: file path ... string
        :return:
        """
        if file_name in signalViewer.channels:
            print("You already loaded this file3")
        else :
            signalViewer.channels[file_name] = pd.read_csv(file_name, skiprows=[i for i in range(500,7657)])
            # self.y = self.data.iloc[:1, 2]
            signalViewer.chunks[file_name] = signalViewer.channels[file_name].iloc[:1, 2]
            self.plot(file_name, signalViewer.chunks[file_name])


    def plot(self, file_name, chunk):
        '''
        main plotting function
        :return:
        '''
        # File name
        name = file_name.split('/')[-1]

        signalViewer.graphs[file_name] = self.widgets[signalViewer.channel].plotItem.plot(chunk, name=name,
                                                                                          pen=self.pens[signalViewer.channel])


    def update_plot_data(self):
        '''
        update function .... add chunks to self.y from loaded data self.data
        :return:
        '''

        for chunk in signalViewer.chunks:  # graph ->> file_name
            signalViewer.i += 30
            signalViewer.chunks[chunk] = pd.concat([signalViewer.chunks[chunk],
                                                    signalViewer.channels[chunk].iloc[signalViewer.i:signalViewer.i+self.speed, 1]],
                                                   axis=0,sort=True)

            signalViewer.graphs[chunk].setData(signalViewer.chunks[chunk])


    def timer(self):
        """
        Timer function that executes the data updating for every n ms
        :return:
        """
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.start_timer()
        self.pause_timer()


    def start_timer(self):
        '''
        Event of clicking the start button which starts the signal plotting
        :return:
        '''
        self.actionStart.triggered.connect(self.timer.start)

    def pause_timer(self):
        '''
        Event of clicking the stop button which stops the signal plotting
        :return:
        '''
        self.actionPause.triggered.connect(self.timer.stop)

    def checkFileExt(self, file):
        """
        Checks the file format loaded by the user and maps to appropriate function
        :param file: File dictionary updated by the load function
        :return:
        """
        for i in file.items():
            if i[1] == '*.csv':
                self.load_csv_data(i[0])
            elif i[1] == '*.txt':
                self.load_txt_data(i[0])
            elif i[1] == '*.mat':
                self.load_mat_data(i[0])

    def resetAllPanels(self):
        print("Deleting panels...")

    def addNewPanel(self):
        if signalViewer.numOfPanels > 3:
            print("No more than 5 plots")
            self.show_popup("Maximum number of channels is 5", "You can't add more than 5 channels, you have to delete one first")
        else:
            signalViewer.numOfPanels += 1
            spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.verticalLayout.addItem(spacerItem)
            self.widgets[signalViewer.numOfPanels] = pg.PlotWidget(self.scrollAreaWidgetContents)
            self.widgets[signalViewer.numOfPanels].setEnabled(True)
            self.widgets[signalViewer.numOfPanels].setMinimumSize(QtCore.QSize(500, 300))
            self.widgets[signalViewer.numOfPanels].setObjectName("widget_3")
            self.widgets[signalViewer.numOfPanels].setXRange(min=0, max=4000)
            self.widgets[signalViewer.numOfPanels].setYRange(min=-1, max=1)
            self.widgets[signalViewer.numOfPanels].setMouseEnabled(x=False, y=False)
            self.widgets[signalViewer.numOfPanels].plotItem.setTitle("Main Window")
            self.widgets[signalViewer.numOfPanels].plotItem.addLegend(size=(2, 3))
            self.widgets[signalViewer.numOfPanels].plotItem.showGrid(True, True, alpha=0.8)
            self.widgets[signalViewer.numOfPanels].plotItem.setLabel('bottom', text='Time (ms)')
            self.verticalLayout.addWidget(self.widgets[signalViewer.numOfPanels])
            print(self.widgets[1])
            print(self.widgets[2])
    def hideChannel_1(self):
        self.widgets[0].setHidden(not self.widget.isHidden())

    def hideChannel_2(self):
        if self.widgets[1] is None :
            self.show_popup("Channel Doesn`t exist", "You didn`t add this channel")
        else:
            self.widgets[1].setHidden(not self.widgets[1].isHidden())

    def hideChannel_3(self):
        if self.widgets[2] is None :
            self.show_popup("Channel Doesn`t exist", "You didn`t add this channel")
        else:
            self.widget_3.setHidden(not self.widgets[2].isHidden())

    def hideChannel_4(self):
        if self.widgets[3] is None :
            self.show_popup("Channel Doesn`t exist", "You didn`t add this channel")
        else :
            self.widget_4.setHidden(not self.widgets[3].isHidden())

    def hideChannel_5(self):
        if self.widgets[4] is None :
            self.show_popup("Channel Doesn`t exist", "You didn`t add this channel")
        else:
            self.widget_5.setHidden(not self.widgets[4].isHidden())



    def show_popup(self, message, info):
        msg = QMessageBox()
        msg.setWindowTitle("Popup Message")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Retry | QMessageBox.Ignore)
        msg.setDefaultButton(QMessageBox.Ignore)
        msg.setInformativeText(info)
        msg.setDetailedText("details")
        msg.buttonClicked.connect(self.popup_button)
        x = msg.exec_()
    def popup_button(self, i):
        print(i.text())

def main():
    '''
    the application startup functions
    :return:
    '''
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = signalViewer(MainWindow, speed=50)
    MainWindow.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
