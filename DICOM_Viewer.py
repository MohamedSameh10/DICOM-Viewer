from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import SimpleITK as sitk
import numpy as np
# from DraggableLines import DraggableHorizontalLine,DraggableVerticalLine

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, figsize=(8, 8)):
        fig = Figure(figsize=figsize)
        self.axes = fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(fig)
        self.setParent(parent)
        self.axes.axis('off')  # Turn off the axes
        self.adjust_size()
    def adjust_size(self):
        # Get the size of the parent widget (vertical layout)
        width = self.parent().width()
        height = self.parent().height()
        # Set the size of the canvas to match the parent widget
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)


class DraggableHorizontalLine:
    def __init__(self, ax, y_pos, on_changed=None):
        self.ax = ax
        self.line = ax.axhline(y=y_pos, color='r', linestyle='--', linewidth=2)
        self.y_pos = y_pos
        y_max, y_min = ax.get_ylim()
        self.height = y_max - y_min
        self.press = None
        self.update_function = on_changed
        self.connect()

    def connect(self):
        self.cidpress = self.line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.line.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.line.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.ax: return
        contains, attrd = self.line.contains(event)
        if not contains:return
        self.press = self.line.get_ydata()[0], event.ydata

    def on_motion(self, event):
        if self.press is None:
            return
        if event.inaxes != self.ax:
            return
        ydata, ypress = self.press
        dy = event.ydata - ypress
        new_y_pos = ydata + dy
        # print('new y= ',new_y_pos)
        # print('height= ',self.height)
        if 0 <= new_y_pos <= self.height:  # Ensure the line stays within the axes limits
            self.y_pos = new_y_pos
            self.line.set_ydata([new_y_pos, new_y_pos])
            self.line.figure.canvas.draw()

            if self.update_function:
                self.update_function(new_y_pos)

    def on_changed(self, update_function):
        self.update_function = update_function

    def on_release(self, event):
        self.press = None

class DraggableVerticalLine:
    def __init__(self, ax, x_pos, on_changed=None):
        self.ax = ax
        self.line = ax.axvline(x=x_pos, color='r', linestyle='--', linewidth=2)
        self.x_pos = x_pos
        x_min, x_max = ax.get_xlim()
        self.width = x_max - x_min
        self.press = None
        self.update_function = on_changed
        self.connect()

    def connect(self):
        self.cidpress = self.line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.line.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.line.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.ax: return
        contains, attrd = self.line.contains(event)
        if not contains: return
        self.press = self.line.get_xdata()[0], event.xdata

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.ax: return
        xdata, xpress = self.press
        dx = event.xdata - xpress
        new_x_pos = xdata + dx
        if 0 <= new_x_pos <= self.width:  # Ensure the line stays within the axes limits
            self.x_pos = new_x_pos
            self.line.set_xdata([new_x_pos, new_x_pos])
            self.line.figure.canvas.draw()

            if self.update_function:
                self.update_function(new_x_pos)

    def on_changed(self, update_function):
        self.update_function = update_function

    def on_release(self, event):
        self.press = None

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1023, 860)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 10, 911, 32))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.filename_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.filename_layout.setContentsMargins(0, 0, 0, 0)
        self.filename_layout.setObjectName("filename_layout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.openButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.openButton.setObjectName("openButton")
        self.horizontalLayout.addWidget(self.openButton)
        self.exitButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout.addWidget(self.exitButton)
        self.filename_layout.addLayout(self.horizontalLayout)
        self.File_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.File_label.setFont(font)
        self.File_label.setObjectName("File_label")
        self.filename_layout.addWidget(self.File_label)
        self.filename_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.filename_label.setText("")
        self.filename_label.setObjectName("filename_label")
        self.filename_layout.addWidget(self.filename_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.filename_layout.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(7, 428, 497, 24))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(7, 50, 497, 24))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.spareView = QtWidgets.QGraphicsView(self.centralwidget)
        self.spareView.setGeometry(QtCore.QRect(510, 458, 496, 341))
        self.spareView.setObjectName("spareView")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(510, 50, 496, 24))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 80, 491, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(510, 80, 491, 341))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 460, 491, 341))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.openButton.clicked.connect(self.getFile)
        self.exitButton.clicked.connect(sys.exit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dicom Viewer"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.File_label.setText(_translate("MainWindow", "File"))
        self.label_3.setText(_translate("MainWindow", "Sagittal"))
        self.label.setText(_translate("MainWindow", "Axial"))
        self.label_2.setText(_translate("MainWindow", "Coronal"))

    def read_dcms(self, directory):
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(directory)
        reader.SetFileNames(dicom_names)
        image_sitk = reader.Execute()
        image_np = sitk.GetArrayFromImage(image_sitk)
        return image_np

    def getFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        seriesPath = QFileDialog.getExistingDirectory()
        #
        self.File_label.setText('File:')
        self.filename_label.setText(seriesPath)

        self.slices = self.read_dcms(seriesPath)
        size = self.slices.shape

        # Create the axial canvas
        self.axial_canvas = MatplotlibCanvas(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.axial_canvas)
        self.axial_axes = self.axial_canvas.axes
        # self.axial_canvas.axes.cla()
        self.axial_axes.imshow(self.slices[size[0] // 2, :, :], cmap='gray')
        self.drag_axial_h = DraggableHorizontalLine(self.axial_axes, y_pos=size[1] // 2)
        self.drag_axial_v = DraggableVerticalLine(self.axial_axes, x_pos=size[2] // 2)

        self.sagittal_canvas = MatplotlibCanvas(self.verticalLayoutWidget_3)
        self.verticalLayout_3.addWidget(self.sagittal_canvas)
        self.sagittal_axes = self.sagittal_canvas.axes
        # self.sagittal_canvas.axes.cla()
        self.sagittal_axes.imshow(np.flipud(self.slices[:, :, size[1]//2]), cmap='gray')
        self.drag_sagittal_h = DraggableHorizontalLine(self.sagittal_axes, y_pos=size[0]//2)
        self.drag_sagittal_v = DraggableVerticalLine(self.sagittal_axes, x_pos=size[2] // 2)

        self.coronal_canvas = MatplotlibCanvas(self.verticalLayoutWidget_2)
        self.verticalLayout_2.addWidget(self.coronal_canvas)
        self.coronal_axes = self.coronal_canvas.axes
        # self.coronal_canvas.axes.cla()
        self.coronal_axes.imshow(np.flipud(self.slices[:,size[2]//2,:]), cmap='gray')
        self.drag_coronal_h = DraggableHorizontalLine(self.coronal_axes, y_pos=size[0] // 2)
        self.drag_coronal_v = DraggableVerticalLine(self.coronal_axes, x_pos=size[1] // 2)

        self.drag_axial_h.on_changed(self.update_coronal)
        self.drag_axial_v.on_changed(self.update_sagittal)

        self.drag_sagittal_h.on_changed(self.update_axial)
        self.drag_sagittal_v.on_changed(self.update_coronal)

        self.drag_coronal_h.on_changed(self.update_axial)
        self.drag_coronal_v.on_changed(self.update_sagittal)

    def update_axial(self,val):
        index = int(val)
        self.axial_axes.images[0].set_array(self.slices[-index, :, :])
        self.axial_canvas.draw_idle()

    def update_sagittal(self,val):
        index = int(val)
        self.sagittal_axes.images[0].set_array(np.flipud(self.slices[:, :, index]))
        self.sagittal_canvas.draw_idle()

    def update_coronal(self,val):
        index = int(val)
        self.coronal_axes.images[0].set_array(np.flipud(self.slices[:, index, :]))
        self.coronal_canvas.draw_idle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
