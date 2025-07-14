import cv2
img = cv2.imread("image.jpg")  # 原始读取的图
print("Top-left pixel (B,G,R):", img[0, 0])  # OpenCV默认是BGR