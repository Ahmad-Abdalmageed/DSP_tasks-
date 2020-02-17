from PyQt5 import QtWidgets, uic, QtCore, QtGui
import pyqtgraph as pg
import startstop3 as ss
import pandas as pd
from scipy.io import loadmat
import sys
from pyqtgraph import PlotWidget

class signalViewer(ss.Ui_MainWindow):
    i = 0 # counter represents the chunks size of data to be loaded
    channel = 1
    filenames = dict()
    channels = dict()

    def __init__(self, mainwindow, speed):
        '''
        Main loop of the UI
        :param mainwindow: QMainWindow Object
        '''
        super(signalViewer, self).setupUi(mainwindow)
        self.speed = speed
        # Plot Configurations
        # Pen color
        self.pen1 = pg.mkPen(color=(0, 255, 0))
        # Setting ranges of the x and y axis
        self.widget.setXRange(min=0, max=4000)
        # set title and add legend
        self.widget.plotItem.setTitle("Main Window")
        self.widget.plotItem.addLegend(size=(2, 3))
        # Grid
        self.widget.plotItem.showGrid(True, True, alpha=0.8)
        self.widget.plotItem.setLabel('bottom', text='Time (ms)')
        self.view = self.widget.plotItem.getViewBox()
        # TODO : Set Auto Panning

        # Load Button connector
        self.load_bt.clicked.connect(self.load_file)

    def load_file(self):
        self.filename , self.format= QtWidgets.QFileDialog.getOpenFileName(None, 'Load Signal','/home', "*.csv;;"
                                                                                                        " *.txt;;"
                                                                                                        "*.mat")
        if self.filename in signalViewer.filenames:
            print("You Already choosed that file ")
        else:
            signalViewer.filenames[self.filename] = self.format
        print(self.filename)
        # self.signal_file = self.filename.split("/")[-1]
        self.checkFileExt(signalViewer.filenames)

    # Plotting Functions
    def plotSignal_csv(self, filename):
        self.load_csv_data(filename)
        self.plot()
        self.timer()

    def plotSignal_mat(self, filename):
        self.load_mat_data(filename)
        self.plot()
        self.timer()

    def plotSignal_txt(self, filename):
        self.load_txt_data(filename)
        self.plot()
        self.timer()

    # Reading Files Functions
    def load_csv_data(self, file_name):
        '''
        load the data from user
        :return:
        '''
        self.data = pd.read_csv(file_name)
        self.y = self.data.iloc[:1, 1]
        # self.x = self.data.iloc[:1, 2] # TODO : Convert to dictionary holding all channels

    def load_mat_data(self, file_name):
        mat_file = loadmat(file_name)
        self.data = pd.DataFrame(mat_file['F'])
        self.y = self.data.iloc[:1, 1]

    def load_txt_data(self, file_name):
        self.data = pd.read_csv(file_name, skiprows=[i for i in range(500,7657)])
        self.y = self.data.iloc[:1, 2]

    def plot(self):
        '''
        main plotting function
        :return:
        '''
        # TODO : Adapt to plot all channels in channels dict
        self.data_line1 = self.widget.plotItem.plot(self.y, pen=self.pen1, name='y')

    def update_plot_data(self):
        '''
        update function .... add chunks to self.y from loaded data self.data
        :return:
        '''
        signalViewer.i += 30
        self.y = pd.concat([self.y, self.data.iloc[signalViewer.i:signalViewer.i+self.speed, 1]], axis=0, sort=True)
        self.data_line1.setData(self.y)

    def timer(self):
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
        self.start_bt.clicked.connect(self.timer.start)

    def pause_timer(self):
        '''
        Event of clicking the stop button which stops the signal plotting
        :return:
        '''
        self.pause_bt.clicked.connect(self.timer.stop)

    # def checkFileExt(self, file):
    #     if file.endswith('.csv'):
    #         self.plotSignal_csv(file)
    #     elif file.endswith('.txt'):
    #         self.plotSignal_txt(file)
    #     elif file.endswith('.mat'):
    #         self.plotSignal_mat(file)

    def checkFileExt(self, file):
        for i in file.items():
            print(i)
            if i[1] == '*.csv':
                self.plotSignal_csv(i[0])
            elif i[1] == '*.txt':
                self.plotSignal_txt(i[0])
            elif i[1] == '*.mat':
                self.plotSignal_mat(i[0])


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
