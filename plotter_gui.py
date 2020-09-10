import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLineEdit

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import pandas as pd
data = pd.read_csv("data.csv")
data.drop('Unnamed: 0',axis=1,inplace=True)

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.text(3,3,"heellloasas")
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object, 
        # which defines a single set of axes as self.axes
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        
        sc.axes.plot(data['x'], data['y'])
        _ = sc.axes.axhline(0,color = 'red',alpha = 0.2)
        _ = sc.axes.axvline(0,color = 'red',alpha = 0.2)
        _ = sc.axes.grid()
        sc.axes.set_xlabel("x")
        sc.axes.set_ylabel("f(x)")
        sc.axes.set_title("Function Plotter")
        
        self.setCentralWidget(sc)
    

        self.show()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()