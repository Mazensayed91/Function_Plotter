from PyQt5.QtWidgets import * 
import sys 
import os
from parsefn import *
import pandas as pd

class Window(QDialog): 
  
    # constructor 
    def __init__(self): 
        super(Window, self).__init__() 
  
        self.setWindowTitle("Plotter") 
  
        self.setGeometry(100, 100, 100, 100) 
  
        self.formGroupBox = QGroupBox("Enter Valid Function") 
  
        self.function = QLineEdit() 
        self.x_min = QLineEdit() 
        self.x_max = QLineEdit() 
        
  
        self.createForm() 
  
        # creating a dialog button for ok and cancel 
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) 
  
        # adding action when form is accepted 
        self.buttonBox.accepted.connect(self.getInfo) 
  
        # addding action when form is rejected 
        self.buttonBox.rejected.connect(self.reject) 
  
        # creating a vertical layout 
        mainLayout = QVBoxLayout() 
  
        # adding form group box to the layout 
        mainLayout.addWidget(self.formGroupBox) 
  
        # adding button box to the layout 
        mainLayout.addWidget(self.buttonBox) 
  
        # setting lay out 
        self.setLayout(mainLayout) 
  
    def getInfo(self): 
        fn = self.function.text()
        x_min = self.x_min.text()
        x_max = self.x_max.text()
        
        file = open("function_data.txt","w+") 
        file.write(fn+"_")
        file.write(x_min+"_")
        file.write(x_max)

        # closing the window 
        self.close() 
        return fn,x_min,x_max
  
    # creat form method 
    def createForm(self): 
  
        # creating a form layout 
        layout = QFormLayout() 
  
        # adding rows 
        layout.addRow(QLabel("Function"), self.function) 
  
        layout.addRow(QLabel("X_Min"), self.x_min) 
  
        layout.addRow(QLabel("X_Max"), self.x_max) 
  
        # setting layout 
        self.formGroupBox.setLayout(layout) 
  
  
if __name__ == '__main__': 
  
    app = QApplication(sys.argv) 
  
    window = Window() 
  
    window.show()
    if app.exec() == 0:
        file1 = open("function_data.txt","r") 
        data = file1.readlines()
        data = data[0].split("_")
        function = data[0]
        x_min = data[1]
        x_max = data[2]
        try:
            eq = DrawEquation(function,int(x_min),int(x_max))
            eq.formatFunction()
            eq.parseEquation()
            xs,ys = eq.evaluateFunction()
        except:
            print("You Entered the function in a wrong format")
            sys.exit(0)
        res = {'x':xs,'y':ys} 
        df = pd.DataFrame(res)
        df.to_csv("data.csv")
        os.system('python plotter_gui.py')
        sys.exit(0)
    #sys.exit(app.exec()) 
