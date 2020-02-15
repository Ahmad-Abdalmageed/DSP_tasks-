from PyQt5 import QtWidgets, uic, QtCore
import pyqtgraph as pg
import  startstop as ss
import pandas as pd
import sys


class signalViewer(ss.Ui_MainWindow):
    i = 0
    def __init__(self, mainwindow):
        '''
        Main loop of the UI
        :param mainwindow:QMainWindow Object
        '''
        super(signalViewer, self).setupUi(mainwindow)
        self.load_data()
        self.plot()
        self.timer()

    def load_data(self):
        '''
        load the data from user
        :return:
        '''
        self.data = pd.read_csv('samples3.csv').astype(float)
        self.y = self.data.iloc[:200, 1]

    def plot(self):
        '''
        main plotting function
        :return:
        '''
        self.widget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.widget.plot(self.y, pen=pen)

    def update_plot_data(self):
        '''
        update function .... add chunks to self.y from loaded data self.data
        :return:
        '''
        signalViewer.i += 200
        self.y = pd.concat([self.y, self.data.iloc[self.i:self.i+200, 1]], axis=0, sort=True)
        # self.x = pd.concat([s elf.x, self.data.iloc[self.i:self.i+200, 1]], axis=0, sort=True)
        self.data_line.setData(self.y)

    def timer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start() ### turn to Button
        self.start_timer()
        self.stop_timer()

    def start_timer(self):
        self.toolButton.clicked.connect(self.timer.start)

    def stop_timer(self):
        self.toolButton_2.clicked.connect(self.timer.stop)



def main():
    '''
    the application startup functions
    :return:
    '''
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = signalViewer(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()