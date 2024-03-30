# Profile Comparator Official Version 1.1
# Author: Joel Aaron Marquez
#------------------------- Libraries -------------------------------------
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QErrorMessage
from PyQt6.QtGui import QIcon
import matplotlib
import matplotlib.pyplot as plt
from gui_main import Ui_MainWindow
import pandas as pd
from pathlib import Path
from webbrowser import open

#------------------------- Classes ---------------------------------------

# Class To Run the GUI window
class MainWindow(QMainWindow, Ui_MainWindow):

    # Class Variables
    fname_base = str()
    fname_sys = str()
    v_line = None
    data_base = None
    data_sys = None

    def __init__(self):
        """
        Function: Initialization of GUI
        Input: None
        Output: None
        """
        super().__init__()
        self.setupUi(self)

        # Fixed Window
        self.setFixedSize(800,700)

        # Load Icons
        self.setWindowIcon(QIcon(str(Path(__file__).parent.absolute().as_posix()) + '/window.png')) # Set Window Icon
        self.generate_icon('/upload.png', self.open_base);  self.generate_icon('/upload.png', self.open_sys)
        self.generate_icon('/generate.png', self.generate); self.generate_icon('/info.png',self.release_page)
        self.generate_icon('/manual.png', self.user_manual)

        # Interactive Buttons
        self.open_base.clicked.connect(self.get_filename_base)
        self.open_sys.clicked.connect(self.get_filename_sys)
        self.generate.clicked.connect(self.print_results)
        self.user_manual.clicked.connect(self.get_user_manual)
        self.release_page.clicked.connect(self.get_release_page)

    def get_filename_base(self):
        """
        Function: Obtains the filename and show on text bar; for the baseline profile
        Input: None
        Output: None
        """
        self.file_warning_window()

        temp = QFileDialog.getOpenFileName(self, 'Select Dataset', 'c://','Text Files (*.txt *.csv *.xlsx)')[0]

        if temp == "":
            del temp
            return
        
        self.fname_base = temp
        del temp

        self.file_base.clear()
        self.file_base.append(self.fname_base)  

    def get_filename_sys(self):
        """
        Function: Obtains the filename and show on text bar; for the evaluating profile
        Input: None
        Output: None
        """
        self.file_warning_window()

        temp = QFileDialog.getOpenFileName(self, 'Select Dataset', 'c://','Text Files (*.txt *.csv *.xlsx)')[0]
        
        if temp == "":
            return
        
        self.fname_sys = temp
        del temp
        self.file_sys.clear()
        self.file_sys.append(self.fname_sys)    

    def print_results(self):
        """
        Function: Plots the graph based on the files provided with the Matplotlib Backend.
        Input: None
        Output: None
        """

        if not self.fname_base or not self.fname_sys:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle("Error!")
            error_dialog.showMessage('File(s) is missing!')
            error_dialog.exec()
            del error_dialog

        else:
            try:
                
                #Remove and clean up previous session
                plt.close('all')
                self.tableWidget.clear()
                self.tableWidget_2.clear()

                # Call method generate_data to extract data and draw table
                self.generate_data()

                # Call method generate_graph to plot graph using Matplotlib
                self.generate_graph()
            
            except:
                error_dialog = QErrorMessage()
                error_dialog.setWindowTitle("Error!")
                error_dialog.showMessage('Something Went Wrong. Check File(s)')
                error_dialog.exec()
                del error_dialog

    def generate_icon(self, path, obj):
        """
        Funtion: Loads icon in the window
        Input: Path (str) = Filepath of the icon; obj (QtWidgets) = Widget that the icon will appear
        Output: None
        """
        obj.setIcon(QIcon(str(Path(__file__).parent.absolute().as_posix()) + path))

    def get_user_manual(self):
        """
        Funtion: Open link to the user manual online
        Input: None
        Output: None
        """
        open('https://docs.google.com/document/d/1ClcJnKmzTSIvLDunIid1eV5g29stwNJC4oaI_Cu-q2A/edit?usp=sharing')  

    def get_release_page(self):
        """
        Funtion: Open link to the Github repository online
        Input: None
        Output: None
        """
        open('https://github.com/joel-a-marquez/load-profile-comparator')

    def file_warning_window(self):
        """
        Funtion: Open warning dialog for file support
        Input: None
        Output: None
        """
        warning_dialog = QErrorMessage()
        warning_dialog.setWindowTitle("Warning!")
        warning_dialog.showMessage('CSV files are ONLY currently supported. Other data file types may not work as intended.')
        warning_dialog.exec()
        del warning_dialog

    def generate_data(self):
        """
        Funtion: Display data from the selected files.
        Input: None
        Output: None
        """
        # Creating a table with Baseline Data
        self.data_base = pd.read_csv(r'%s' % self.fname_base, names = ["Time (hr)","Load (kW)"])

        self.tableWidget.setColumnCount(len(self.data_base.columns))
        self.tableWidget.setRowCount(len(self.data_base.index))
        self.tableWidget.setHorizontalHeaderLabels(self.data_base.columns)

        self.generate_table(self.data_base, self.tableWidget)

        # Creating a table with System Data
        self.data_sys = pd.read_csv(r'%s' % self.fname_sys, names = ["Time (hr)","Load (kW)"])

        self.tableWidget_2.setColumnCount(len(self.data_sys.columns))
        self.tableWidget_2.setRowCount(len(self.data_sys.index))
        self.tableWidget_2.setHorizontalHeaderLabels(self.data_sys.columns)

        self.generate_table(self.data_sys, self.tableWidget_2)

        # Display Graph Data from System Load Profile
        data_max = self.data_sys[self.data_sys["Load (kW)"]==self.data_sys["Load (kW)"].max()]
        data_min = self.data_sys[self.data_sys["Load (kW)"]==self.data_sys["Load (kW)"].min()]
        self.lineEdit.setText(str(data_max.iloc[0]["Time (hr)"]))
        self.lineEdit_2.setText(str(data_max.iloc[0]["Load (kW)"]))
        self.lineEdit_4.setText(str(data_min.iloc[0]["Time (hr)"]))
        self.lineEdit_3.setText(str(data_min.iloc[0]["Load (kW)"]))
        self.lineEdit_9.setText(str(self.data_sys["Time (hr)"].iloc[0]) + ' to ' + str(self.data_sys["Time (hr)"].iloc[-1]))

        # Free Memory after use
        del data_max;  del data_min

    def generate_table(self, data, table):
        """
        Funtion: Generate the tabulated data with pandas library and the selected files.
        Input: data (Pandas Dataframe) = Dataset ; table (QTableWidget) = Table Widget 
        Output: None
        """
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                table.setItem(i,j,QTableWidgetItem(str(round(data.iat[i,j],3))))

    def generate_graph(self):
        # Generate Graph using Matplotlib
        self.fig = plt.figure(figsize=(8, 7), dpi=90)
        self.fig.canvas.manager.set_window_title('Baseline Profile VS. System Profile')
        ax = self.fig.add_subplot(111)
                        
        self.data_base.plot(x = "Time (hr)", ax = ax, picker = True)
        self.data_sys.plot(x = "Time (hr)", ax = ax, picker = True)

        #  Graph Formatting
        plt.title('Baseline Profile VS. System Profile\n', fontsize = 10, fontweight ='bold') 
        plt.legend(['Baseline Load Profile', 'System Load Profile'], loc = 'upper center',bbox_to_anchor=(0.5,-0.07),
                        fancybox=True, shadow=True,ncol=5)
        plt.grid()
        plt.xlabel("Time (hr)");  plt.ylabel("Load (kW)")

        # Generate The Graph
        plt.show()

        # Allows extraction of data to update information on the main window
        self.fig.canvas.mpl_connect('pick_event', self.pick_datapoint)

    def pick_datapoint(self,event):
        """
        Function: Provides Additional Interaction with the Matplotlib Window with the main window
        Input: event (mousePressEvent) = Selects the plotted data on Matplotlib Window
        Output: None
        """

        # Handles first time error of vertical line since it's not produced on initial graph
        if self.v_line != None:  self.v_line.remove()
        
        # Get the point data
        data_point = event.artist
        xdata = data_point.get_xdata(); ydata = data_point.get_ydata()
        ind = event.ind
        
        # Display information of selected point in main window
        self.lineEdit_6.setText(str(xdata[ind][-1])) # Print time
        if not self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]].empty: # Highlight Baseline Load Profile Table of Selected Point
            self.tableWidget.verticalScrollBar().setValue(self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]]["Time (hr)"].item()-self.data_base["Time (hr)"].loc[0]-5)
            self.tableWidget.selectRow(self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]]["Time (hr)"].item()-self.data_base["Time (hr)"].loc[0])
        if not self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]].empty: # Highlight System Load Profile Table of Selected Point
            self.tableWidget_2.verticalScrollBar().setValue(self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]]["Time (hr)"].item()-self.data_sys["Time (hr)"].loc[0]-5)
            self.tableWidget_2.selectRow(self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]]["Time (hr)"].item()-self.data_sys["Time (hr)"].loc[0])


        # If else to allow accurate display of points depending on the selection of the grap
        if self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]].empty: # If system data point of selected x-value is non-existent
            point = round(self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item(),3)
            self.lineEdit_7.setText(str(point)) # Print on baseline
            self.lineEdit_5.setText("N/A")
            self.lineEdit_8.setText("N/A") # Print on system
            self.lineEdit_10.setText(str(round(self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item()
                     - self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item(),3)) + "  /  " +
                     str(round((self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item()
                     - self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item())*100/abs(self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item()),3))) # Print Difference Relative to Previous Hour
            self.label_10.setText("Selected Data - Baseline")

        elif self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]].empty: # If baseline data point of selected x-value is non-existent
            point = round(self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item(),3)
            self.lineEdit_8.setText(str(point)) # Print on system
            self.lineEdit_5.setText("N/A")
            self.lineEdit_7.setText("N/A") # Print on baseline
            self.lineEdit_10.setText(str(round(self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item()
                    - self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item(),3))+ "  /  " +
                     str(round((self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item()
                     - self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item())*100/abs(self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item()),3))) # Print Difference Relative to Previous Hour
            self.label_10.setText("Selected Data - System")

        elif ydata[ind][-1] == self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item(): # If selecting the baseline profile
            point = round(self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item(),3)
            self.lineEdit_7.setText(str(round(ydata[ind][-1],3))) # Print on baseline
            self.lineEdit_8.setText(str(point)) # Print on system
            self.lineEdit_5.setText(str(round(point-ydata[ind][-1],3))+ "  /  " +
                    str(round((point-ydata[ind][-1])*100/abs(ydata[ind][-1]),2))) # Print difference
            self.lineEdit_10.setText(str(round(self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item() - 
                    self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item(),3)) + "  /  " +
                     str(round((self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item()
                     - self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item())*100/abs(self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item()),3))) # Print Difference Relative to Previous Hour
            self.label_10.setText("Selected Data - Baseline")

        elif ydata[ind][-1] == self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item(): # If selecting the system profile
            point = round(self.data_base.loc[self.data_base["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item(),3)
            self.lineEdit_8.setText(str(round(ydata[ind][-1],3))) # Print on system
            self.lineEdit_7.setText(str(point)) # Print on baseline
            self.lineEdit_5.setText(str(round(ydata[ind][-1]-point,3)) + "  /  " +  
                    str(round((ydata[ind][-1]-point)*100/abs(point),3))) # Print difference
            self.lineEdit_10.setText(str(round(self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item() - 
                    self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item(),3))+ "  /  " +
                     str(round((self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]]["Load (kW)"].item()
                     - self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item())*100/abs(self.data_sys.loc[self.data_sys["Time (hr)"] == xdata[ind][-1]-1]["Load (kW)"].item()),3))) # Print Difference Relative to Previous Hour
            self.label_10.setText("Selected Data - System")

        else: # Catch Any Errors
            self.lineEdit_8.setText("-");   self.lineEdit_5.setText("-");   self.lineEdit_7.setText("-")
            self.lineEdit_10.setText("-");  self.label_10.setText("Selected Data")

        # Producing/Overwriting a Vertical Line
        self.v_line = plt.axvline(xdata[ind][-1], color='gray', linestyle='--')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # Free Memory after use
        del ind;  del data_point;   del point

#------------------------------- Main -------------------------------------

def run_gui():

    # Enable backend use for PyQT6
    matplotlib.use('QTAgg')

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    run_gui();