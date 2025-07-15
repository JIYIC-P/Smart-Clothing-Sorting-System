import cv2
import numpy as np

# 改成你的图片名
path = '7.jpg'
img  = cv2.imread(path)
if img is None:
    raise FileNotFoundError('图片没找到')
hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.namedWindow('Tune')
for ch in ['H','S','V']:
    for rng in ['min','max']:
        default = 0 if rng=='min' else {'H':179,'S':255,'V':255}[ch]
        cv2.createTrackbar(f'{ch}{rng}','Tune',default,
                           {'H':179,'S':255,'V':255}[ch], lambda x:None)

while True:
    hmin = cv2.getTrackbarPos('Hmin','Tune')
    smin = cv2.getTrackbarPos('Smin','Tune')
    vmin = cv2.getTrackbarPos('Vmin','Tune')
    hmax = cv2.getTrackbarPos('Hmax','Tune')
    smax = cv2.getTrackbarPos('Smax','Tune')
    vmax = cv2.getTrackbarPos('Vmax','Tune')

    mask = cv2.inRange(hsv, (hmin,smin,vmin), (hmax,smax,vmax))
    mask = cv2.bitwise_not(mask)          # 1=衣物区域
    vis  = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('mask', mask)
    cv2.imshow('result', vis)
    if cv2.waitKey(1) & 0xFF == 27:       # Esc 退出
        break
cv2.destroyAllWindows()