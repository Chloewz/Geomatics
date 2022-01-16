"""
Created by Chloe on 2021/10/30
"""

import cv2.cv2 as cv2
# import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 图像字体汉化


# 统计直方图参数-matplotlib
def calHist_mat(img):
    # 图片转化为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # calcHist返回一个数组，该例中为256*1的数组，值为对应灰度的像素个数，下标即为像素值
    # calcHist函数的参数依次为:images, channels, mask(掩膜), histSize, ranges
    hist = cv2.calcHist([gray], [0], None, [256], [0, 255])     # mask为None表示处理整幅图像
    return hist


# 绘制三通道直方图（BGR）-matplotlib
def calHistThree_mat(img):
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        hist_three = cv2.calcHist([img], [i], None, [256], [0, 255])
        # 直接绘制三通道直方图的图像
        plt.subplot(224), plt.plot(hist_three, color=col)
        plt.xlim([0, 256]), plt.title('Histogram')
    return 0


# 主程序
if __name__ == '__main__':
    # 读入图片
    image = cv2.imread("D:\\pyfiles\\DigitalImageProcessing\\image\\zouye.jpg")

    # 转换为灰度图像
    grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 统计直方图参数
    hist_num = calHist_mat(image)
    # print(hist_num)

    # 绘制直方图
    plt.subplot(221), plt.imshow(grayImg, 'gray')
    plt.title('grayImage'), plt.axis('off') # 221处为灰度图像
    plt.subplot(222), plt.hist(grayImg.ravel(), 256, [0, 256])  # 使用hist算法绘制直方图
    plt.title('Histogram'), plt.xlim([0, 256]) # 222处为灰度直方图
    plt.subplot(223), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('OriginalImage'), plt.axis('off')    # 223为原图
    calHistThree_mat(image)     # 224为三通道直方图

    plt.tight_layout()  # 自动调整子图间距
    plt.savefig("D:\\pyfiles\\DigitalImageProcessing\\result\\Hist1.png")
    plt.show()
