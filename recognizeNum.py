import pytesseract
import os
import cv2
import numpy as np


os.environ['TESSDATA_PREFIX'] = r'D:\Tesseract-OCR'  # 替换为您的实际路径
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'  # 替换为您的实际路径

def get_intersection(h_line, v_line):
    rho_h, theta_h = h_line
    rho_v, theta_v = v_line
    # 计算交点坐标
    x, y = np.linalg.solve(np.array([[np.cos(theta_h), np.sin(theta_h)],
                                     [np.cos(theta_v), np.sin(theta_v)]]).astype(float),
                           np.array([rho_h, rho_v]).astype(float))

    # 将交点坐标转为整数
    x, y = int(x), int(y)

    return x, y


def find_all_squares(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    sharpened = cv2.filter2D(blurred, -1, np.array([[0, -2, 0], [-2, 9, -2], [0, -2, 0]]))  # 强化锐化处理
    edges = cv2.Canny(sharpened, 200, 500)

    # 使用霍夫线变换检测直线
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=175)

    horizontal_lines = []
    vertical_lines = []

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho

            # 转换为图像上的坐标
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            # 计算直线的角度
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

            # 根据角度进行分类，阈值可以根据实际情况调整
            if 0 <= abs(angle) <= 2 or 178 <= abs(angle) <= 175:
                horizontal_lines.append((rho, theta))
            elif 88 <= abs(angle) <= 92:
                vertical_lines.append((rho, theta))

    # 对横线按照从上到下的顺序排序
    horizontal_lines.sort(key=lambda line: line[0])
    merged_horizontal_lines = []
    merged_vertical_lines = []
    merge_threshold = 3
    previous_line = None

    for current_line in horizontal_lines:
        if previous_line is None or current_line[0] - previous_line[0] > merge_threshold:
            merged_horizontal_lines.append((current_line[0], current_line[1]))
        previous_line = current_line

    # 对竖线按照从左到右的顺序排序
    vertical_lines.sort(key=lambda line: line[0])
    previous_line = None
    for current_line in vertical_lines:
        if previous_line is not None and current_line[0] - previous_line[0] <= merge_threshold:
            # 合并相邻的水平线
            merged_vertical_lines[-1] = (current_line[0], current_line[1])
        else:
            merged_vertical_lines.append((current_line[0], current_line[1]))
        previous_line = current_line

    found_squares = []
    threshold = 3

    # 寻找正方形
    for i, h_line in enumerate(merged_horizontal_lines):
        if i >= len(merged_horizontal_lines)-1:
            break
        next_h_line = merged_horizontal_lines[i+1]
        for j, v_line in enumerate(merged_vertical_lines):
            if j >= len(merged_vertical_lines) - 1:
                break
            next_v_line = merged_vertical_lines[j+1]

            p_x1, p_y1 = get_intersection(h_line, v_line)
            p_x2, p_y2 = get_intersection(next_h_line, next_v_line)

            is_square = abs(abs(p_x2-p_x1) - abs(p_y2-p_y1)) <= threshold and abs(p_x2-p_x1) > 15
            if is_square:
                found_squares.append((p_x1, p_y1, p_x2, p_y2))

    return found_squares


def crop_region(image, square):
    (x1, y1, x2, y2) = square

    # 通过切片提取矩形区域
    cropped_region = image[y1:y2, x1:x2]

    return cropped_region


def recognize_digit(image):
    # 预处理图像，例如二值化处理
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    # 使用 pytesseract 进行数字识别
    digit = pytesseract.image_to_string(thresholded, config='--psm 6 digits')  # --psm 6 表示按行识别

    return digit.strip()


def recognize_matrix(image):
    squares = find_all_squares(image)

    crop_images = []
    for square in squares:
        crop_images.append(crop_region(image, square))

    recognized_digits = []

    # 遍历每张小图片进行数字识别
    for i, cropped_image in enumerate(crop_images):
        digit = recognize_digit(cropped_image)
        recognized_digits.append(digit)

    digits_matrix = []
    for i in range(16):
        digits_matrix.append((recognized_digits[i * 10:i * 10 + 10]))

    return digits_matrix, squares