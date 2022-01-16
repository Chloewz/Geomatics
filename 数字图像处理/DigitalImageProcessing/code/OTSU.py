"""
Created by Chloe on 2021/10/30
"""

import cv2.cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 图像字体汉化


# 大津二值化，返回二值化图像
def otsu(img):
    # 灰度化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    max_gray = 0  # 存储灰度类间方差
    suitable_th = 0  # 存储灰度类间方差对应的阈值
    ave, total = cv2.meanStdDev(gray)   # meanStdDev计算图像的均值和标准偏差，分别用ave和total存储

    # 遍历每一个灰度值, 此时作为阈值
    for threshold in range(255):
        binary = gray > threshold  # 输出为true/false，0/1
        binary_inv = gray <= threshold  # 输出为true/false, 0/1
        fore_pix = np.sum(binary)  # 前景像素总数(c1)
        back_pix = np.sum(binary_inv)  # 后景像素总数(c2)
        if fore_pix == 0:
            break
        if back_pix == 0:
            continue

        w0 = float(fore_pix) / gray.size  # gray.size获得灰度图像总长度，即像素个数
        u0 = float(np.sum(gray * binary)) / fore_pix  # 前景灰度值总和，u0为c1平均灰度
        w1 = float(back_pix) / gray.size
        u1 = float(np.sum(gray * binary_inv)) / back_pix

        class_Var = w0 * w1 * (u0 - u1) * (u0 - u1)  # class_Var为类间方差
        # 取类间方差最大的对应阈值为最终阈值，并计算可分离测度
        if class_Var > max_gray:
            max_gray = class_Var
            suitable_th = threshold
            yita = float(class_Var / (total ** 2))  # yita即为可分离测度值
    print("otsu计算最适阈值为: %d, 可分离测度为: %.20f" % (suitable_th, yita))

    # 生成otsu二值化图像
    binary_otsu = np.zeros((height, width), gray.dtype)
    for i in range(height):
        for j in range(width):
            if gray[i, j] >= suitable_th:
                binary_otsu[i, j] = 255
            else:
                binary_otsu[i, j] = 0
    binary_otsu = cv2.cvtColor(binary_otsu, cv2.COLOR_BGR2RGB)
    return binary_otsu


# 主程序
if __name__ == '__main__':
    # 读入图片
    image = cv2.imread("D:\\pyfiles\\DigitalImageProcessing\\image\\test.tif")

    # 获取图像尺寸
    height, width = image.shape[0:2]

    # opencv大津算法二值化
    threshold_num, binary_th = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_OTSU)
    binary_th = cv2.cvtColor(binary_th, cv2.COLOR_BGR2RGB)
    print('opencv计算阈值threshold_num:', threshold_num)

    # otsu二值化图像
    binary_ot = otsu(image)

    # 显示图像
    titles = ['opencv大津', 'otsu大津']
    images = [binary_th, binary_ot]
    for i in range(2):
        plt.subplot(1, 2, i + 1)
        plt.imshow(images[i], cmap='gray')
        plt.title(titles[i])
        plt.axis('off')
    plt.savefig("D:\\pyfiles\\DigitalImageProcessing\\result\\OTSUImage1.png", bbox_inches='tight')
    plt.show()
