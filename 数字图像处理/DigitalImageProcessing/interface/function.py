"""
方便起见，将其他函数全部导入其中
下列函数与原py函数做出了简要修改，主要为cv2可以读取，qt可以输出
"""

import cv2.cv2 as cv2
import numpy as np

""" 
灰度化
"""


# opencv内置函数灰度化, 即加权平均
def gray_function(img):
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # COLOR_BGR2GRAY参数表示BGR图像转化为灰度图像
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)  # COLOR_BGR2RGB参数表示BGR图像转化为RGB图像以在plt中显示
    return gray


# 使用最大值灰度化
def gray_Max(img):
    img = cv2.imread(img)
    height, width = img.shape[0:2]
    gray = np.zeros((height, width), img.dtype)  # 设置一个新的图像存放灰度图像，防止对原图进行修改
    for i in range(height):
        for j in range(width):
            gray[i, j] = max(img[i, j, 0], img[i, j, 1], img[i, j, 2])  # 最大值设置为灰度
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
    return gray


# 使用平均值灰度化
def gray_Average(img):
    img = cv2.imread(img)
    height, width = img.shape[0:2]
    gray = np.zeros((height, width), img.dtype)
    for i in range(height):
        for j in range(width):
            gray[i, j] = (int(img[i, j, 0]) + int(img[i, j, 1]) + int(img[i, j, 2])) / 3  # 平均值作为灰度
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
    return gray


# 使用Gamma校正进行灰度处理
def gray_Gamma(img):
    img = cv2.imread(img)
    height, width = img.shape[0:2]
    gray = np.zeros((height, width), img.dtype)
    for i in range(height):
        for j in range(width):
            a = img[i, j, 2] ** 2.2 + 1.5 * img[i, j, 1] ** 2.2 + 0.6 * img[i, j, 0] ** 2.2  # 分子
            b = 1 + 1.5 ** 2.2 + 0.6 ** 2.2  # 分母
            gray[i, j] = pow(a / b, 1.0 / 2.2)  # 开2.2次方根，即Gamma矫正灰度处理
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
    return gray


"""
二值化
"""


# 使用opencv算法求解全局阈值，作为参照
def threshold_Ref(img, threshold):
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    binary = cv2.cvtColor(binary, cv2.COLOR_BGR2RGB)
    return binary


# 自定义二进制阈值，生成二值图像，大于阈值图像设置为255
def threshold_self(img, threshold):  # threshold为输入的阈值
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape[0:2]
    binary = np.zeros((height, width), gray.dtype)  # 空白图像存放二值图像，避免对原图修改
    for x in range(height):
        for y in range(width):
            # 判断是否阈值，大于阈值设置为255(全白)
            binary[x, y] = 255 if gray[x, y] >= threshold else 0
    binary = cv2.cvtColor(binary, cv2.COLOR_BGR2RGB)
    return binary


# 自定义反二进制阈值，生成二值图像，大于阈值图像设置为0
def threshold_self_inv(img, threshold):
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape[0:2]
    binary = np.zeros((height, width), gray.dtype)
    for x in range(height):
        for y in range(width):
            if gray[x, y] >= threshold:
                binary[x, y] = 0
            else:
                binary[x, y] = 255
    binary = cv2.cvtColor(binary, cv2.COLOR_BGR2RGB)
    return binary


"""
大津算法
"""


# 大津二值化，返回二值化图像
def otsu(image):
    image = cv2.imread(image)
    # 灰度化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape[0:2]

    max_gray = 0  # 存储灰度类间方差
    suitable_th = 0  # 存储灰度类间方差对应的阈值
    ave, total = cv2.meanStdDev(gray)

    # 遍历每一个灰度值
    for threshold in range(255):
        binary = gray > threshold  # 输出为true/false
        binary_inv = gray <= threshold  # 输出为true/false
        fore_pix = np.sum(binary)  # 前景像素总数(c1)
        back_pix = np.sum(binary_inv)  # 后景像素总数(c2)
        if fore_pix == 0:
            break
        if back_pix == 0:
            continue

        w0 = float(fore_pix) / gray.size  # gray.size获得灰度图像总长度，即像素个数
        u0 = float(np.sum(gray * binary)) / fore_pix  # c1灰度值总和，u0为c1平均灰度
        w1 = float(back_pix) / gray.size
        u1 = float(np.sum(gray * binary_inv)) / back_pix

        class_Var = w0 * w1 * (u0 - u1) * (u0 - u1)  # class_Var为类间方差
        # 取类间方差最大的对应阈值为最终阈值，并计算可分离测度
        if class_Var > max_gray:
            max_gray = class_Var
            suitable_th = threshold
        #     yita = float(class_Var / (total**2))
    # print("otsu计算最适阈值为: %d, 可分离测度为: %.20f" % (suitable_th, yita))

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


"""
Canny算法进行边界提取
"""


# Canny算法边缘提取
def Canny(img, minT, maxT):
    """
    Canny算法边缘提取
    :param img: 原图像，不为灰度
    :param minT: 低阈值
    :param maxT: 高阈值
    :return: Canny算法结果图像
    """
    img = cv2.imread(img)
    # 获取灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 定义空白图像，用于存放LOG算法提取出的轮廓图
    # canny_img = np.zeros((height, width), dtype=gray.dtype)
    # 定义空白图像，用于存放高斯滤波处理后的图像
    height, width = gray.shape[0:2]
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


# opencv进行Canny算法
def Canny_opencv(img, minT, maxT):
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # 高斯滤波
    Canny_op = cv2.Canny(blur, minT, maxT)  # 80为低阈值，255为高阈值
    return Canny_op
