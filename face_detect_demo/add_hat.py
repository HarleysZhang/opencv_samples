import cv2
import copy
from PIL import Image
import numpy as np

# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
hat_img_bgra = cv2.imread("./images/hat.png", -1) # 图像需为PNG格式（方便alpha通道的使用）
r, g, b, a = cv2.split(hat_img_bgra)
hat_rgb = cv2.merge((r, g, b)) # 把 rgb 三通道合成一张rgb的彩色图, shape is (height, width, channel)

def add_hat(img1, x, y, w, h, img2):
    # 1, 将标志图像缩放到合适尺寸，并以此在原图上创建 ROI，同时将标志图像缩放，并显示
    # I want put img2 on img1's roi, So I create roi
    scaled_factor = w/img2.shape[1]
    resized_hat_h = int(round(img2.shape[0] * scaled_factor))
    if resized_hat_h > y:
        resized_hat_h = y-1		#可调
    img1_roi = img1[y - resized_hat_h : y, x : x + w] # 原ROI中提取放LOGO的区域, roi shape is (173, 253, 3)
    img2_resized = cv2.resize(img2, (img1_roi.shape[1], img1_roi.shape[0])) # 将img2缩放到roi一样大小

    print(img1_roi.shape, img2_resized.shape)

    # 2，得到背景图和前景图的alpha通道，即alpha掩模
    b, g, r, a = cv2.split(img2_resized)
    fg = cv2.merge((b, g, r))
    alpha = cv2.merge((a, a, a)) # 得到前景PNG图像的alpha通道，即alpha掩模
    cv2.imwrite("alpha.jpg",alpha)
    # plt_show_two(img1_roi, alpha, "will be changed roi in img1", "resized img2")

    # 3, 加权乘法运算之前的一些预处理工作
    background = img1_roi.astype(float) # 将数据类型设为float，防止后续乘法运算发生溢出操作
    foreground = fg.astype(float)
    alpha = alpha.astype(float)/255 #将alpha的值归一化在0-1之间，作为加权系数

    # 4, 前景和背景roi图分别乘以对应alpha掩模，前景部分为1（alpha），背景部分为0（1-alpha）
    # 将前景和背景进行加权，每个像素的加权系数即为alpha掩模对应位置像素的值，
    foreground = cv2.multiply(alpha,foreground)
    background = cv2.multiply(1-alpha,background)

    add_ret = cv2.add(background, foreground)
    img1[y - resized_hat_h : y, x : x + w] = add_ret
    return img1

if __name__ == "__main__":
    img = cv2.imread("./images/programmer.png") # 必须为 png 图片
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.4, 5) # Detect the faces
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y: y+h, x: x+w]
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2) # visual face detect bbox
        output_image = add_hat(img, x, y, w, h, hat_rgb)
    
    cv2.imwrite('./images/add_hat.png', output_image)