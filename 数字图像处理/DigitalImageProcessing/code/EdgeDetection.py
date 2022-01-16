"""
Created by Chloe on 6/11/2021
"""
import cv2.cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 图像字体汉化


# Canny算法边缘提取
def Canny(img, minT, maxT):
    """
    Canny算法边缘提取
    :param img: 原图像，不为灰度
    :param minT: 低阈值
    :param maxT: 高阈值
    :return: Canny算法结果图像
    """
    # 获取灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 定义空白图像，用于存放高斯滤波处理后的图像
    gauss_img = np.zeros((height, width), dtype=gray.dtype)

    # 定义高斯核卷积模板
    a = np.array([[1, 4, 7, 4, 1],
                  [4, 16, 26, 16, 4],
                  [7, 26, 41, 26, 7],
                  [4, 16, 26, 16, 4],
                  [1, 4, 7, 4, 1]])
    kernel = a * (1 / 273)

    '''
    使用高斯平滑去除噪声
    '''
    # 对图像进行高斯滤波处理
    for i in range(2, height - 2):
        for j in range(2, width - 2):
            sum_num = np.sum(gray[i - 2:i + 2 + 1, j - 2:j + 2 + 1] * kernel)
            gauss_img[i, j] = sum_num

    '''
    按照Sobel滤波器步骤计算梯度幅值与方向，寻找图像强度梯度
    '''
    sobel_img = np.zeros((height, width), dtype=gray.dtype)
    # 对阈值化图像遍历，进行Sobel求解梯度值
    for i in range(height - 1):
        for j in range(width - 1):
            dx = (int(gauss_img[i - 1, j - 1]) + 2 * int(gauss_img[i - 1, j]) + int(gauss_img[i - 1, j + 1])) - (
                    int(gauss_img[i + 1, j - 1]) + 2 * int(gauss_img[i + 1, j]) + int(gauss_img[i + 1, j + 1]))
            dy = (int(gauss_img[i - 1, j + 1]) + 2 * int(gauss_img[i, j + 1]) + int(gauss_img[i + 1, j + 1])) - (
                    int(gauss_img[i - 1, j - 1]) + 2 * int(gauss_img[i, j - 1]) + int(gauss_img[i + 1, j - 1]))
            sobel_img[i, j] = np.sqrt(dx ** 2 + dy ** 2)

    '''
    通过Non-maximum Suppression过滤非边缘元素
    '''
    suppression_img = np.zeros((height, width), dtype=gray.dtype)
    # 对阈值化图像遍历，进行non-maximum suppression
    for i in range(height - 1):
        for j in range(width - 1):
            # 首先仍是Sobel算子的计算结果，因sobel_image后还要用做判断，此处不做修改，而是再生成一系列。
            dx = (int(gauss_img[i - 1, j - 1]) + 2 * int(gauss_img[i - 1, j]) + int(gauss_img[i - 1, j + 1])) - (
                    int(gauss_img[i + 1, j - 1]) + 2 * int(gauss_img[i + 1, j]) + int(gauss_img[i + 1, j + 1]))
            dy = (int(gauss_img[i - 1, j + 1]) + 2 * int(gauss_img[i, j + 1]) + int(gauss_img[i + 1, j + 1])) - (
                    int(gauss_img[i - 1, j - 1]) + 2 * int(gauss_img[i, j - 1]) + int(gauss_img[i + 1, j - 1]))

            # 确保分母不为0
            dx = np.maximum(dx, 1e-10)
            theta = np.arctan(dy / dx)

            '''
            确定梯度角度
            '''
            if -0.4142 < theta < 0.4142:
                angle = 0
            elif 0.4142 < theta < 2.4142:
                angle = 45
            elif abs(theta) > 2.4142:
                angle = 90
            elif -2.4142 < theta < -0.4142:
                angle = 135

            '''
            根据梯度角度方向，求对应的非极大值抑制
            '''
            if angle == 0:
                if max(sobel_img[i, j], sobel_img[i, j - 1], sobel_img[i, j + 1]) == sobel_img[i, j]:
                    # 比较x方向梯度三个值中的最大值，如果Sobel_img[i,j]最大则保留，否则设置为0
                    suppression_img[i, j] = sobel_img[i, j]
                else:
                    suppression_img[i, j] = 0
            elif angle == 45:
                if max(sobel_img[i, j], sobel_img[i - 1, j + 1], sobel_img[i + 1, j - 1]) == sobel_img[i, j]:
                    # 比较正对角线方向梯度三个值中的最大值，如果sobel_img[i,j]最大则保留，否则设置为0
                    suppression_img[i, j] = sobel_img[i, j]
                else:
                    suppression_img[i, j] = 0
            elif angle == 90:
                if max(sobel_img[i, j], sobel_img[i - 1, j], sobel_img[i + 1.j]) == sobel_img[i, j]:
                    # 比较y方向梯度三个值中的最大值，如果sobel_img[i,j]最大则保留，否则设置为0
                    suppression_img[i, j] = sobel_img[i, j]
                else:
                    suppression_img[i, j] = 0
            elif angle == 135:
                if max(sobel_img[i, j], sobel_img[i - 1, j - 1], sobel_img[i + 1, j - 1]) == sobel_img[i, j]:
                    # 比较反对角线方向梯度三个值中的最大值，如果sobel_img[i,j]最大则保留，否则设置为0
                    suppression_img[i, j] = sobel_img[i, j]
                else:
                    suppression_img[i, j] = 0

    '''
    利用双阈值方法确定潜在的边界
    '''
    canny_img = np.zeros((height, width), dtype=gray.dtype)
    # 对阈值化图像遍历，进行双阈值处理
    for i in range(height):
        for j in range(width):
            if suppression_img[i, j] >= maxT:  # 大于高阈值，设置为255
                canny_img[i, j] = 255
            elif suppression_img[i, j] <= minT:  # 小于低阈值，设置为0
                canny_img[i, j] = 0
            else:
                '''
                利用滞后技术跟踪边界，若某一像素位置和strong edge相连的weak edge认定是边界，其余的若边界删除(设为0)
                '''
                # 周围8邻域内有比该像素值更大的像素，则设置为255，否则设置为0
                if max(suppression_img[i - 1, j - 1], suppression_img[i - 1, j], suppression_img[i - 1, j + 1],
                       suppression_img[i, j - 1], suppression_img[i, j + 1], suppression_img[i + 1, j - 1],
                       suppression_img[i + 1, j], suppression_img[i + 1, j + 1]) >= suppression_img[i, j]:
                    canny_img[i, j] = 255
                else:
                    canny_img[i, j] = 0

    # 转为可输出格式
    canny_img = cv2.cvtColor(canny_img, cv2.COLOR_BGR2RGB)
    return canny_img


# 主程序
if __name__ == '__main__':
    # 读取图片
    image = cv2.imread("D:\\pyfiles\\DigitalImageProcessing\\image\\Celtics.jpg")

    # 获取图片尺寸
    height, width = image.shape[0:2]

    # 使用opencv进行Canny算子边缘提取
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (3, 3), 0)  # 高斯滤波
    Canny_opencv = cv2.Canny(gray, 50, 200)  # 80为低阈值，255为高阈值

    # 使用Canny算法进行边缘提取
    Canny_img = Canny(image, 50, 200)
    # cv2.imshow('Canny_img', Canny_img)
    # cv2.waitKey()

    # 将图像转为plt输出格式
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    Canny_opencv = cv2.cvtColor(Canny_opencv, cv2.COLOR_BGR2RGB)

    # 图像显示
    titles = ['原图', 'opencv中canny算法', 'canny算法']
    images = [image, Canny_opencv, Canny_img]
    for i in range(3):
        plt.subplot(1, 3, i + 1)
        plt.imshow(images[i])
        plt.title(titles[i])
        plt.axis('off')
    plt.savefig("D:\\pyfiles\\DigitalImageProcessing\\result\\CannyImage1111.png", bbox_inches='tight')
    plt.show()
