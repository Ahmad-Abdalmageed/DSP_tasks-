from PyQt5 import QtWidgets, uic, QtCore, QtGui
import pyqtgraph as pg
import  startstop3 as ss
import pandas as pd
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
        # self.load_bt.clicked.connect(self.load)
        self.load_data('samples3.csv')
        self.plot()
        self.timer()
        # print(self.filename)
        # print(self.format)

    # def load(self):
    #     self.filename , self.format= QtWidgets.QFileDialog.getOpenFileName(None, 'Load Signal','/home', "Data Files (*.csv)")

    def load_data(self, filename):
        '''
        load the data from user
        :return:
        '''

        self.data = pd.read_csv(filename)
        self.y = self.data.iloc[:1, 1]
        self.x = self.data.iloc[:1, 2] # TODO : Convert to dictionary holding all channels

    def plot(self):
        '''
        main plotting function
        :return:
        '''
        # TODO : Adapt to plot all channels in channels dict

        # Color of each line
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


    def update_plot_data(self):
        '''
        update function .... add chunks to self.y from loaded data self.data
        :return:
        '''
        signalViewer.i += 20
        self.y = pd.concat([self.y, self.data.iloc[signalViewer.i:signalViewer.i+self.speed, 1]], axis=0, sort=True)
        self.data_line1.setData(self.y)
        self.x = pd.concat([self.x, self.data.iloc[signalViewer.i:signalViewer.i+self.speed, 2]], axis=0, sort=True)
        self.data_line2.setData(self.x)

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