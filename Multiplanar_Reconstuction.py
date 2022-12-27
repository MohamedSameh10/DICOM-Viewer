from PyQt5 import QtCore, QtGui, QtWidgets
import os
from PyQt5.QtWidgets import QFileDialog
import numpy as np
import pydicom as dcm
from pyqtgraph import ImageView
import pyqtgraph as pg
from scipy.ndimage import rotate

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
        self.coronalView = ImageView(self.centralwidget)
        self.coronalView.setGeometry(QtCore.QRect(510, 80, 496, 342))
        self.coronalView.setObjectName("coronalView")
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
        self.spareView = ImageView(self.centralwidget)
        self.spareView.setGeometry(QtCore.QRect(510, 458, 496, 341))
        self.spareView.setObjectName("spareView")
        self.sagitalView = ImageView(self.centralwidget)
        self.sagitalView.setGeometry(QtCore.QRect(7, 458, 497, 341))
        self.sagitalView.setObjectName("sagitalView")
        self.axialView = ImageView(self.centralwidget)
        self.axialView.setGeometry(QtCore.QRect(7, 80, 497, 342))
        self.axialView.setObjectName("axialView")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(510, 50, 496, 24))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1023, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.openButton.clicked.connect(self.getFile)
        self.exitButton.clicked.connect(sys.exit)

        self.axialView.ui.histogram.hide()
        self.axialView.ui.roiBtn.hide()
        self.axialView.ui.menuBtn.hide()
        self.coronalView.ui.histogram.hide()
        self.coronalView.ui.roiBtn.hide()
        self.coronalView.ui.menuBtn.hide()
        self.sagitalView.ui.histogram.hide()
        self.sagitalView.ui.roiBtn.hide()
        self.sagitalView.ui.menuBtn.hide()
        self.spareView.ui.histogram.hide()
        self.spareView.ui.roiBtn.hide()
        self.spareView.ui.menuBtn.hide()

        self.vLine = pg.LineSegmentROI([[280, 0], [280, 400]], pen='g',rotatable=False)
        self.hLine = pg.LineSegmentROI([[80, 300], [500, 300]], pen='r',rotatable=False)
        self.roi_7 = pg.LineSegmentROI([[80, 10], [400, 250]], pen='b')

        self.vLine2 = pg.LineSegmentROI([[280, 0], [280, 400]], pen='g', rotatable=False)
        self.hLine2 = pg.LineSegmentROI([[80, 300], [500, 300]], pen='r', rotatable=False)
        self.roi_8 = pg.LineSegmentROI([[80, 10], [400, 250]], pen='b')

        self.vLine3 = pg.LineSegmentROI([[280, 0], [280, 400]], pen='g', rotatable=False)
        self.hLine3 = pg.LineSegmentROI([[80, 300], [500, 300]], pen='r', rotatable=False)
        self.roi_9 = pg.LineSegmentROI([[80, 10], [400, 250]], pen='b')

        self.axialView.addItem(self.vLine, ignoreBounds=False)
        self.axialView.addItem(self.hLine, ignoreBounds=False)
        self.axialView.addItem(self.roi_7, ignoreBounds=False)
        self.coronalView.addItem(self.vLine2, ignoreBounds=False)
        self.coronalView.addItem(self.hLine2, ignoreBounds=False)
        self.coronalView.addItem(self.roi_8, ignoreBounds=False)
        self.sagitalView.addItem(self.vLine3, ignoreBounds=False)
        self.sagitalView.addItem(self.hLine3, ignoreBounds=False)
        self.sagitalView.addItem(self.roi_9, ignoreBounds=False)

        self.vLine.sigRegionChanged.connect(self.vdragaxial)
        self.hLine.sigRegionChanged.connect(self.hdragaxial)
        self.vLine2.sigRegionChanged.connect(self.vdragcoronal)
        self.hLine2.sigRegionChanged.connect(self.hdragcoronal)
        self.vLine3.sigRegionChanged.connect(self.vdragsagital)
        self.hLine3.sigRegionChanged.connect(self.hdragsagital)
        self.roi_7.sigRegionChanged.connect(self.oblique)

    def getFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        seriesPath = QFileDialog.getExistingDirectory()

        browsed_files = []
        for path in os.listdir(seriesPath):
            full_path = os.path.join(seriesPath, path)
            if os.path.isfile(full_path):
                browsed_files.append(full_path)

        self.File_label.setText('File:')
        self.filename_label.setText(seriesPath)

        ct_images = browsed_files
        slices = [dcm.read_file(image_file, force=True) for image_file in ct_images]
        slices = sorted(slices, key=lambda x: x.ImagePositionPatient[2])
        self.img_shape = list(slices[0].pixel_array.shape)
        self.img_shape.append(len(slices))
        self.volume3d = np.zeros(self.img_shape)
        print(slices[10])
        for i, s in enumerate(slices):
            array2D = s.pixel_array
            self.volume3d[:, :, i] = array2D

        axial_image = self.volume3d[:, :, self.img_shape[2] // 2]
        sagital_image = rotate(self.volume3d[:, self.img_shape[1] // 2, :], 180)
        coronal_image = rotate(self.volume3d[self.img_shape[0] // 2, :, :], 180)

        self.axialView.setImage(axial_image,autoRange=True)
        self.coronalView.setImage(coronal_image,autoRange=True)
        self.sagitalView.setImage(sagital_image,autoRange=True)

    def vdragaxial(self):
        coronal_image=self.vLine.getArrayRegion(self.volume3d, self.axialView.imageItem, axes=(0,1))
        self.coronalView.setImage(rotate(coronal_image,180),autoRange=True)
    def hdragaxial(self):
        sagital_image=self.hLine.getArrayRegion(self.volume3d, self.axialView.imageItem, axes=(0,1))
        self.sagitalView.setImage(rotate(sagital_image,180),autoRange=True)
    def vdragcoronal(self):
        sagital_image=self.vLine2.getArrayRegion(self.volume3d, self.coronalView.imageItem, axes=(1, 2))
        self.sagitalView.setImage(rotate(sagital_image,180),autoRange=True)
    def hdragcoronal(self):
        axial_image=self.hLine2.getArrayRegion(self.volume3d, self.coronalView.imageItem, axes=(1, 2))
        self.axialView.setImage(axial_image)
    def vdragsagital(self):
        coronal_image=self.vLine3.getArrayRegion(np.flip(self.volume3d,0), self.sagitalView.imageItem, axes=(0, 2))
        self.coronalView.setImage(rotate(coronal_image,270),autoRange=True)
        #self.coronalView.setImage(coronal_image)
    def hdragsagital(self):
        axial_image=self.hLine3.getArrayRegion(self.volume3d, self.sagitalView.imageItem, axes=(0, 2))
        self.axialView.setImage(axial_image)

    def oblique(self):
        oblique_image = self.roi_7.getArrayRegion(self.volume3d, self.axialView.imageItem, axes=(0, 1))
        self.spareView.setImage(rotate(oblique_image,180),autoRange=True)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.File_label.setText(_translate("MainWindow", "File"))
        self.label_3.setText(_translate("MainWindow", "Sagital"))
        self.label.setText(_translate("MainWindow", "Axial"))
        self.label_2.setText(_translate("MainWindow", "Coronal"))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
