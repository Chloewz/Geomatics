"""
数字图像处理GUI界面主入口
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2.cv2 as cv2

import interface
import function


class MainCode(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        interface.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # 按钮触发事件
        self.actionOpen.triggered.connect(self.openImage)
        self.actionSave.triggered.connect(self.saveImage)
        self.actionOpencvGray.triggered.connect(self.grayOpencv)
        self.actionMax.triggered.connect(self.grayMax)
        self.actionAverage.triggered.connect(self.grayAverage)
        self.actionGamma.triggered.connect(self.grayGamma)

        self.actionSelf.triggered.connect(self.binarySelf)
        self.actionSelfInv.triggered.connect(self.binarySelfInv)
        self.actionOTSU.triggered.connect(self.binaryOTSU)

        # binary图像二值化的滑动条与按钮相接
        if self.actionOpencvBinary.triggered.connect(self.binaryOpencv):
            self.horizontalSliderBinary.valueChanged.connect(self.binaryOpencv)
        elif self.actionSelf.triggered.connect(self.binarySelf):
            self.horizontalSliderBinary.valueChanged.connect(self.binarySelf)
        elif self.actionSelfInv.triggered.connect(self.binarySelfInv):
            self.horizontalSliderBinary.valueChanged.connect(self.binarySelfInv)

        # binary图像二值化的滑动条与显示框相连
        self.spinBoxBinary.valueChanged.connect(self.spinBoxChange)
        self.horizontalSliderBinary.valueChanged.connect(self.sliderChange)

        # 按钮连接
        self.pushButtonLargeOriginal.clicked.connect(self.graphicsLarge)

    # 打开图像--open
    def openImage(self):
        global imgName  # 设置为全局变量
        imgName, imgType = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "打开图片", "",
                                                                 "All Files(*);;*.jpg;;*.png")
        img = QtGui.QPixmap(imgName)  # 通过文件路径获取图片文件
        item = QtWidgets.QGraphicsPixmapItem(img)
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(item)
        self.graphicsViewOriginal.setScene(scene)  # 在graphicsView控件上显示选择的图片

    # 保存图像--save
    def saveImage(self):
        screen = QtWidgets.QApplication.primaryScreen()
        pix = screen.grabWindow(self.graphicsViewResult.winId())
        fd, filetype = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget, "保存图片", "",
                                                             "*.png;;*.jpg;;All Files(*)")
        pix.save(fd)

    # 使图像显示在graphicsViewResult中
    def graphicsView(self, img):
        img = QtGui.QImage(img.data, img.shape[1], img.shape[0],
                           img.shape[1] * img.shape[2],
                           QtGui.QImage.Format_RGB888)
        img = QtGui.QPixmap(img)
        item = QtWidgets.QGraphicsPixmapItem(img)
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(item)
        self.graphicsViewResult.setScene(scene)

    # 灰度化opencv--opencvGray
    def grayOpencv(self):
        gray = function.gray_function(imgName)
        self.graphicsView(gray)

    # 灰度化最大值--Max
    def grayMax(self):
        gray = function.gray_Max(imgName)
        self.graphicsView(gray)

    # 灰度化平均值--Average
    def grayAverage(self):
        gray = function.gray_Average(imgName)
        self.graphicsView(gray)

    # 灰度化伽马校正--Gamma
    def grayGamma(self):
        gray = function.gray_Gamma(imgName)
        self.graphicsView(gray)

    # 滑动条改变时，显示框数值也随之改变
    def sliderChange(self):
        self.spinBoxBinary.setValue(self.horizontalSliderBinary.value())

    # 显示框改变时，滑动条数值也随之改变
    def spinBoxChange(self):
        self.horizontalSliderBinary.setValue(self.spinBoxBinary.value())

    # 二值化opencv--opencvBinary
    def binaryOpencv(self):
        threshold = int(self.horizontalSliderBinary.value())
        binary = function.threshold_Ref(imgName, threshold)
        self.graphicsView(binary)

    # 二值化self--self
    def binarySelf(self):
        threshold = int(self.horizontalSliderBinary.value())
        binary = function.threshold_self(imgName, threshold)
        self.graphicsView(binary)

    # 反二值化self--selfInv
    def binarySelfInv(self):
        threshold = int(self.horizontalSliderBinary.value())
        binary = function.threshold_self_inv(imgName, threshold)
        self.graphicsView(binary)

    # 二值化大津算法--OTSU
    def binaryOTSU(self):
        otsu = function.otsu(imgName)
        self.graphicsView(otsu)

    # 边界提取Canny--Canny
    def edgeDetectionCanny(self):
        return 0

    # 边界提取CannyOpencv

    # 图像的放大
    def graphicsLarge(self):
        img = cv2.imread(imgName)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 图像放大
        imgScale = 1
        imgScale = imgScale + 0.05
        if imgScale >= 1.2:
            imgScale = 1.2

        # 修改图像规模并展示
        Large = QtGui.QImage(img, img.shape[1], img.shape[0],
                             QtGui.QImage.Format_RGB888)
        Large = QtGui.QPixmap(Large)
        item = QtWidgets.QGraphicsPixmapItem(Large)
        item.setScale(imgScale)
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(item)
        self.graphicsViewOriginal.setScene(scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainCode()
    MainWindow.show()
    sys.exit(app.exec_())
