"""
Created by Chloe on 2021/10/26
"""

import cv2.cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']


# opencv内置函数灰度化, 即加权平均
def gray_function(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # COLOR_BGR2GRAY参数表示BGR图像转化为灰度图像
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)  # COLOR_BGR2RGB参数表示BGR图像转化为RGB图像以在plt中显示
    return gray


# 使用最大值灰度化
def gray_Max(img):
    gray = np.zeros((height, width), img.dtype)  # 设置一个新的图像存放灰度图像，防止对原图进行修改
    for i in range(height):
        for j in range(width):
            gray[i, j] = max(img[i, j, 0], img[i, j, 1], img[i, j, 2])  # 最大值设置为灰度
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
    return gray


# 使用平均值灰度化
def gray_Average(img):
    gray = np.zeros((height, width), img.dtype)
    for i in range(height):
        for j in range(width):
            gray[i, j] = (int(img[i, j, 0]) + int(img[i, j, 1]) + int(img[i, j, 2])) / 3  # 平均值作为灰度
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
    return gray


# 使用Gamma校正进行灰度处理
def gray_Gamma(img):
    gray = np.zeros((height, width), img.dtype)
    for i in range(height):
        for j in range(width):
            a = img[i, j, 2] ** 2.2 + 1.5 * img[i, j, 1] ** 2.2 + 0.6 * img[i, j, 0] ** 2.2  # 分子
            b = 1 + 1.5 ** 2.2 + 0.6 ** 2.2  # 分母
            gray[i, j] = pow(a / b, 1.0 / 2.2)  # 开2.2次方根，即Gamma矫正灰度处理
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
    return gray


# 主程序
if __name__ == '__main__':
    # 获取图像
    image = cv2.imread("D:\\pyfiles\\DigitalImageProcessing\\image\\sylm1.jpeg")

    # 获取图像尺寸
    height, width = image.shape[0:2]

    # 将图像灰度化
    gray_func = gray_function(image)
    gray_max = gray_Max(image)
    gray_ave = gray_Average(image)
    gray_gamma = gray_Gamma(image)

    # 显示图像
    titles = ['cv2.cvtColor', '最大值灰度化', '平均值灰度化', 'Gamma校正灰度化']  # 标题
    images = [gray_func, gray_max, gray_ave, gray_gamma]  # 图像对比显示
    for i in range(4):  # 使用matplotlib绘图
        plt.subplot(1, 4, i + 1)
        plt.imshow(images[i])
        plt.title(titles[i])
        plt.axis('off')  # 关闭坐标轴
    plt.savefig("D:\\pyfiles\\DigitalImageProcessing\\result\\GrayImage.png", bbox_inches='tight')  # 文件保存
    plt.show()  # 图像展示
