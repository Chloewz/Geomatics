"""
Created by Chloe on 2021/10/26
"""

import cv2.cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt
import GrayImage as Gray

plt.rcParams['font.sans-serif'] = ['SimHei']


# 使用opencv算法求解全局阈值，作为参照
def threshold_Ref(img):
    gray = Gray.gray_function(img)  # 转为灰度图像，使用opencv自带算法
    threshold, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)    # 设127为阈值
    return binary


# 自定义二进制阈值，生成二值图像，大于阈值图像设置为255
def threshold_self(img, threshold):  # threshold为输入的阈值
    gray = cv2.cvtColor(Gray.gray_function(img), cv2.COLOR_BGR2GRAY)    # 灰度化
    binary = np.zeros((height, width), gray.dtype)  # 空白图像存放二值图像，避免对原图修改
    for x in range(height):
        for y in range(width):
            # 判断是否阈值，大于阈值设置为255(全白), 否则设置为0(全黑)
            binary[x, y] = 255 if gray[x, y] >= threshold else 0
    binary = cv2.cvtColor(binary, cv2.COLOR_BGR2RGB)
    return binary


# 自定义反二进制阈值，生成二值图像，大于阈值图像设置为0
def threshold_self_inv(img, threshold):
    gray = cv2.cvtColor(Gray.gray_function(img), cv2.COLOR_BGR2GRAY)
    binary = np.zeros((height, width), gray.dtype)
    for x in range(height):
        for y in range(width):
            # 判断是否阈值，大于阈值设置为0(全黑)，否则设置为255(全白)
            binary[x, y] = 0 if gray[x, y] >= threshold else 255
    binary = cv2.cvtColor(binary, cv2.COLOR_BGR2RGB)
    return binary


# 主程序
if __name__ == '__main__':
    # 读入图片
    image = cv2.imread("D:\\pyfiles\\DigitalImageProcessing\\image\\sylm1.jpeg")

    # 获取图像尺寸
    height, width = image.shape[0:2]

    # 二值化图像
    binary_ref = threshold_Ref(image)
    binary_self = threshold_self(image, 127)
    binary_self_inv = threshold_self_inv(image, 127)

    # 显示图像
    titles = ['cv2.threshold', '自定义二值图像', '自定义反二值图像']  # 标题
    images = [binary_ref, binary_self, binary_self_inv]  # 图像对比显示
    for i in range(3):  # 使用matplotlib绘图
        plt.subplot(1, 3, i + 1)
        plt.imshow(images[i])
        plt.title(titles[i])
        plt.axis('off')  # 关闭坐标轴
    plt.savefig("D:\\pyfiles\\DigitalImageProcessing\\result\\BinaryImage.png", bbox_inches='tight')
    plt.show()
