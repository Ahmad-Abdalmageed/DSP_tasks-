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
    def __init__(self, mainwindow, speed):
        '''
        Main loop of the UI
        :param mainwindow: QMainWindow Object
        '''
        super(signalViewer, self).setupUi(mainwindow)
        # self.data = {}
        self.speed = speed
<<<<<<< Updated upstream

        # Load Button connector
        self.load_bt.clicked.connect(self.load)

        # Plot Configurations

        # Pen color
        self.pen1 = pg.mkPen(color=(0, 255, 0))

        # Setting ranges of the x and y axis
        self.widget.setYRange(min=-1, max=1)
        self.widget.setXRange(min=0, max=4000)

        # set title and add legend
        self.widget.plotItem.setTitle("PLOT")
        self.widget.plotItem.addLegend(size=(2, 3))

        # Grid
        self.widget.plotItem.showGrid(True, True, alpha=0.8)
        self.widget.plotItem.setLabel('bottom', text='Time (ms)')

    def load(self):
        self.filename , self.format= QtWidgets.QFileDialog.getOpenFileName(None, 'Load Signal','/home', "Data Files (*)")
        self.signal_file = self.filename.split("/")[-1]
        self.checkFileExt(self.signal_file)

    def plotSignal_csv(self, filename):
        self.load_csv_data(filename)
        self.plot()
        self.timer()

    def plotSignal_mat(self, filename):
        self.load_mat_data(filename)
        self.plot()
        self.timer()
=======
        self.File = self.load_bt.clicked.connect(self.load)
        print(self.File)
        self.load_data(self.File)
        self.plot()
        self.timer()


    def load(self):
        filename, format= QtWidgets.QFileDialog.getOpenFileName(None, 'Load Signal','/home', "*.csv;; *.edf;;*.mat")
        return [filename, format]
>>>>>>> Stashed changes

    def plotSignal_txt(self, filename):
        self.load_txt_data(filename)
        self.plot()
        self.timer()

    def load_csv_data(self, file_name):
        '''
        load the data from user
        :return:
        '''
<<<<<<< Updated upstream

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
=======
        if filename != None:
            self.data = pd.read_csv(filename[0])
            self.y = self.data.iloc[:1, 1]
            self.x = self.data.iloc[:1, 2] # TODO : Convert to dictionary holding all channels
>>>>>>> Stashed changes

    def plot(self):
        '''
        main plotting function
        :return:
        '''
        # TODO : Adapt to plot all channels in channels dict

<<<<<<< Updated upstream
        self.data_line1 = self.widget.plotItem.plot(self.y, pen=self.pen1, name='y')
        # self.data_line2 = self.widget.plotItem.plot(self.x, pen=pen2, name= 'x')
=======
        # Color of each line
        if hasattr(self,'y'):

            pen2 = pg.mkPen(color=(255, 0, 0))
            pen1 = pg.mkPen(color=(0, 255, 0))
            # Setting ranges of the x and y axis
            self.widget.setYRange(min=-1, max=1)
            self.widget.setXRange(min=0, max=4000)
            # set title and add legend
            self.widget.plotItem.setTitle("PLOT")
            self.widget.plotItem.addLegend(size=(2,3))
            # Grid
            self.widget.plotItem.showGrid(True, True, alpha=0.4)
            self.widget.plotItem.setLabel('bottom', text='Time (ms)')

            #Ploting
            self.data_line1 = self.widget.plotItem.plot(self.y, pen=pen1, name='y')
            self.data_line2 = self.widget.plotItem.plot(self.x, pen=pen2, name= 'x')
>>>>>>> Stashed changes


    def update_plot_data(self):
        '''
        update function .... add chunks to self.y from loaded data self.data
        :return:
        '''
<<<<<<< Updated upstream

        signalViewer.i += 30
        self.y = pd.concat([self.y, self.data.iloc[signalViewer.i:signalViewer.i+self.speed, 1]], axis=0, sort=True)
        self.data_line1.setData(self.y)
        # self.x = pd.concat([self.x, self.data.iloc[signalViewer.i:signalViewer.i+self.speed, 2]], axis=0, sort=True)
        # self.data_line2.setData(self.x)


=======
        if hasattr(self, 'y'):
            signalViewer.i += 20
            self.y = pd.concat([self.y, self.data.iloc[signalViewer.i:signalViewer.i+self.speed, 1]], axis=0, sort=True)
            self.data_line1.setData(self.y)
            self.x = pd.concat([self.x, self.data.iloc[signalViewer.i:signalViewer.i+self.speed, 2]], axis=0, sort=True)
            self.data_line2.setData(self.x)
        # else : pass
>>>>>>> Stashed changes
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

    def checkFileExt(self, file):
        if file.endswith('.csv'):
            self.plotSignal_csv(file)
        elif file.endswith('.txt'):
            self.plotSignal_txt(file)
        elif file.endswith('.mat'):
            self.plotSignal_mat(file)


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
