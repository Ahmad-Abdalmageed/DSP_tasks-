from PyQt5 import QtWidgets, uic, QtCore, QtGui
import pyqtgraph as pg
import startstop3 as ss
import pandas as pd
from scipy.io import loadmat
import sys
from pyqtgraph import PlotWidget

class signalViewer(ss.Ui_MainWindow):
    i = 0 # counter represents the chunks size of data to be loaded
    filenames = dict()
    channels = dict()
    chunks = dict()
    graphs = dict()
    channel = 1  # Current Channel

    def __init__(self, mainwindow, speed):
        '''
        Main loop of the UI
        :param mainwindow: QMainWindow Object
        '''
        super(signalViewer, self).setupUi(mainwindow)
        self.speed = speed
        self.filename, self.format = None, None

        # Plot Configurations
        # Pen color
        self.pen1 = pg.mkPen(color=(0, 255, 0))
        # Setting ranges of the x and y axis
        self.widget.setXRange(min=0, max=4000)
        self.widget.setYRange(min=-1, max=1)
        # set title and add legend
        self.widget.plotItem.setTitle("Main Window")
        self.widget.plotItem.addLegend(size=(2, 3))
        # Grid
        self.widget.plotItem.showGrid(True, True, alpha=0.8)
        self.widget.plotItem.setLabel('bottom', text='Time (ms)')
        # TODO : Set Auto Panning
        # Load Button connector
        self.load_bt.clicked.connect(self.load_file)

        self.timer()


    def load_file(self):
        self.filename , self.format= QtWidgets.QFileDialog.getOpenFileName(None, 'Load Signal','/home', "*.csv;;"
                                                                                                        " *.txt;;"
                                                                                                        "*.mat")

        print('File :', self.filename)
        if self.filename in signalViewer.filenames:
            print("You Already choosed that file ")
        else:
            signalViewer.filenames[self.filename] = self.format

        # self.signal_file = self.filename.split("/")[-1]
        self.checkFileExt(signalViewer.filenames)

    # Reading Files Functions
    def load_csv_data(self, file_name):
        '''
        load the data from user
        :return:
        '''
        if file_name in signalViewer.channels :
            print("You Already Loaded this file1")
        else:
            signalViewer.channels[file_name] = pd.read_csv(file_name)
            signalViewer.chunks[file_name] = signalViewer.channels[file_name].iloc[:1,1]
            print(signalViewer.chunks)
            print(signalViewer.channels)
            self.plot(file_name, signalViewer.chunks[file_name])

            # self.x = self.data.iloc[:1, 2] # TODO : Convert to dictionary holding all channels

    def load_mat_data(self, file_name):
        if file_name in signalViewer.channels:
            print("You already loaded this file2")
        else:
            mat_file = loadmat(file_name)
            # signalViewer.channels[file_name] = pd.DataFrame(mat_file['F'])
            # self.y = self.data.iloc[:1, 1]
            signalViewer.channels[file_name] = pd.DataFrame(mat_file['F'])
            signalViewer.chunks[file_name] = signalViewer.channels[file_name].iloc[:1, 1]

    def load_txt_data(self, file_name):
        if file_name in signalViewer.channels:
            print("You already loaded this file3")
        else :
            signalViewer.channels[file_name] = pd.read_csv(file_name, skiprows=[i for i in range(500,7657)])
            # self.y = self.data.iloc[:1, 2]
            signalViewer.chunks[file_name] = signalViewer.channels[file_name].iloc[:1, 2]

    def plot(self, file_name, chunk):
        '''
        main plotting function
        :return:
        '''
        # TODO : Adapt to plot all channels in channels dict
        print('Here')
        name = file_name.split('/')[-1]
        signalViewer.graphs[file_name] = self.widget.plotItem.plot(chunk, name=name, pen=self.pen1)


    def update_plot_data(self):
        '''
        update function .... add chunks to self.y from loaded data self.data
        :return:
        '''

        signalViewer.i += 30

        for chunk in signalViewer.chunks:  # graph ->> file_name
            # self.y = pd.concat([self.y, self.data.iloc[signalViewer.i:signalViewer.i+self.speed, 1]], axis=0, sort=True)
            # self.data_line1.setData(self.y)
            signalViewer.chunks[chunk] = pd.concat([signalViewer.chunks[chunk],
                                                    signalViewer.channels[chunk].iloc[signalViewer.i:signalViewer.i+self.speed, 1]],
                                                   axis=0,sort=True)
            signalViewer.graphs[chunk].setData(signalViewer.chunks[chunk])
            # print(signalViewer.chunks[chunk])


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
            if i[1] == '*.csv':
                self.load_csv_data(i[0])
            elif i[1] == '*.txt':
                self.load_txt_data(i[0])
            elif i[1] == '*.mat':
                self.load_mat_data(i[0])


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
